import streamlit as st
from datetime import datetime
from ui.translator import translator as locale

def render_footer() -> None:
    """Renders the footer section with additional information"""
    
    st.markdown("---")
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown(f"### {locale.get_text('footer.text')}")
        
    with cols[1]:
        st.markdown(f"#### {locale.get_text('footer.links')}")
        st.markdown("- [GitHub](https://github.com/luyen-tran/nuclear-simulation-tool)")
        st.markdown(f"- [{locale.get_text('footer.documentation')}](https://github.com/luyen-tran/nuclear-simulation-tool/blob/main/README.MD)")
        
    with cols[2]:
        st.markdown(f"#### {locale.get_text('footer.info')}")
        st.markdown(locale.get_text("footer.version", version="2.0.0"))
        
        # Use current date rather than hardcoded future date
        current_date = datetime.now().strftime("%Y-%m-%d")
        st.markdown(locale.get_text("footer.last_updated", date=current_date))
