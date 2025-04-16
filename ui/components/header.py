import streamlit as st
from typing import Optional
from ui.translator import translator as locale

def apply_header_styles():
    """Apply custom CSS styles for the header"""
    st.markdown("""
    <style>
        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        .stApp {
            margin-top: 0 !important;
        }
        
        .header-container {
            background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-top: 0;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header-title {
            color: white;
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.05em;
        }
        .breadcrumb {
            background-color: #F3F4F6;
            padding: 0.75rem 1rem;
            border-radius: 0.25rem;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        .breadcrumb strong {
            color: #1E40AF;
        }
        .breadcrumb-separator {
            margin: 0 0.5rem;
            color: #6B7280;
        }
        hr {
            height: 3px;
            background: linear-gradient(90deg, #3B82F6 0%, #1E3A8A 100%);
            border: none;
            margin: 1rem 0 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

def render_breadcrumb(home_title: str, current_page: str) -> None:
    """Render breadcrumb navigation component
    
    Args:
        home_title: Title of the home page
        current_page: Title of the current page
    """
    st.markdown(f"""
    <div class="breadcrumb">
        <strong>{home_title}</strong> <span class="breadcrumb-separator">›</span> <strong>{current_page}</strong>
    </div>
    """, unsafe_allow_html=True)

def render_title(title: str) -> None:
    """Render the main title component
    
    Args:
        title: The title to display
    """
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def render_header(title: Optional[str] = None) -> None:
    """Render the complete header with custom title
    
    Args:
        title: Optional custom title. If None, uses the localized app title.
    """
    # Apply custom styles first to avoid any white space
    apply_header_styles()
    
    # Get the app title from localization if not provided
    if title is None:
        title = locale.get_text("app.title")
    
    # Render the main title
    render_title(title)
    
    # Add breadcrumb navigation when on a sub-page
    app_title = locale.get_text("app.title")
    if "current_page" in st.session_state and st.session_state.current_page != app_title:
        render_breadcrumb(app_title, st.session_state.current_page)
    
    # Add separator
    st.markdown("<hr>", unsafe_allow_html=True) 