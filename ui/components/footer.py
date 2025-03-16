import streamlit as st
from ui.translator import translator as locale

def render_footer():
    """Hiển thị footer với thông tin bổ sung"""
    
    st.markdown("---")
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("### " + locale.get_text("footer.text"))
        
    with cols[1]:
        st.markdown("#### " + locale.get_text("footer.links"))
        st.markdown("- [GitHub](https://github.com/luyen-tran/nuclear-simulation-tool)")
        st.markdown(f"- [{locale.get_text('footer.documentation')}](https://github.com/luyen-tran/nuclear-simulation-tool/blob/main/README.md)")
        
    with cols[2]:
        st.markdown("#### " + locale.get_text("footer.info"))
        st.markdown(locale.get_text("footer.version", version="1.0.0"))
        st.markdown(locale.get_text("footer.last_updated", date="2025-03-16"))