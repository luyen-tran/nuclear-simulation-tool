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
            help=locale.get_text("help.energy_kt")
        )
        
        max_distance = st.slider(
            locale.get_text("blast.distance"),
            min_value=1000,
            max_value=50000,
            value=10000,
            step=1000,
            help=locale.get_text("help.max_distance_m")
        )
    
    with col2:
        density = st.slider(
            locale.get_text("blast.density"),
            min_value=0.1,
            max_value=5.0,
            value=1.225,
            step=0.1,
            help=locale.get_text("help.density")
        )
        
        time_after = st.slider(
            locale.get_text("blast.time"),
            min_value=0.1,
            max_value=60.0,
            value=10.0,
            step=0.1,
            help=locale.get_text("help.time_after_s")
        )
    
    # Tạo model
    model = SedovTaylorModel(energy_kt=yield_kt, ambient_density=density)
    
    # Tính toán bán kính
    radius = model.blast_radius(time_after)
    st.info(locale.get_text("blast.radius", time=time_after, radius=radius))
    
    # Tạo nút chạy mô phỏng
    if st.button(locale.get_text("blast.button"), key="run_blast_sim"):
        with st.spinner(locale.get_text("common.calculating")):
            # Tính toán mô hình
            distances = np.linspace(1, max_distance, 200)
            overpressures = model.overpressure(distances, time_after)
            
            # Tính toán ngưỡng thiệt hại
            damage_thresholds = {
                locale.get_text("chart.window_breakage"): 1.0,  # 1 kPa - cửa kính vỡ
                locale.get_text("chart.moderate_damage"): 7.0,  # 7 kPa - thiệt hại vừa phải
                locale.get_text("chart.severe_damage"): 35.0,  # 35 kPa - thiệt hại nặng
                locale.get_text("chart.reinforced_damage"): 70.0  # 70 kPa - bê tông cốt thép hư hại
            }
            
            # Tạo biểu đồ
            fig = go.Figure()
            
            # Thêm dữ liệu áp suất
            fig.add_trace(go.Scatter(
                x=distances,
                y=overpressures,
                mode='lines',
                name=locale.get_text("chart.overpressure"),
                line=dict(color='red', width=4)
            ))
            
            # Thêm các ngưỡng thiệt hại
            dash_styles = ['dash', 'dot', 'dashdot', 'longdash']
            colors = ['rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 
                      'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)']
            
            for i, (damage_name, threshold) in enumerate(damage_thresholds.items()):
                # Create horizontal line for damage threshold
                fig.add_trace(go.Scatter(
                    x=distances,
                    y=[threshold] * len(distances),
                    mode='lines',
                    name=damage_name,
                    line=dict(color=colors[i], width=2, dash=dash_styles[i])
                ))
            
            # Thiết lập layout
            fig.update_layout(
                title=locale.get_text("blast.chart_title", time=time_after),
                xaxis_title=locale.get_text("blast.x_axis"),
                yaxis_title=locale.get_text("blast.y_axis"),
                yaxis_type="log",
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99
                )
            )
            
            # Hiện biểu đồ
            plotly_chart_with_theme(fig, use_container_width=True)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("blast_wave", locale.current_lang)) 