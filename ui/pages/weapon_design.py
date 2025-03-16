import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang phân tích thiết kế vũ khí hạt nhân"""
    
    # Header
    render_header(locale.get_text("weapon.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        weapon_type = st.selectbox(
            locale.get_text("weapon.type"),
            options=[
                locale.get_text("weapon.type_fission"),
                locale.get_text("weapon.type_boosted"),
                locale.get_text("weapon.type_thermonuclear")
            ],
            index=0
        )
        
        yield_kt = st.slider(
            locale.get_text("weapon.yield"),
            min_value=1.0,
            max_value=10000.0,
            value=20.0,
            step=1.0,
            help="Năng lượng thiết kế tính bằng kiloton"
        )
    
    with col2:
        # Các tham số phụ thuộc vào loại vũ khí
        if weapon_type == locale.get_text("weapon.type_fission"):
            implosion_quality = st.slider(
                locale.get_text("weapon.implosion_quality"),
                min_value=0.3,
                max_value=0.9,
                value=0.7,
                step=0.05
            )
            
            tamper_effectiveness = st.slider(
                locale.get_text("weapon.tamper_effectiveness"),
                min_value=0.1,
                max_value=0.9,
                value=0.5,
                step=0.1
            )
            
            # Tham số bổ sung cho vũ khí phân hạch
            neutron_initiator = st.slider(
                locale.get_text("weapon.neutron_initiator"),
                min_value=0.5,
                max_value=0.99,
                value=0.9,
                step=0.01
            )
            
        elif weapon_type == locale.get_text("weapon.type_boosted"):
            fission_efficiency = st.slider(
                locale.get_text("weapon.fission_efficiency"),
                min_value=0.1,
                max_value=0.5,
                value=0.3,
                step=0.05
            )
            
            tritium_amount = st.slider(
                locale.get_text("weapon.tritium_amount"),
                min_value=1.0,
                max_value=10.0,
                value=3.0,
                step=0.5,
                help="Gam"
            )
            
        else:  # Thermonuclear
            primary_yield = st.slider(
                locale.get_text("weapon.primary_yield"),
                min_value=0.05,
                max_value=0.2,
                value=0.1,
                step=0.01,
                help="Tỷ lệ năng lượng từ giai đoạn đầu"
            )
            
            coupling_efficiency = st.slider(
                locale.get_text("weapon.coupling_efficiency"),
                min_value=0.3,
                max_value=0.9,
                value=0.7,
                step=0.05
            )
            
            secondary_burn = st.slider(
                locale.get_text("weapon.secondary_burn"),
                min_value=0.1,
                max_value=0.7,
                value=0.3,
                step=0.05
            )
    
    # Phân tích thiết kế
    if st.button(locale.get_text("weapon.analyze_button"), type="primary", use_container_width=True):
        with st.spinner(locale.get_text("weapon.analyzing")):
            st.subheader(locale.get_text("weapon.characteristics"))
            
            # Tính toán hiệu suất dựa trên các tham số
            if weapon_type == locale.get_text("weapon.type_fission"):
                efficiency = implosion_quality * tamper_effectiveness * neutron_initiator
                material_type = "U-235" if yield_kt < 50 else "Pu-239"
                
                # Ước tính khối lượng vật liệu phân hạch
                # Giả định: 10-20 kt trên kg vật liệu phân hạch với hiệu suất 100%
                # Thực tế hiệu suất thấp hơn nhiều
                material_kg = yield_kt / (15 * efficiency)
                
                # Tạo bảng vật liệu
                materials_df = pd.DataFrame({
                    locale.get_text("weapon.material_type"): [material_type, locale.get_text("weapon.material_conventional"), locale.get_text("weapon.material_aluminum")],
                    locale.get_text("weapon.material_amount"): [f"{material_kg:.2f} kg", f"{yield_kt*0.1:.1f} kg", f"{material_kg*2.5:.1f} kg"]
                })
                
                st.dataframe(materials_df, use_container_width=True)
                
                # Hiển thị tham số
                st.subheader(locale.get_text("weapon.parameters"))
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(locale.get_text("weapon.implosion_quality"), f"{implosion_quality:.2f}")
                    st.metric(locale.get_text("weapon.neutron_initiator"), f"{neutron_initiator:.2f}")
                
                with col2:
                    st.metric(locale.get_text("weapon.tamper_effectiveness"), f"{tamper_effectiveness:.2f}")
                    st.metric(locale.get_text("weapon.efficiency"), f"{efficiency:.2f}")
                
            elif weapon_type == locale.get_text("weapon.type_boosted"):
                # Hiệu suất tăng cường bởi tritium
                boost_factor = 1 + tritium_amount * 0.5
                efficiency = fission_efficiency * boost_factor
                material_type = "Pu-239"
                
                # Ước tính khối lượng vật liệu
                material_kg = yield_kt / (20 * efficiency)
                
                # Tạo bảng vật liệu
                materials_df = pd.DataFrame({
                    locale.get_text("weapon.material_type"): [material_type, locale.get_text("weapon.material_tritium"), locale.get_text("weapon.material_conventional"), locale.get_text("weapon.material_beryllium")],
                    locale.get_text("weapon.material_amount"): [f"{material_kg:.2f} kg", f"{tritium_amount:.1f} g", f"{yield_kt*0.05:.1f} kg", f"{material_kg*0.5:.1f} kg"]
                })
                
                st.dataframe(materials_df, use_container_width=True)
                
                # Hiển thị tham số
                st.subheader(locale.get_text("weapon.parameters"))
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(locale.get_text("weapon.fission_efficiency"), f"{fission_efficiency:.2f}")
                    st.metric(locale.get_text("weapon.boost_factor"), f"{boost_factor:.2f}x")
                
                with col2:
                    st.metric(locale.get_text("weapon.tritium_amount"), f"{tritium_amount:.1f} g")
                    st.metric(locale.get_text("weapon.efficiency"), f"{efficiency:.2f}")
                
            else:  # Thermonuclear
                # Năng lượng giai đoạn đầu và hai
                primary_kt = yield_kt * primary_yield
                secondary_kt = yield_kt - primary_kt
                
                # Tính hiệu suất tổng thể
                efficiency = primary_yield * 0.3 + (1 - primary_yield) * coupling_efficiency * secondary_burn
                
                # Tính vật liệu
                primary_material = primary_kt / (20 * 0.3)  # Giai đoạn đầu giả định hiệu suất 30%
                secondary_material_LiD = secondary_kt / (50 * secondary_burn)  # Ước tính LiD
                
                # Tạo bảng vật liệu
                materials_df = pd.DataFrame({
                    locale.get_text("weapon.material_type"): [locale.get_text("weapon.material_pu_primary"), locale.get_text("weapon.material_lithium"), locale.get_text("weapon.material_u238"), locale.get_text("weapon.material_conventional")],
                    locale.get_text("weapon.material_amount"): [f"{primary_material:.2f} kg", f"{secondary_material_LiD:.1f} kg", f"{secondary_material_LiD*2:.1f} kg", f"{primary_kt*0.05:.1f} kg"]
                })
                
                st.dataframe(materials_df, use_container_width=True)
                
                # Hiển thị tham số
                st.subheader(locale.get_text("weapon.parameters"))
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(locale.get_text("weapon.primary_yield"), f"{primary_yield:.2f}")
                    st.metric(locale.get_text("weapon.primary_energy"), f"{primary_kt:.1f} kt")
                
                with col2:
                    st.metric(locale.get_text("weapon.coupling_efficiency"), f"{coupling_efficiency:.2f}")
                    st.metric(locale.get_text("weapon.secondary_energy"), f"{secondary_kt:.1f} kt")
                
                with col3:
                    st.metric(locale.get_text("weapon.secondary_burn"), f"{secondary_burn:.2f}")
                    st.metric(locale.get_text("weapon.efficiency"), f"{efficiency:.2f}")
            
            # Tạo biểu đồ phân bố năng lượng
            fig = go.Figure()
            
            if weapon_type == locale.get_text("weapon.type_fission"):
                # Phân bố năng lượng cho vũ khí phân hạch
                energy_types = [locale.get_text("chart.blast"), locale.get_text("chart.thermal"), 
                              locale.get_text("chart.instant_radiation"), locale.get_text("chart.delayed_radiation")]
                energy_fractions = [0.5, 0.35, 0.05, 0.1]
                
            elif weapon_type == locale.get_text("weapon.type_boosted"):
                # Phân bố năng lượng cho vũ khí tăng cường
                energy_types = [locale.get_text("chart.blast"), locale.get_text("chart.thermal"), 
                              locale.get_text("chart.instant_radiation"), locale.get_text("chart.delayed_radiation"), 
                              locale.get_text("chart.fast_neutrons")]
                energy_fractions = [0.45, 0.35, 0.05, 0.05, 0.1]
                
            else:  # Thermonuclear
                # Phân bố năng lượng cho vũ khí nhiệt hạch
                energy_types = [locale.get_text("chart.blast"), locale.get_text("chart.thermal"), 
                              locale.get_text("chart.instant_radiation"), locale.get_text("chart.delayed_radiation"), 
                              locale.get_text("chart.fast_neutrons")]
                energy_fractions = [0.4, 0.35, 0.05, 0.03, 0.17]
            
            colors = ['royalblue', 'crimson', 'gold', 'purple', 'mediumseagreen']
            
            fig.add_trace(go.Pie(
                labels=energy_types,
                values=energy_fractions,
                textinfo='percent+label',
                insidetextorientation='radial',
                marker=dict(colors=colors)
            ))
            
            fig.update_layout(
                title=locale.get_text("chart.energy_distribution"),
                height=400,
                template=theme_manager.get_template()
            )
            
            plotly_chart_with_theme(fig, use_container_width=True)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("weapon_design", locale.current_lang)) 