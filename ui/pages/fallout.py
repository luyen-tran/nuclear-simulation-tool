import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from models.fallout import FalloutModel
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng mưa phóng xạ"""
    
    # Header
    render_header(locale.get_text("fallout.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        yield_kt = st.slider(
            locale.get_text("fallout.yield"),
            min_value=1.0,
            max_value=5000.0,
            value=100.0,
            step=10.0,
            help="Năng lượng vụ nổ tính bằng kiloton"
        )
        
        burst_height = st.slider(
            locale.get_text("fallout.height"),
            min_value=0.0,
            max_value=2000.0,
            value=0.0,
            step=100.0,
            help="Độ cao vụ nổ tính bằng mét"
        )
        
        fission_fraction = st.slider(
            locale.get_text("fallout.fission_fraction"),
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Tỷ lệ năng lượng từ phân hạch"
        )
    
    with col2:
        wind_speed = st.slider(
            locale.get_text("fallout.wind_speed"),
            min_value=0.0,
            max_value=60.0,
            value=15.0,
            step=1.0,
            help="Tốc độ gió (km/h)"
        )
        
        wind_direction = st.slider(
            locale.get_text("fallout.wind_direction"),
            min_value=0,
            max_value=359,
            value=90,
            step=5,
            help="Hướng gió tính theo độ (0=Bắc, 90=Đông, 180=Nam, 270=Tây)"
        )
        
        time_hours = st.slider(
            locale.get_text("fallout.time"),
            min_value=1,
            max_value=336,  # 2 tuần
            value=24,
            step=1,
            help="Thời gian sau vụ nổ tính bằng giờ"
        )
    
    # Khoảng cách cụ thể để hiển thị liều lượng
    specific_distance = st.slider(
        locale.get_text("fallout.specific_distance"),
        min_value=0.5,
        max_value=500.0,
        value=10.0,
        step=0.5,
        help="Khoảng cách cụ thể từ tâm để hiển thị liều lượng"
    )
    
    # Mô phỏng mưa phóng xạ
    if st.button(locale.get_text("fallout.button"), type="primary", use_container_width=True):
        with st.spinner("Đang tính toán mẫu mưa phóng xạ..."):
            # Tính liều lượng tại khoảng cách cụ thể
            # Sử dụng công thức Way-Wigner: R ~ t^-1.2
            # Và tỷ lệ với năng lượng phân hạch, giảm dần theo khoảng cách
            base_dose = 1000 * yield_kt * fission_fraction * (time_hours ** -1.2)
            fallout_dose = base_dose * np.exp(-specific_distance / (wind_speed * time_hours / 24))
            
            if burst_height > 200:  # Vụ nổ trên không cao
                fallout_dose *= 0.1
            
            # Hiển thị liều lượng
            st.info(locale.get_text("fallout.dose_rate", 
                                   distance=specific_distance, 
                                   time=time_hours, 
                                   dose=fallout_dose))
            
            # Tạo dữ liệu mô phỏng 2D
            grid_size = 100
            x = np.linspace(-100, 100, grid_size)
            y = np.linspace(-100, 100, grid_size)
            X, Y = np.meshgrid(x, y)
            
            # Tính toán khoảng cách từ tâm
            distances = np.sqrt(X**2 + Y**2)
            
            # Tính toán góc từ gốc tọa độ
            angles = np.degrees(np.arctan2(Y, X))
            
            # Điều chỉnh góc gió - đảm bảo gió thổi ĐẾN hướng được chỉ định
            wind_effect = np.exp(-((angles - wind_direction + 180) % 360 - 180)**2 / 1000)
            
            # Tính liều lượng phóng xạ
            Z = base_dose * np.exp(-distances / (wind_speed * time_hours / 24 + 1)) * wind_effect
            
            # Điều chỉnh theo độ cao nổ
            if burst_height > 200:
                Z *= 0.1 * np.exp(-burst_height / 1000)
            
            # Tạo biểu đồ mưa phóng xạ
            fig = go.Figure(data=go.Contour(
                z=Z,
                x=x,
                y=y,
                colorscale='Viridis',
                contours=dict(
                    showlabels=True,
                    labelfont=dict(size=12, color='white'),
                ),
                colorbar=dict(
                    title=dict(
                        text=locale.get_text("fallout.dose_rate_unit"),
                        side='right'
                    ),
                    tickmode='auto',
                    tickfont=dict(size=12),
                )
            ))
            
            # Thêm điểm tâm vụ nổ
            fig.add_trace(go.Scatter(
                x=[0],
                y=[0],
                mode='markers',
                marker=dict(
                    size=10,
                    color='red',
                    symbol='circle',
                    line=dict(width=2, color='black')
                ),
                name=locale.get_text("chart.detonation_center")
            ))
            
            # Thêm mũi tên chỉ hướng gió
            arrow_length = 20
            # Tính toán điểm bắt đầu của mũi tên (từ hướng gió thổi)
            # Hướng gió trong khí tượng học là hướng MÀ gió thổi TỪ ĐÓ
            start_x = arrow_length * np.cos(np.radians(wind_direction))
            start_y = arrow_length * np.sin(np.radians(wind_direction))
            
            fig.add_annotation(
                x=start_x, y=start_y,  # Điểm bắt đầu mũi tên (nơi gió thổi từ đó)
                ax=0, ay=0,            # Điểm cuối mũi tên (tâm vụ nổ - nơi gió thổi đến)
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='cyan',
                text=locale.get_text("chart.wind_direction"),
                font=dict(size=12, color='cyan')
            )
            
            # Cấu hình biểu đồ
            fig.update_layout(
                title=locale.get_text("fallout.pattern_title", time=time_hours),
                xaxis_title=locale.get_text("fallout.x_axis"),
                yaxis_title=locale.get_text("fallout.y_axis"),
                height=700,
                template=theme_manager.get_template(),
                margin=dict(t=60, b=60, l=60, r=60),
                autosize=True
            )
            
            plotly_chart_with_theme(fig, use_container_width=True)
            
            # Hiển thị thông tin bổ sung
            with st.expander(locale.get_text("fallout.info_title")):
                st.markdown(f"""
                **{locale.get_text("fallout.info_note")}**
                {locale.get_text("fallout.info_decay")}
                {locale.get_text("fallout.info_ground")}
                {locale.get_text("fallout.info_air")}
                {locale.get_text("fallout.info_wind")}
                {locale.get_text("fallout.info_dose")}
                """)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("fallout", locale.current_lang)) 