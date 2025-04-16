import streamlit as st
import numpy as np
import plotly.graph_objects as go
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme
from models.flash_effects import FlashEffectsModel

def render_page():
    """Hiển thị trang mô phỏng hiệu ứng ánh sáng hạt nhân"""
    
    # Header
    render_header(locale.get_text("flash.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        yield_kt = st.slider(
            locale.get_text("flash.yield"),
            min_value=1.0,
            max_value=5000.0,
            value=20.0,
            step=1.0,
            help="Năng lượng vụ nổ tính bằng kiloton"
        )
        
        max_distance = st.slider(
            locale.get_text("flash.distance"),
            min_value=1.0,
            max_value=100.0,
            value=30.0,
            step=1.0,
            help="Khoảng cách tối đa từ tâm vụ nổ tính bằng km"
        )
    
    with col2:
        burst_height = st.slider(
            locale.get_text("flash.height"),
            min_value=0.0,
            max_value=5000.0,
            value=500.0,
            step=100.0,
            help="Độ cao vụ nổ tính bằng mét"
        )
        
        day_time = st.selectbox(
            locale.get_text("flash.time_of_day"),
            options=[
                locale.get_text("flash.day_time"),
                locale.get_text("flash.twilight"),
                locale.get_text("flash.night_time")
            ],
            index=0,
            help=locale.get_text("flash.time_of_day_help")
        )
    
    # Chạy mô phỏng
    if st.button(locale.get_text("flash.illuminance"), type="primary", use_container_width=True):
        with st.spinner(locale.get_text("common.calculating")):
            # Ánh xạ từ lựa chọn ngôn ngữ sang giá trị trong model
            day_time_mapping = {
                locale.get_text("flash.day_time"): "Ngày",
                locale.get_text("flash.twilight"): "Chạng vạng",
                locale.get_text("flash.night_time"): "Đêm"
            }
            
            # Khởi tạo model với thông số đầu vào
            model = FlashEffectsModel(
                yield_kt=yield_kt, 
                burst_height=burst_height,
                day_condition=day_time_mapping[day_time]
            )
            
            # Tạo dữ liệu mô phỏng
            distances = np.linspace(0.1, max_distance, 100)  # km
            
            # Lấy kết quả từ model
            results = model.calculate_eye_effects(distances)
            
            illuminance = results['illuminance']
            flash_blindness_prob = results['temporary_blindness_probability']
            retinal_burn_prob = results['retinal_burn_probability']
            permanent_damage_prob = results['permanent_damage_probability']
            
            # Tạo biểu đồ độ rọi
            fig1 = go.Figure()
            
            fig1.add_trace(go.Scatter(
                x=distances,
                y=illuminance,
                mode='lines',
                name=locale.get_text("flash.peak_illuminance"),
                line=dict(color='yellow', width=3)
            ))
            
            # Thêm các ngưỡng
            fig1.add_trace(go.Scatter(
                x=[0, max_distance],
                y=[model.flash_blindness_threshold, model.flash_blindness_threshold],
                mode='lines',
                name=locale.get_text("flash.temporary_blindness_threshold"),
                line=dict(dash='dash', color='blue')
            ))
            
            fig1.add_trace(go.Scatter(
                x=[0, max_distance],
                y=[model.retinal_burn_threshold, model.retinal_burn_threshold],
                mode='lines',
                name=locale.get_text("flash.retinal_burn_threshold"),
                line=dict(dash='dash', color='orange')
            ))
            
            fig1.add_trace(go.Scatter(
                x=[0, max_distance],
                y=[model.permanent_damage_threshold, model.permanent_damage_threshold],
                mode='lines',
                name=locale.get_text("flash.permanent_damage_threshold"),
                line=dict(dash='dash', color='red')
            ))
            
            # Cấu hình biểu đồ
            fig1.update_layout(
                title=locale.get_text("flash.illuminance_title"),
                xaxis_title=locale.get_text("flash.x_axis"),
                yaxis_title=locale.get_text("flash.y_axis"),
                yaxis_type="log",
                height=500,
                template=theme_manager.get_template()
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(fig1, use_container_width=True)
            
            # Tạo biểu đồ xác suất tổn thương mắt
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(
                x=distances,
                y=flash_blindness_prob,
                mode='lines',
                name=locale.get_text("flash.temporary_blindness"),
                line=dict(color='blue', width=3)
            ))
            
            fig2.add_trace(go.Scatter(
                x=distances,
                y=retinal_burn_prob,
                mode='lines',
                name=locale.get_text("flash.retinal_burn"),
                line=dict(color='orange', width=3)
            ))
            
            fig2.add_trace(go.Scatter(
                x=distances,
                y=permanent_damage_prob,
                mode='lines',
                name=locale.get_text("flash.permanent_damage"),
                line=dict(color='red', width=3)
            ))
            
            # Cấu hình biểu đồ
            fig2.update_layout(
                title=locale.get_text("flash.damage_title"),
                xaxis_title=locale.get_text("flash.x_axis"),
                yaxis_title=locale.get_text("flash.probability"),
                height=500,
                template=theme_manager.get_template()
            )
            
            # Hiển thị biểu đồ
            plotly_chart_with_theme(fig2, use_container_width=True)
            
            # Tính khoảng cách tối đa cho mỗi loại tác động
            max_flash_blindness = model.get_max_effect_distance("temporary_blindness", 0.5)
            max_retinal_burn = model.get_max_effect_distance("retinal_burn", 0.5)
            max_permanent_damage = model.get_max_effect_distance("permanent_damage", 0.5)
            
            # Hiển thị thông tin bổ sung
            with st.expander(locale.get_text("flash.info_title")):
                st.markdown(f"""
                **{locale.get_text("flash.condition")}:** {day_time}
                
                **{locale.get_text("flash.max_distances")}:**
                - {locale.get_text("flash.temporary_blindness")}: {max_flash_blindness:.2f} km
                - {locale.get_text("flash.retinal_burn")}: {max_retinal_burn:.2f} km
                - {locale.get_text("flash.permanent_damage")}: {max_permanent_damage:.2f} km
                
                **{locale.get_text("flash.effects_title")}:**
                - **{locale.get_text("flash.temporary_blindness_info")}:** {locale.get_text("flash.temporary_blindness_desc")}
                - **{locale.get_text("flash.retinal_burn_info")}:** {locale.get_text("flash.retinal_burn_desc")}
                - **{locale.get_text("flash.permanent_damage_info")}:** {locale.get_text("flash.permanent_damage_desc")}
                
                **{locale.get_text("flash.time_effect_title")}:**
                - {locale.get_text("flash.night_effect")}
                - {locale.get_text("flash.visibility_note")}
                """)
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("flash_effects", locale.current_lang))