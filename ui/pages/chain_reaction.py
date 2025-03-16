import streamlit as st
import numpy as np
import plotly.graph_objects as go
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from models.chain_reaction import ChainReactionModel
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng phản ứng dây chuyền hạt nhân"""
    
    # Header
    render_header(locale.get_text("chain.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        enrichment = st.slider(
            locale.get_text("chain.enrichment"),
            min_value=0.2,
            max_value=0.95,
            value=0.85,
            step=0.05,
            help="Độ giàu của uranium-235"
        )
        
        # Tạo từ điển ánh xạ từ tên hiển thị sang giá trị cho model
        geometry_options = {
            locale.get_text("chain.geometry.sphere"): "sphere",
            locale.get_text("chain.geometry.cylinder"): "cylinder",
            locale.get_text("chain.geometry.slab"): "slab"
        }
        
        geometry_display = st.selectbox(
            locale.get_text("chain.geometry"),
            options=list(geometry_options.keys()),
            index=0,
            help="Hình dạng của vật liệu phân hạch"
        )
        
        # Chuyển đổi từ tên hiển thị sang giá trị sử dụng trong model
        geometry = geometry_options[geometry_display]
    
    with col2:
        neutrons = st.slider(
            locale.get_text("chain.neutrons"),
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Số lượng neutron ban đầu"
        )
        
        mass_ratio = st.slider(
            locale.get_text("chain.mass_ratio"),
            min_value=0.5,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help="Tỷ lệ so với khối lượng tới hạn"
        )
    
    # Tạo model
    model = ChainReactionModel(enrichment=enrichment)
    
    # Tính toán khối lượng tới hạn
    critical_mass = model.calculate_critical_mass(geometry=geometry)
    st.info(locale.get_text("chain.critical_mass", mass=critical_mass))
    
    # Chạy mô phỏng
    if st.button(locale.get_text("chain.button"), type="primary", use_container_width=True):
        with st.spinner("Đang tính toán..."):
            # Mô phỏng phản ứng dây chuyền
            time, neutron_count = model.simulate_chain_reaction(
                initial_neutrons=neutrons,
                mass_ratio=mass_ratio
            )
            
            # Tạo biểu đồ
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=time,
                y=neutron_count,
                mode='lines',
                name=locale.get_text("chart.neutron_population"),
                line=dict(color='red', width=3)
            ))
            
            # Thêm đường tham chiếu cho tính tới hạn
            if mass_ratio > 1.0:
                fig.add_trace(go.Scatter(
                    x=[time[0], time[-1]],
                    y=[neutrons, neutrons],
                    mode='lines',
                    name=locale.get_text("chart.initial_count"),
                    line=dict(dash='dash', color='gray')
                ))
            
            # Cấu hình biểu đồ
            fig.update_layout(
                title=locale.get_text("chart.neutron_population"),
                xaxis_title=locale.get_text("chart.time_seconds"),
                yaxis_title=locale.get_text("chart.neutron_count"),
                yaxis_type="log" if mass_ratio > 1.0 else "linear",
                height=500,
                template=theme_manager.get_template()
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(fig, use_container_width=True)
            
            # Tạo biểu đồ bổ sung về tỷ lệ năng lượng
            if mass_ratio > 1.0:
                # Tính năng lượng (giả định)
                energy = neutron_count * 200  # MeV per fission
                
                energy_fig = go.Figure()
                
                energy_fig.add_trace(go.Scatter(
                    x=time,
                    y=energy,
                    mode='lines',
                    name=locale.get_text("chart.energy_released"),
                    line=dict(color='orange', width=3)
                ))
                
                energy_fig.update_layout(
                    title=locale.get_text("chart.energy_released"),
                    xaxis_title=locale.get_text("chart.time_seconds"),
                    yaxis_title=locale.get_text("chart.energy_mev"),
                    yaxis_type="log",
                    height=400,
                    template=theme_manager.get_template()
                )
                
                plotly_chart_with_theme(energy_fig, use_container_width=True)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("chain_reaction", locale.current_lang)) 