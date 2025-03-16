import streamlit as st
import numpy as np
import plotly.graph_objects as go
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from ui.components.charts import create_heatmap, plotly_chart_with_theme
from models.neutron_transport import NeutronTransportModel
from ui.conclusions import get_conclusions

def render_page():
    """Hiển thị trang mô phỏng phương trình vận chuyển neutron"""
    
    # Header
    render_header(locale.get_text("transport.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        size = st.slider(
            locale.get_text("transport.size"),
            min_value=1.0,
            max_value=50.0,
            value=10.0,
            step=0.5,
            help="Kích thước hệ thống tính bằng cm"
        )
        
        resolution = st.slider(
            locale.get_text("transport.resolution"),
            min_value=50,
            max_value=200,
            value=100,
            step=10,
            help="Độ phân giải không gian"
        )
    
    with col2:
        scattering_xs = st.slider(
            locale.get_text("transport.scattering"),
            min_value=0.01,
            max_value=1.0,
            value=0.1,
            step=0.01,
            help="Tiết diện tán xạ"
        )
        
        absorption_xs = st.slider(
            locale.get_text("transport.absorption"),
            min_value=0.001,
            max_value=0.5,
            value=0.01,
            step=0.001,
            help="Tiết diện hấp thụ"
        )
        
        fission_xs = st.slider(
            locale.get_text("transport.fission"),
            min_value=0.01,
            max_value=0.5,
            value=0.05,
            step=0.01,
            help="Tiết diện phân hạch"
        )
    
    # Chạy mô phỏng
    if st.button(locale.get_text("transport.button"), type="primary", use_container_width=True):
        with st.spinner("Đang tính toán..."):
            # Tạo model
            model = NeutronTransportModel(
                spatial_points=resolution,
                scattering_xs=scattering_xs,
                absorption_xs=absorption_xs,
                fission_xs=fission_xs
            )
            
            # Giải phương trình khuếch tán
            x, flux = model.solve_diffusion_equation(size=size)
            
            # Tạo biểu đồ dòng neutron
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=x,
                y=flux,
                mode='lines',
                name='Neutron Flux',
                line=dict(color='blue', width=3)
            ))
            
            # Cấu hình biểu đồ
            fig.update_layout(
                title=locale.get_text("chart.neutron_flux"),
                xaxis_title=locale.get_text("chart.position"),
                yaxis_title=locale.get_text("chart.flux"),
                height=500,
                template=theme_manager.get_template()
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(fig, use_container_width=True)
            
            # Tạo biểu đồ nhiệt 2D nếu không gian đủ lớn
            if resolution >= 100:
                # Tạo dữ liệu lưới 2D
                x_grid = np.linspace(0, size, resolution)
                y_grid = np.linspace(0, size, resolution)
                X, Y = np.meshgrid(x_grid, y_grid)
                
                # Mô phỏng phân bố 2D (giả định đối xứng hướng tâm)
                Z = np.zeros((resolution, resolution))
                center_x, center_y = resolution // 2, resolution // 2
                for i in range(resolution):
                    for j in range(resolution):
                        r = np.sqrt(((i - center_x) * size / resolution)**2 + 
                                   ((j - center_y) * size / resolution)**2)
                        # Tìm điểm gần nhất trong mảng x
                        idx = np.abs(x - r).argmin() if r <= size/2 else 0
                        Z[i, j] = flux[idx] if idx < len(flux) else 0
                
                # Tạo biểu đồ nhiệt
                heatmap_fig = create_heatmap(
                    x_grid, y_grid, Z,
                    locale.get_text("chart.neutron_flux_2d"),
                    locale.get_text("chart.position"), locale.get_text("chart.position")
                )
                
                # Hiển thị biểu đồ nhiệt
                plotly_chart_with_theme(heatmap_fig, use_container_width=True)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("neutron_transport", locale.current_lang)) 