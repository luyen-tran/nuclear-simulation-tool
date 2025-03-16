import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng hiệu ứng EMP"""
    
    # Header
    render_header(locale.get_text("emp.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        yield_kt = st.slider(
            locale.get_text("emp.yield"),
            min_value=1.0,
            max_value=10000.0,
            value=1000.0,
            step=100.0,
            help="Năng lượng vụ nổ tính bằng kiloton"
        )
        
        burst_height = st.slider(
            locale.get_text("emp.height"),
            min_value=0.0,
            max_value=500.0,
            value=400.0,
            step=10.0,
            help="Độ cao vụ nổ tính bằng km"
        )
    
    with col2:
        max_distance = st.slider(
            locale.get_text("emp.distance"),
            min_value=100,
            max_value=2000,
            value=1000,
            step=100,
            help="Khoảng cách tối đa từ tâm vụ nổ tính bằng km"
        )
        
        surface_conductivity = st.slider(
            locale.get_text("emp.conductivity"),
            min_value=0.0001,
            max_value=0.01,
            value=0.001,
            step=0.0001,
            format="%.4f",
            help="Độ dẫn điện của bề mặt, đơn vị S/m (Siemens/meter)"
        )
    
    # Tính toán hiệu ứng EMP
    if st.button(locale.get_text("emp.button"), type="primary", use_container_width=True):
        with st.spinner("Đang tính toán..."):
            # Giả lập dữ liệu (trong thực tế cần mô hình phức tạp hơn)
            distances = np.linspace(0, max_distance, 100)
            
            # Ước tính cường độ trường điện từ (E field)
            # Công thức giản lược: E = E0 * (H/H0)^0.5 * (Y/Y0)^0.5 * e^(-d/d0)
            # Trong đó E0 = 50000 V/m, H0 = 100 km, Y0 = 1 Mt, d0 = 1000 km
            field_strength = 50000 * (burst_height/100)**0.5 * (yield_kt/1000)**0.5 * np.exp(-distances/1000)
            
            # Cường độ trường từ (B field - theo Tesla)
            magnetic_field = field_strength / 3e8 * (1 + surface_conductivity * 1e4)
            
            # Cường độ xung cảm ứng (V/m mỗi giây)
            induction = field_strength / 1e-6 * (1 + distances/100)**(-1.5)
            
            # Tính xác suất thiệt hại đối với các thiết bị điện tử
            failure_prob = 1.0 - np.exp(-field_strength / 10000)
            
            # Giới hạn giá trị xác suất
            failure_prob = np.clip(failure_prob, 0, 1)
            
            # Tạo DataFrame cho Plotly
            emp_df = pd.DataFrame({
                'distance': distances,
                'field_strength': field_strength,
                'failure_prob': failure_prob,
                'induction': induction
            })
            
            # Thêm ngưỡng thiệt hại vào DataFrame
            threshold_df = pd.DataFrame({
                'distance': [0, max_distance],
                'threshold': [20000, 20000],
                'level': [locale.get_text("emp.threshold_label"), locale.get_text("emp.threshold_label")]
            })
            
            # Tạo DataFrame với các ngưỡng xác suất thiệt hại
            damage_thresholds = []
            for threshold, label in [(0.25, "25%"), (0.5, "50%"), (0.75, "75%")]:
                damage_thresholds.append({
                    'distance': 0, 'threshold': threshold, 'level': locale.get_text("emp.threshold_percentage", percentage=label)
                })
                damage_thresholds.append({
                    'distance': max_distance, 'threshold': threshold, 'level': locale.get_text("emp.threshold_percentage", percentage=label)
                })
            
            damage_threshold_df = pd.DataFrame(damage_thresholds)
            
            # Tạo biểu đồ cường độ điện trường sử dụng Plotly với ngưỡng thiệt hại
            field_fig = go.Figure()
            
            # Thêm đường cường độ điện trường
            field_fig.add_trace(go.Scatter(
                x=emp_df['distance'],
                y=emp_df['field_strength'],
                mode='lines',
                name=locale.get_text("emp.field_strength_trace"),
                line=dict(color="#FF4B00", width=3)
            ))
            
            # Thêm các đường ngưỡng thiệt hại
            for i, group in threshold_df.groupby('level'):
                field_fig.add_trace(go.Scatter(
                    x=group['distance'],
                    y=group['threshold'],
                    mode='lines',
                    name=i,
                    line=dict(color="#00B3FF", width=2, dash='dash')
                ))
            
            # Cấu hình biểu đồ
            field_fig.update_layout(
                title=locale.get_text("emp.field_strength_title"),
                xaxis_title=locale.get_text("emp.x_axis"),
                yaxis_title=locale.get_text("emp.y_axis"),
                yaxis_type="log",  # Sử dụng thang logarit cho trục y
                yaxis=dict(range=[np.log10(1), np.log10(100000)]),  # Giới hạn trục y từ 1 đến 100,000
                xaxis=dict(range=[0, max_distance])  # Giới hạn trục x từ 0 đến max_distance
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(field_fig, use_container_width=True)
            
            # Hiển thị ngưỡng thiệt hại như một chú thích
            st.info(locale.get_text("emp.threshold_note"))
            
            # Tạo biểu đồ xác suất thiệt hại với ngưỡng
            damage_fig = go.Figure()
            
            # Thêm đường xác suất thiệt hại
            damage_fig.add_trace(go.Scatter(
                x=emp_df['distance'],
                y=emp_df['failure_prob'],
                mode='lines',
                name=locale.get_text("emp.damage_probability_trace"),
                line=dict(color="#FF005C", width=3)
            ))
            
            # Thêm các đường ngưỡng thiệt hại
            for i, group in damage_threshold_df.groupby('level'):
                damage_fig.add_trace(go.Scatter(
                    x=group['distance'],
                    y=group['threshold'],
                    mode='lines',
                    name=i,
                    line=dict(color="#0057FF", width=2, dash='dash')
                ))
            
            # Cấu hình biểu đồ
            damage_fig.update_layout(
                title=locale.get_text("emp.damage_title"),
                xaxis_title=locale.get_text("emp.x_axis"),
                yaxis_title=locale.get_text("emp.probability"),
                yaxis=dict(range=[0, 1], tickvals=[0, 0.25, 0.5, 0.75, 1], tickformat='.0%'),  # Giới hạn trục y từ 0 đến 1
                xaxis=dict(range=[0, max_distance])  # Giới hạn trục x từ 0 đến max_distance
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(damage_fig, use_container_width=True)
            
            # Hiển thị chú thích về các ngưỡng - chỉ hiển thị một ngôn ngữ
            st.info(locale.get_text("emp.damage_thresholds_note"))
            
            # Tạo biểu đồ cảm ứng điện từ
            induction_fig = go.Figure()
            
            # Thêm đường cảm ứng điện từ
            induction_fig.add_trace(go.Scatter(
                x=emp_df['distance'],
                y=emp_df['induction'],
                mode='lines',
                name='Cảm ứng điện từ',
                line=dict(color="#00FFD9", width=3)
            ))
            
            # Cấu hình biểu đồ
            induction_fig.update_layout(
                title=locale.get_text("emp.induction_title"),
                xaxis_title=locale.get_text("emp.x_axis"),
                yaxis_title=locale.get_text("emp.induction_y_axis"),  # Sử dụng nhãn trục y cho cảm ứng
                yaxis_type="log",  # Sử dụng thang logarit cho trục y
                xaxis=dict(range=[0, max_distance])  # Giới hạn trục x từ 0 đến max_distance
            )
            
            # Lưu biểu đồ vào session_state để sử dụng khi cần
            st.session_state["induction_chart"] = induction_fig
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(st.session_state["induction_chart"], use_container_width=True)
            
            # Hiển thị thông tin bổ sung
            with st.expander(locale.get_text("emp.induction_title")):
                if locale.current_lang == "vi":
                    st.markdown("""
                    **Hiệu ứng EMP (Electromagnetic Pulse) từ vụ nổ hạt nhân:**
                    
                    1. **E1 (Early-time EMP)**: Xảy ra trong vài nana giây, tạo ra bởi tia gamma tương tác với không khí.
                    
                    2. **E2 (Intermediate-time EMP)**: Kéo dài vài micro giây, tương tự như sét đánh.
                    
                    3. **E3 (Late-time EMP)**: Kéo dài từ vài giây đến vài phút, gây ra bởi sự biến dạng từ trường Trái Đất.
                    
                    **Tác động đến cơ sở hạ tầng:**
                    
                    * Các hệ thống điện tử không được bảo vệ có thể bị hư hỏng hoàn toàn
                    
                    * Lưới điện quốc gia có thể bị sụp đổ
                    
                    * Thiết bị viễn thông, máy tính và mạng internet bị ngắt kết nối
                    
                    * Phương tiện giao thông hiện đại với hệ thống điện tử có thể bị vô hiệu hóa
                    """)
                else:
                    st.markdown("""
                    **EMP (Electromagnetic Pulse) Effects from Nuclear Explosions:**
                    
                    1. **E1 (Early-time EMP)**: Occurs within nanoseconds, generated by gamma rays interacting with air.
                    
                    2. **E2 (Intermediate-time EMP)**: Lasts microseconds, similar to lightning strikes.
                    
                    3. **E3 (Late-time EMP)**: Lasts seconds to minutes, caused by distortion of Earth's magnetic field.
                    
                    **Impact on Infrastructure:**
                    
                    * Unprotected electronic systems can be completely damaged
                    
                    * National power grids can collapse
                    
                    * Telecommunications equipment, computers and internet networks disconnected
                    
                    * Modern vehicles with electronic systems can be disabled
                    """)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("emp_effects", locale.current_lang)) 