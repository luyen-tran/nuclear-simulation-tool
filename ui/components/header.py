import streamlit as st
from ui.translator import translator as locale

def render_header(title=None):
    """Hiển thị header với tiêu đề tùy chỉnh"""
    
    # Kiểm tra chế độ giao diện hiện tại 
    is_dark_mode = bool(st.session_state.get("dark_mode", False))
    
    # Sử dụng CSS đã được định nghĩa trong dashboard.py
    if title is None:
        title = locale.get_text("app.title")
        
    # Hiển thị header container với tiêu đề
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

    # Thêm breadcrumb navigation
    if "current_page" in st.session_state and st.session_state.current_page != locale.get_text("app.title"):
        st.markdown(f"""
        <div class="breadcrumb">
            <strong>{locale.get_text('app.title')}</strong> > <strong>{st.session_state.current_page}</strong>
        </div>
        """, unsafe_allow_html=True)
        
    # Vạch ngăn cách
    st.markdown("---") 