import streamlit as st
import numpy as np
import plotly.graph_objects as go
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from models.blast_wave import SedovTaylorModel
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng sóng xung kích"""
    
    # Header
    render_header(locale.get_text("blast.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        yield_kt = st.slider(
            locale.get_text("blast.yield"),
            min_value=1.0,
            max_value=1000.0,
            value=20.0,
            step=1.0,
            help="Năng lượng vụ nổ tính bằng kiloton"
        )
        
        max_distance = st.slider(
            locale.get_text("blast.distance"),
            min_value=1000,
            max_value=50000,
            value=10000,
            step=1000,
            help="Khoảng cách tối đa từ tâm vụ nổ tính bằng mét"
        )
    
    with col2:
        density = st.slider(
            locale.get_text("blast.density"),
            min_value=0.1,
            max_value=5.0,
            value=1.225,
            step=0.1,
            help="Mật độ không khí xung quanh, mặc định là 1.225 kg/m³ (mật độ không khí ở mực nước biển)"
        )
        
        time_after = st.slider(
            locale.get_text("blast.time"),
            min_value=0.1,
            max_value=60.0,
            value=10.0,
            step=0.1,
            help="Thời gian sau vụ nổ tính bằng giây"
        )
    
    # Tạo model
    model = SedovTaylorModel(energy_kt=yield_kt, ambient_density=density)
    
    # Tính toán bán kính
    radius = model.blast_radius(time_after)
    st.info(locale.get_text("blast.radius", time=time_after, radius=radius))
    
    # Chạy mô phỏng
    if st.button(locale.get_text("blast.button"), type="primary", use_container_width=True):
        with st.spinner("Đang tính toán..."):
            # Tính toán dữ liệu mô phỏng
            sim_data = model.simulate_blast_wave(max_distance=max_distance)
            
            # Tìm chỉ số thời gian gần nhất với thời gian được chọn
            time_index = np.abs(sim_data['times'] - time_after).argmin()
            
            # Tạo biểu đồ tương tác sử dụng Plotly
            fig = go.Figure()
            
            # Vẽ đường áp suất
            fig.add_trace(go.Scatter(
                x=sim_data['distances'], 
                y=sim_data['pressures'][:, time_index] / 1000,  # Chuyển sang kPa
                mode='lines',
                name=locale.get_text("chart.overpressure"),
                line=dict(color='red', width=3)
            ))
            
            # Thêm các ngưỡng thiệt hại
            damage_levels = [
                (3, locale.get_text("chart.window_breakage")),
                (7, locale.get_text("chart.moderate_damage")),
                (15, locale.get_text("chart.severe_damage")),
                (35, locale.get_text("chart.reinforced_damage"))
            ]
            
            for pressure, label in damage_levels:
                fig.add_trace(go.Scatter(
                    x=[0, max_distance],
                    y=[pressure, pressure],
                    mode='lines',
                    name=label,
                    line=dict(dash='dash', color='gray')
                ))
                
            # Cấu hình biểu đồ
            fig.update_layout(
                title=locale.get_text("blast.chart_title", time=time_after),
                xaxis_title=locale.get_text("blast.x_axis"),
                yaxis_title=locale.get_text("blast.y_axis"),
                height=600,
                template=theme_manager.get_template()
            )
            
            # Hiện biểu đồ
            plotly_chart_with_theme(fig, use_container_width=True)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("blast_wave", locale.current_lang)) 