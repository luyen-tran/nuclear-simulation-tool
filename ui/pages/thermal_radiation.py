import streamlit as st
import numpy as np
import plotly.graph_objects as go
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from models.thermal_radiation import ThermalRadiationModel
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng hiệu ứng bức xạ nhiệt"""
    
    # Header
    render_header(locale.get_text("thermal.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        yield_kt = st.slider(
            locale.get_text("thermal.yield"),
            min_value=1.0,
            max_value=1000.0,
            value=20.0,
            step=1.0,
            help="Năng lượng vụ nổ tính bằng kiloton"
        )
        
        max_distance = st.slider(
            locale.get_text("thermal.distance"),
            min_value=1.0,
            max_value=50.0,
            value=20.0,
            step=1.0,
            help="Khoảng cách tối đa từ tâm vụ nổ tính bằng km"
        )
    
    with col2:
        burst_height = st.slider(
            locale.get_text("thermal.height"),
            min_value=0.0,
            max_value=5000.0,
            value=0.0,
            step=100.0,
            help="Độ cao vụ nổ tính bằng mét"
        )
    
    # Chạy mô phỏng
    if st.button(locale.get_text("thermal.button"), type="primary", use_container_width=True):
        with st.spinner("Đang tính toán..."):
            # Tạo model
            model = ThermalRadiationModel(
                yield_kt=yield_kt,
                burst_height=burst_height
            )
            
            # Tính toán các hiệu ứng nhiệt ở các khoảng cách khác nhau
            distances = np.linspace(0.1, max_distance, 100)  # km
            thermal_effects = model.calculate_thermal_effects(distances)
            
            # Tạo biểu đồ mật độ năng lượng nhiệt
            fig1 = go.Figure()
            
            fig1.add_trace(go.Scatter(
                x=thermal_effects['distances'],
                y=thermal_effects['energy_density'],
                mode='lines',
                name='Mật độ năng lượng nhiệt',
                line=dict(color='red', width=3)
            ))
            
            # Cấu hình biểu đồ
            fig1.update_layout(
                title=locale.get_text("thermal.energy_title"),
                xaxis_title=locale.get_text("thermal.energy_x_axis"),
                yaxis_title=locale.get_text("thermal.energy_y_axis"),
                yaxis_type="log",
                height=500,
                template=theme_manager.get_template()
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(fig1, use_container_width=True)
            
            # Tạo biểu đồ xác suất bỏng
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(
                x=thermal_effects['distances'],
                y=thermal_effects['first_degree_burn_probability'],
                mode='lines',
                name=locale.get_text("thermal.first_degree"),
                line=dict(color='yellow', width=3)
            ))
            
            fig2.add_trace(go.Scatter(
                x=thermal_effects['distances'],
                y=thermal_effects['second_degree_burn_probability'],
                mode='lines',
                name=locale.get_text("thermal.second_degree"),
                line=dict(color='orange', width=3)
            ))
            
            fig2.add_trace(go.Scatter(
                x=thermal_effects['distances'],
                y=thermal_effects['third_degree_burn_probability'],
                mode='lines',
                name=locale.get_text("thermal.third_degree"),
                line=dict(color='red', width=3)
            ))
            
            # Cấu hình biểu đồ
            fig2.update_layout(
                title=locale.get_text("thermal.burn_title"),
                xaxis_title=locale.get_text("thermal.burn_x_axis"),
                yaxis_title=locale.get_text("thermal.burn_y_axis"),
                height=500,
                template=theme_manager.get_template()
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(fig2, use_container_width=True)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("thermal_radiation", locale.current_lang)) 