import streamlit as st
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
import plotly.io as pio
import json
import os

def render_sidebar():
    """Render sidebar with language selector and simulation categories"""
    
    # Initialize theme from URL parameters
    _initialize_theme()
    
    # Apply CSS styling
    _apply_theme_css()
    
    with st.sidebar:
        # Language selector
        _render_language_selector()
                
        # Navigation categories
        _render_navigation_categories()
        
        # Theme settings
        _render_theme_settings()
    
    # Apply JavaScript for theme handling
    _apply_theme_js()
        
    return st.session_state.current_page

def _initialize_theme():
    """Initialize theme state from URL parameters"""
    # Get theme from URL parameters
    query_params = st.query_params
    current_theme = query_params.get("theme", ["light"])[0]
    
    # Initialize theme if valid
    if current_theme in ["light", "dark"]:
        theme_manager.set_theme(current_theme)
    
    # Keep dark_mode in session_state for backward compatibility
    st.session_state["dark_mode"] = theme_manager.is_dark_mode()
    
    # Initialize current_page if not exists
    if "current_page" not in st.session_state:
        st.session_state.current_page = locale.get_text("nav.chain_reaction")

def _render_language_selector():
    """Render language selection dropdown"""
    current_lang = st.selectbox(
        locale.get_text("language.selector"),
        options=["en", "vi"],
        format_func=lambda x: "English" if x == "en" else "Tiếng Việt",
        index=0 if locale.current_lang == "en" else 1
    )
    locale.set_lang(current_lang)

def _render_navigation_categories():
    """Render navigation menu with theoretical and practical categories"""
    # Category header
    st.markdown(f"<div style='font-size:1.4em; font-weight:bold; margin-top:1rem;'>{locale.get_text('select.category')}</div>", unsafe_allow_html=True)
    
    # Theoretical category
    with st.expander(locale.get_text("category.theoretical"), expanded=True):
        _render_category_buttons([
            "nav.chain_reaction",
            "nav.neutron_transport",
            "nav.monte_carlo"
        ], "theoretical")
    
    # Practical category
    with st.expander(locale.get_text("category.practical"), expanded=True):
        _render_category_buttons([
            "nav.blast_wave",
            "nav.thermal_radiation",
            "nav.emp_effects",
            "nav.fallout",
            "nav.weapon_design",
            "nav.flash_effects"
        ], "practical")

def _render_category_buttons(option_keys, category_prefix):
    """Render buttons for a specific category
    
    Args:
        option_keys: List of translation keys for buttons
        category_prefix: Prefix for button keys
    """
    for key in option_keys:
        option_text = locale.get_text(key)
        if st.button(option_text, key=f"{category_prefix}_{key}", use_container_width=True):
            st.session_state.current_page = option_text

def _render_theme_settings():
    """Render theme selection dropdown"""
    # Theme section header
    st.markdown(f"<div style='font-size:1.2em; font-weight:bold; margin-top:1rem;'>🎨 {locale.get_text('theme.settings')}</div>", unsafe_allow_html=True)
    
    # Theme selector
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
    
    # Handle theme change
    selected_theme = theme_options[theme_labels.index(selected_label)]
    _handle_theme_change(current_theme, selected_theme)

def _handle_theme_change(current_theme, selected_theme):
    """Handle theme change and apply necessary updates
    
    Args:
        current_theme: Current theme name
        selected_theme: Selected theme name
    """
    if selected_theme != current_theme:
        # Avoid infinite loops by checking if we've already applied this theme
        if "applied_theme" not in st.session_state or st.session_state["applied_theme"] != selected_theme:
            # Save applied theme
            st.session_state["applied_theme"] = selected_theme
            
            # Update theme
            theme_manager.set_theme(selected_theme)
            st.session_state["dark_mode"] = theme_manager.is_dark_mode()
            
            # Update Plotly template
            template_name = "plotly_dark" if theme_manager.is_dark_mode() else "plotly_white"
            pio.templates.default = template_name
            
            # Clear cached charts
            for key in list(st.session_state.keys()):
                if key.endswith("_chart"):
                    del st.session_state[key]
            
            # Update URL parameter
            st.query_params.update(theme=selected_theme)
            
            # Force reload
            st.rerun()

def _apply_theme_css():
    """Apply CSS styling based on current theme"""
    # Get theme values
    is_dark = theme_manager.is_dark_mode()
    
    # Set theme colors
    colors = {
        "text": "#F8F9FA" if is_dark else "#31333F",
        "border": "#444444" if is_dark else "#DDDDDD",
        "button_border": "#4D96FF" if is_dark else "#4369B2",
        "hover": "#3A3F4B" if is_dark else "#E5E9F2",
        "expander": "#262B3D" if is_dark else "#FFFFFF",
        "background": "#0E1117" if is_dark else "#FFFFFF",
        "sidebar": "#0E1117" if is_dark else "#FFFFFF"
    }
    
    # Common CSS
    css = f"""
    <style>
        /* CSS variables */
        :root {{
            --background-color: {colors["background"]};
            --sidebar-color: {colors["sidebar"]};
            --text-color: {colors["text"]};
            --border-color: {colors["border"]};
            --button-border: {colors["button_border"]};
            --hover-color: {colors["hover"]};
            --expander-color: {colors["expander"]};
        }}
        
        /* Layout fixes */
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        
        [data-testid="stAppViewContainer"] {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}
        
        [data-testid="stSidebar"] {{
            margin-top: 0 !important;
            padding-top: 0 !important;
            z-index: 999999 !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }}
        
        /* Theme colors */
        html[theme="{theme_manager.get_theme()}"], body, .stApp, [data-testid="stAppViewContainer"],
        .main, [data-testid="stVerticalBlock"], .element-container, .stMarkdown, .block-container {{
            color: var(--text-color) !important;
            background-color: var(--background-color) !important;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"], section[data-testid="stSidebar"], div[data-testid="stSidebarContent"] {{
            background-color: var(--sidebar-color) !important;
            border-right: 1px solid var(--border-color) !important;
        }}
        
        [data-testid="stSidebar"] *, [data-testid="stSidebarContent"] * {{
            color: var(--text-color) !important;
        }}
        
        /* UI components */
        button, button[kind="primary"], button[kind="secondary"],
        .stButton>button, .stButton button,
        [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] {{
            background-color: var(--sidebar-color) !important;
            color: var(--text-color) !important;
            border-color: var(--button-border) !important;
            transition: all 0.3s ease;
            border-radius: 6px !important;
        }}
        
        button:hover, .stButton>button:hover {{
            background-color: var(--hover-color) !important;
            border-color: var(--button-border) !important;
        }}
        
        [data-testid="stExpander"] {{
            background-color: var(--expander-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
            border-radius: 8px !important;
            margin-bottom: 1rem !important;
        }}
        
        .stSelectbox [data-baseweb="select"], [data-baseweb="select"],
        .stTextInput input, .stNumberInput input, .stTextArea textarea {{
            background-color: var(--sidebar-color) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
            border-radius: 6px !important;
        }}
        
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
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def _apply_theme_js():
    """Apply JavaScript for theme handling"""
    theme = theme_manager.get_theme()
    is_dark = theme_manager.is_dark_mode()
    
    # Theme colors
    colors = {
        "bg": "black" if is_dark else "white",
        "sidebar": "black" if is_dark else "white",
        "text": "white" if is_dark else "#31333F",
        "border": "#444" if is_dark else "#DDDDDD"
    }
    
    # Simplified JavaScript
    js = f"""
    <script>
        (function() {{
            document.documentElement.setAttribute('theme', '{theme}');
            
            document.documentElement.style.setProperty('--background-color', '{colors["bg"]}');
            document.documentElement.style.setProperty('--sidebar-color', '{colors["sidebar"]}');
            document.documentElement.style.setProperty('--text-color', '{colors["text"]}');
            document.documentElement.style.setProperty('--border-color', '{colors["border"]}');
            
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {{
                const headers = sidebar.querySelectorAll('h1, h2, h3, h4, h5, h6');
                headers.forEach(header => {{
                    header.style.display = 'none';
                }});
            }}
        }})();
    </script>
    """
    
    st.markdown(js, unsafe_allow_html=True)