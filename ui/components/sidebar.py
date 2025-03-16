import streamlit as st
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
import plotly.io as pio
import json
import os

def render_sidebar():
    """Hiển thị thanh bên với ngôn ngữ và danh mục mô phỏng"""
    
    # Thiết lập theme dựa trên tham số URL 
    query_params = st.query_params
    current_theme = query_params.get("theme", ["light"])[0]
    
    # Khởi tạo theme từ query params
    if current_theme in ["light", "dark"]:
        theme_manager.set_theme(current_theme)
    
    # Vẫn giữ lại dark_mode trong session_state để tương thích ngược
    st.session_state["dark_mode"] = theme_manager.is_dark_mode()
    
    # Khởi tạo current_page nếu chưa tồn tại
    if "current_page" not in st.session_state:
        # Mặc định là trang đầu tiên
        st.session_state.current_page = locale.get_text("nav.chain_reaction")
    
    # Áp dụng CSS tùy chỉnh trước khi hiển thị bất kỳ giao diện nào
    apply_theme_css()
    
    with st.sidebar:
        # Logo ứng dụng (tùy chọn)
        # st.image("assets/logo.png", width=100, use_column_width=True)
        
        # Chọn ngôn ngữ
        current_lang = st.selectbox(
            locale.get_text("language.selector"),
            options=["en", "vi"],
            format_func=lambda x: "English" if x == "en" else "Tiếng Việt",
            index=0 if locale.current_lang == "en" else 1
        )
        locale.set_lang(current_lang)
        
        # Tiêu đề ứng dụng - Dùng markdown thay vì title
        st.markdown(f"<div style='font-size:1.8em; font-weight:bold;'>{locale.get_text('app.title')}</div>", unsafe_allow_html=True)
        
        # Danh mục mô phỏng - Dùng markdown thay vì header
        st.markdown(f"<div style='font-size:1.4em; font-weight:bold; margin-top:1rem;'>{locale.get_text('select.category')}</div>", unsafe_allow_html=True)
        
        theoretical_expander = st.expander(locale.get_text("category.theoretical"), expanded=True)
        practical_expander = st.expander(locale.get_text("category.practical"), expanded=True)
        
        with theoretical_expander:
            theoretical_options = [
                locale.get_text("nav.chain_reaction"),
                locale.get_text("nav.neutron_transport"),
                locale.get_text("nav.monte_carlo"),
            ]
            
            for option in theoretical_options:
                if st.button(option, key=f"theoretical_{option}", use_container_width=True):
                    st.session_state.current_page = option
        
        with practical_expander:
            practical_options = [
                locale.get_text("nav.blast_wave"),
                locale.get_text("nav.thermal_radiation"),
                locale.get_text("nav.emp_effects"),
                locale.get_text("nav.fallout"),
                locale.get_text("nav.weapon_design"),
                locale.get_text("nav.flash_effects")
            ]
            
            for option in practical_options:
                if st.button(option, key=f"practical_{option}", use_container_width=True):
                    st.session_state.current_page = option
                    
        # Footer
        st.markdown("---")
        st.markdown(locale.get_text("footer.text"))
        
        # Theme settings section - Dùng markdown thay vì subheader
        st.markdown(f"<div style='font-size:1.2em; font-weight:bold; margin-top:1rem;'>🎨 {locale.get_text('theme.settings')}</div>", unsafe_allow_html=True)
        
        # Sử dụng selectbox thay vì button để đổi theme
        current_theme = theme_manager.get_theme()
        theme_options = ["light", "dark"]
        theme_labels = [locale.get_text("theme.light"), locale.get_text("theme.dark")]
        
        selected_theme_idx = 0 if current_theme == "light" else 1
        selected_label = st.selectbox(
            locale.get_text("theme.selector"),
            options=theme_labels,
            index=selected_theme_idx,
            key="theme_selector"
        )
        
        # Xác định theme được chọn
        selected_theme = theme_options[theme_labels.index(selected_label)]
        
        # Nếu theme đã thay đổi, cập nhật và tải lại trang
        if selected_theme != current_theme:
            # Lưu theme mới vào session state để tránh vòng lặp vô hạn
            if "applied_theme" not in st.session_state or st.session_state["applied_theme"] != selected_theme:
                # Lưu lại theme đã áp dụng
                st.session_state["applied_theme"] = selected_theme
                
                # Cập nhật theme trong session state và theme manager
                theme_manager.set_theme(selected_theme)
                st.session_state["dark_mode"] = theme_manager.is_dark_mode()
                
                # Cập nhật global template cho Plotly
                template_name = "plotly_dark" if theme_manager.is_dark_mode() else "plotly_white"
                pio.templates.default = template_name
                
                # Xóa bất kỳ biểu đồ được lưu trong session_state để vẽ lại
                for key in list(st.session_state.keys()):
                    if key.endswith("_chart"):
                        del st.session_state[key]
                
                # Cập nhật URL parameter
                st.query_params.update(theme=selected_theme)
                
                # Force reload toàn bộ trang
                st.rerun()
        
    # Áp dụng JavaScript để đảm bảo theme được áp dụng đúng
    apply_theme_js()
        
    return st.session_state.current_page

def apply_theme_css():
    """Áp dụng CSS cho theme"""
    # Xác định giá trị màu sắc dựa trên theme hiện tại
    if theme_manager.is_dark_mode():
        # Dark theme colors
        text_color = "#F8F9FA"
        border_color = "#444444"
        button_border = "#4D96FF"
        hover_color = "#3A3F4B"
        expander_color = "#262B3D"
        sidebar_width = "300px"
    else:
        # Light theme colors
        text_color = "#31333F"
        border_color = "#DDDDDD"
        button_border = "#4369B2"
        hover_color = "#E5E9F2"
        expander_color = "#FFFFFF"
        sidebar_width = "300px"
    
    # CSS chung cho cả hai theme
    common_css = f"""
    <style>
        /* CSS variables */
        :root {{
            --background-color: {theme_manager.is_dark_mode() and "#0E1117" or "#FFFFFF"};
            --sidebar-color: {theme_manager.is_dark_mode() and "#0E1117" or "#FFFFFF"};
            --text-color: {text_color};
            --border-color: {border_color};
            --button-border: {button_border};
            --hover-color: {hover_color};
            --expander-color: {expander_color};
        }}
        
        /* Ẩn thanh header mặc định của Streamlit */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        
        /* Điều chỉnh main container để tránh header */
        [data-testid="stAppViewContainer"] {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        /* Đảm bảo sidebar không bị che khuất */
        [data-testid="stSidebar"] {{
            margin-top: 0 !important;
            padding-top: 0 !important;
            z-index: 999999 !important;
        }}
        
        /* Main background */
        html[theme="{theme_manager.get_theme()}"], body, .stApp, [data-testid="stAppViewContainer"] {{
            color: var(--text-color) !important;
            background-color: var(--background-color) !important;
        }}
        
        /* Main content */
        .main, [data-testid="stVerticalBlock"], .element-container, .stMarkdown, .block-container {{
            color: var(--text-color) !important;
            background-color: var(--background-color) !important;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"], section[data-testid="stSidebar"], div[data-testid="stSidebarContent"] {{
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid var(--border-color) !important;
            min-width: {sidebar_width} !important;
            max-width: 300px !important;
        }}
        
        /* Sidebar text */
        [data-testid="stSidebar"] *, [data-testid="stSidebarContent"] * {{
            color: var(--text-color) !important;
        }}
        
        /* Buttons */
        button,
        button[kind="primary"],
        button[kind="secondary"],
        .stButton>button, 
        .stButton button,
        [data-testid="baseButton-secondary"],
        [data-testid="baseButton-primary"] {{
            background-color: var(--sidebar-color) !important;
            color: var(--text-color) !important;
            border-color: var(--button-border) !important;
            transition: all 0.3s ease;
            border-radius: 6px !important;
        }}
        
        button:hover,
        .stButton>button:hover {{
            background-color: var(--hover-color) !important;
            border-color: var(--button-border) !important;
        }}
        
        /* Expander styling */
        [data-testid="stExpander"] {{
            background-color: var(--expander-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
            border-radius: 8px !important;
            margin-bottom: 1rem !important;
        }}
        
        /* Selectbox styling */
        .stSelectbox [data-baseweb="select"],
        [data-baseweb="select"] {{
            background-color: var(--sidebar-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
            border-radius: 6px !important;
        }}
        
        /* Table styling */
        .stDataFrame table, .stTable table {{
            background-color: var(--sidebar-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }}
        
        .stDataFrame th, .stTable th {{
            background-color: var(--expander-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }}
        
        /* Input styling */
        .stTextInput input, 
        .stNumberInput input,
        .stTextArea textarea {{
            background-color: var(--sidebar-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
            border-radius: 6px !important;
        }}
    </style>
    """
    
    st.markdown(common_css, unsafe_allow_html=True)

def apply_theme_js():
    """Áp dụng JavaScript để đảm bảo theme được áp dụng đúng"""
    theme = theme_manager.get_theme()
    is_dark = theme_manager.is_dark_mode()
    
    # Định nghĩa màu sắc dựa trên theme
    if is_dark:
        bg_color = "black"
        sidebar_color = "black"
        text_color = "white"
        border_color = "#444"
    else:
        bg_color = "white"
        sidebar_color = "#white"
        text_color = "#31333F"
        border_color = "#DDDDDD"
    
    # JavaScript đơn giản hơn để áp dụng theme
    st.markdown(f"""
    <script>
        (function() {{
            // Đặt theme attribute cho HTML tag
            document.documentElement.setAttribute('theme', '{theme}');
            
            // Đặt CSS variables
            document.documentElement.style.setProperty('--background-color', '{bg_color}');
            document.documentElement.style.setProperty('--sidebar-color', '{sidebar_color}');
            document.documentElement.style.setProperty('--text-color', '{text_color}');
            document.documentElement.style.setProperty('--border-color', '{border_color}');
            
            // Ẩn header trong sidebar
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {{
                const headers = sidebar.querySelectorAll('h1, h2, h3, h4, h5, h6');
                headers.forEach(header => {{
                    header.style.display = 'none';
                }});
            }}
        }})();
    </script>
    """, unsafe_allow_html=True)