import streamlit as st
from ui.translator import translator as locale
from ui.translations import translations
from ui.theme_manager import theme_manager
from ui.components.sidebar import render_sidebar
from ui.components.header import render_header
from ui.components.footer import render_footer
import plotly.io as pio

# Import tất cả các trang
from ui.pages.chain_reaction import render_page as chain_reaction_page
from ui.pages.neutron_transport import render_page as neutron_transport_page
from ui.pages.monte_carlo import render_page as monte_carlo_page
from ui.pages.blast_wave import render_page as blast_wave_page
from ui.pages.thermal_radiation import render_page as thermal_radiation_page
from ui.pages.emp_effects import render_page as emp_effects_page
from ui.pages.fallout import render_page as fallout_page
from ui.pages.weapon_design import render_page as weapon_design_page
from ui.pages.flash_effects import render_page as flash_effects_page

def apply_theme():
    """Áp dụng theme dựa vào ThemeManager"""
    # Lấy theme hiện tại từ theme_manager
    current_theme = theme_manager.get_theme()
    has_dark_mode = theme_manager.is_dark_mode()
    
    # Cập nhật dark_mode trong session_state để tương thích ngược
    st.session_state["dark_mode"] = has_dark_mode
    
    # CSS chung cho cả dark và light mode
    st.markdown("""
    <style>
    /* Cho phép nhận diện theme với data-theme */
    :root {
        color-scheme: light dark;
    }
    
    html {
        transition: background-color 0.3s, color 0.3s;
    }
    
    /* Đảm bảo theme được áp dụng ngay cả khi JavaScript chưa tải xong */
    html[data-theme="dark"] {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    html[data-theme="light"] {
        background-color: #FFFFFF;
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Thêm data-theme attribute vào html element
    st.markdown(f"""
    <script>
        // Đặt theme ngay lập tức để tránh nhấp nháy màn hình
        (function() {{
            document.documentElement.setAttribute('data-theme', '{current_theme}');
        }})();
    </script>
    """, unsafe_allow_html=True)
    
    # Kiểm tra theme có phải là dark không
    if has_dark_mode:
        # CSS cho Dark Mode - được áp dụng với mức độ ưu tiên cao nhất
        st.markdown("""
        <style>
        /* CSS cho Dark Mode */
        :root {
            --background-color: #0E1117 !important;
            --secondary-background-color: #262730 !important;
            --text-color: #FAFAFA !important;
            --font-color: #FAFAFA !important;
        }
        
        body, .stApp {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }
        
        p, h1, h2, h3, h4, h5, h6, span, div, label, button, select, option {
            color: var(--text-color) !important;
        }
        
        .stMarkdown, .stMarkdown p, .stMarkdown span {
            color: var(--text-color) !important;
        }
        
        .stSidebar, .stSidebar .sidebar-content {
            background-color: #1E1E1E !important;
        }
        
        .stButton > button {
            background-color: #333333 !important;
            color: #FFFFFF !important;
            border-color: #555555 !important;
        }
        
        .stButton > button:hover {
            background-color: #444444 !important;
            border-color: #777777 !important;
        }
        
        .stExpander {
            background-color: #1E1E1E !important;
            border-color: #333333 !important;
        }
        
        /* Selectbox styling cho dark mode */
        .stSelectbox > div > div {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
            border-color: #333333 !important;
        }
        
        /* Dropdown của selectbox */
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
            border-color: #333333 !important;
        }
        
        /* Items trong dropdown */
        .stSelectbox ul {
            background-color: #1E1E1E !important;
        }
        
        .stSelectbox ul li, .stSelectbox ul div {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        
        .stSelectbox ul li:hover, .stSelectbox ul div:hover {
            background-color: #333333 !important;
        }
        
        /* Icons trong selectbox */
        .stSelectbox svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        
        /* Khi hover vào selectbox */
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #555555 !important;
        }
        
        /* Khi focus vào selectbox */
        .stSelectbox [data-baseweb="select"]:focus-within {
            border-color: rgb(0, 180, 216) !important;
        }
        
        /* Popup menu cho selectbox */
        div[data-baseweb="popover"] {
            background-color: #1E1E1E !important;
            border-color: #333333 !important;
        }
        
        div[data-baseweb="popover"] ul, 
        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] div {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] li:hover, 
        div[data-baseweb="popover"] div[role="option"]:hover {
            background-color: #333333 !important;
        }
        
        div[data-baseweb="popover"] div[role="option"] {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        
        div[data-baseweb="popover"] div[role="option"][aria-selected="true"] {
            background-color: #333333 !important;
        }
        
        /* Header styles cho dark mode */
        .header-container {
            background: linear-gradient(90deg, rgba(0,91,187,0.3) 0%, rgba(0,180,216,0.3) 100%) !important;
        }
        
        .header-title, .breadcrumb {
            color: #FAFAFA !important;
        }
        
        /* Streamlit header toolbar style cho dark mode */
        header[data-testid="stHeader"], .stDeployButton, .stToolbar {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }
        
        .stDeployButton button {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
            border-color: #555555 !important;
        }
        
        /* Đảm bảo các icon trong header có màu phù hợp */
        header[data-testid="stHeader"] button svg, header button {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
        }
        
        /* Nút menu trong streamlit header cho dark mode */
        [data-testid="stHamburgerButton"], [data-testid="baseButton-headerNoPadding"] {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
        }
        
        [data-testid="stHamburgerButton"] svg, [data-testid="baseButton-headerNoPadding"] svg {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
            stroke: var(--text-color) !important;
        }
        
        /* Đảm bảo dropdown menu cũng có màu phù hợp */
        div[data-testid="stDropdownMenu"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
        }
        
        div[data-testid="stDropdownMenu"] button {
            color: var(--text-color) !important;
        }
        
        /* CSS cho menu toolbar (rerun, settings, print) */
        [data-testid="stToolbar"] {
            background-color: var(--background-color) !important;
        }
        
        [data-testid="stToolbar"] button, [data-testid="stToolbar"] button svg {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
        }
        
        /* Menu dropdown chứa Rerun, Settings, Report a bug, etc. */
        ul[class*="menu_"], ul[class*="menu_"] li, ul[class*="menu_"] button {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
        }
        
        ul[class*="menu_"] button svg {
            fill: var(--text-color) !important;
            color: var(--text-color) !important;
        }
        
        ul[class*="menu_"] li:hover, ul[class*="menu_"] button:hover {
            background-color: rgba(128, 128, 128, 0.2) !important;
        }
        
        /* CSS đặc biệt cho menu settings trong dark mode */
        div[data-testid="stSettingsMenu"], 
        div[data-testid="stSettingsMenuContainer"],
        div[data-testid="stSettingsMenuContent"] {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        
        button[kind="settingsButton"] {
            color: #FFFFFF !important;
        }
        
        button[kind="settingsButton"] svg {
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
        }
        
        div[data-testid="stSettingsMenuContainer"] button, 
        div[data-testid="stSettingsMenuContainer"] a,
        div[data-testid="stSettingsMenuContainer"] p,
        div[data-testid="stSettingsMenuContainer"] span,
        div[data-testid="stSettingsMenuContent"] button,
        div[data-testid="stSettingsMenuContent"] a,
        div[data-testid="stSettingsMenuContent"] p,
        div[data-testid="stSettingsMenuContent"] span {
            color: #FFFFFF !important;
        }
        
        /* Màu nền cho menu khi mở */
        div[data-testid="stExpander"] {
            background-color: #1E1E1E !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # CSS cho Light Mode (tùy chọn)
        st.markdown("""
        <style>
        /* CSS cho Light Mode */
        :root {
            --background-color: #FFFFFF !important;
            --secondary-background-color: #F0F2F6 !important;
            --text-color: #333333 !important;
            --font-color: #333333 !important;
        }
        
        body, .stApp {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }
        
        p, h1, h2, h3, h4, h5, h6, span, div, label, button, select, option {
            color: var(--text-color) !important;
        }
        
        /* Header styles cho light mode */
        .header-container {
            background: linear-gradient(90deg, rgba(0,180,216,0.2) 0%, rgba(0,91,187,0.2) 100%) !important;
        }
        
        .header-title, .breadcrumb {
            color: #333333 !important;
        }
        
        /* Streamlit header toolbar style cho light mode */
        header[data-testid="stHeader"], .stDeployButton, .stToolbar {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }
        
        .stDeployButton button {
            background-color: #F0F2F6 !important;
            color: #333333 !important;
            border-color: #E0E0E0 !important;
        }
        
        /* Đảm bảo các icon trong header có màu phù hợp */
        header[data-testid="stHeader"] button svg, header button {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
        }
        
        /* Nút menu trong streamlit header cho light mode */
        [data-testid="stHamburgerButton"], [data-testid="baseButton-headerNoPadding"] {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
        }
        
        [data-testid="stHamburgerButton"] svg, [data-testid="baseButton-headerNoPadding"] svg {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
            stroke: var(--text-color) !important;
        }
        
        /* Đảm bảo dropdown menu cũng có màu phù hợp */
        div[data-testid="stDropdownMenu"] {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
        }
        
        div[data-testid="stDropdownMenu"] button {
            color: var(--text-color) !important;
        }
        
        /* CSS cho menu toolbar (rerun, settings, print) */
        [data-testid="stToolbar"] {
            background-color: var(--background-color) !important;
        }
        
        [data-testid="stToolbar"] button, [data-testid="stToolbar"] button svg {
            color: var(--text-color) !important;
            fill: var(--text-color) !important;
        }
        
        /* Menu dropdown chứa Rerun, Settings, Report a bug, etc. */
        ul[class*="menu_"], ul[class*="menu_"] li, ul[class*="menu_"] button {
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
        }
        
        ul[class*="menu_"] button svg {
            fill: var(--text-color) !important;
            color: var(--text-color) !important;
        }
        
        ul[class*="menu_"] li:hover, ul[class*="menu_"] button:hover {
            background-color: rgba(128, 128, 128, 0.2) !important;
        }
        
        /* CSS đặc biệt cho menu settings trong light mode */
        div[data-testid="stSettingsMenu"], 
        div[data-testid="stSettingsMenuContainer"],
        div[data-testid="stSettingsMenuContent"] {
            background-color: #FFFFFF !important;
            color: #333333 !important;
        }
        
        button[kind="settingsButton"] {
            color: #333333 !important;
        }
        
        button[kind="settingsButton"] svg {
            fill: #333333 !important;
            color: #333333 !important;
        }
        
        div[data-testid="stSettingsMenuContainer"] button, 
        div[data-testid="stSettingsMenuContainer"] a,
        div[data-testid="stSettingsMenuContainer"] p,
        div[data-testid="stSettingsMenuContainer"] span,
        div[data-testid="stSettingsMenuContent"] button,
        div[data-testid="stSettingsMenuContent"] a,
        div[data-testid="stSettingsMenuContent"] p,
        div[data-testid="stSettingsMenuContent"] span {
            color: #333333 !important;
        }
        
        /* Màu nền cho menu khi mở */
        div[data-testid="stExpander"] {
            background-color: #FFFFFF !important;
        }
        
        /* Selectbox styling cho light mode */
        .stSelectbox > div > div {
            background-color: #FFFFFF !important;
            color: #333333 !important;
            border-color: #DDDDDD !important;
        }
        
        /* Dropdown của selectbox */
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #333333 !important;
            border-color: #DDDDDD !important;
        }
        
        /* Items trong dropdown */
        .stSelectbox ul {
            background-color: #FFFFFF !important;
        }
        
        .stSelectbox ul li, .stSelectbox ul div {
            background-color: #FFFFFF !important;
            color: #333333 !important;
        }
        
        .stSelectbox ul li:hover, .stSelectbox ul div:hover {
            background-color: #F0F2F6 !important;
        }
        
        /* Icons trong selectbox */
        .stSelectbox svg {
            color: #333333 !important;
            fill: #333333 !important;
        }
        
        /* Khi hover vào selectbox */
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #BBBBBB !important;
        }
        
        /* Khi focus vào selectbox */
        .stSelectbox [data-baseweb="select"]:focus-within {
            border-color: rgb(0, 91, 187) !important;
        }
        
        /* Popup menu cho selectbox */
        div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border-color: #DDDDDD !important;
        }
        
        div[data-baseweb="popover"] ul, 
        div[data-baseweb="popover"] li,
        div[data-baseweb="popover"] div {
            background-color: #FFFFFF !important;
            color: #333333 !important;
        }
        
        div[data-baseweb="popover"] li:hover, 
        div[data-baseweb="popover"] div[role="option"]:hover {
            background-color: #F0F2F6 !important;
        }
        
        div[data-baseweb="popover"] div[role="option"] {
            background-color: #FFFFFF !important;
            color: #333333 !important;
        }
        
        div[data-baseweb="popover"] div[role="option"][aria-selected="true"] {
            background-color: #F0F2F6 !important;
        }
        </style>
        """, unsafe_allow_html=True)

def run_dashboard():
    # Lấy theme từ URL query params trước khi cấu hình trang
    query_params = st.query_params
    current_theme = query_params.get("theme", ["light"])[0]
    
    # Khởi tạo theme
    if current_theme in ["light", "dark"]:
        theme_manager.set_theme(current_theme)
        # Cập nhật session_state cho tương thích ngược
        st.session_state["dark_mode"] = theme_manager.is_dark_mode()
    
    # Khởi tạo session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = locale.get_text("nav.chain_reaction")
    
    # Bật debug mode bằng query param debug=true
    if "debug" in query_params:
        st.session_state["show_debug"] = True
    
    # Tải bản dịch
    locale.add_translations(translations)
    
    # Thiết lập Streamlit theme dựa trên theme_manager
    # Phải thực hiện TRƯỚC st.set_page_config
    streamlit_theme = "dark" if theme_manager.is_dark_mode() else "light"
    
    # Thiết lập cấu hình trang
    st.set_page_config(
        page_title=locale.get_text("app.page_title"),
        page_icon=locale.get_text("app.icon"),
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get help": locale.get_text("app.menu.get_help"),
            "Report a bug": locale.get_text("app.menu.report_bug"),
            "About": locale.get_text("app.menu.about")
        }
    )
    
    # Thiết lập mặc định global template cho Plotly
    template_name = "plotly_dark" if theme_manager.is_dark_mode() else "plotly_white"
    pio.templates.default = template_name
    
    # Lưu trữ tất cả các tham số URL hiện tại để sử dụng sau này khi tải lại trang
    if "url_params" not in st.session_state:
        st.session_state["url_params"] = {k: v for k, v in query_params.items() if k != "theme"}
    
    # Hiển thị debug chi tiết nếu cần
    if st.session_state.get("show_debug", False):
        st.write(f"Theme from query params: {current_theme}")
        st.write(f"Theme from theme_manager: {theme_manager.get_theme()}")
        st.write(f"Dark mode in session state: {st.session_state.get('dark_mode', False)}")
        if "current_page" in st.session_state:
            st.write(f"Current page: {st.session_state.current_page}")
    
    # Áp dụng theme - phải thực hiện TRƯỚC khi render bất kỳ component nào
    apply_theme()
    
    # Hiển thị sidebar và lấy trang hiện tại
    current_page = render_sidebar()
    
    # Hiển thị trang tương ứng dựa vào current_page
    if current_page == locale.get_text("nav.chain_reaction"):
        chain_reaction_page()
    elif current_page == locale.get_text("nav.neutron_transport"):
        neutron_transport_page()
    elif current_page == locale.get_text("nav.monte_carlo"):
        monte_carlo_page()
    elif current_page == locale.get_text("nav.blast_wave"):
        blast_wave_page()
    elif current_page == locale.get_text("nav.thermal_radiation"):
        thermal_radiation_page()
    elif current_page == locale.get_text("nav.emp_effects"):
        emp_effects_page()
    elif current_page == locale.get_text("nav.fallout"):
        fallout_page()
    elif current_page == locale.get_text("nav.weapon_design"):
        weapon_design_page()
    elif current_page == locale.get_text("nav.flash_effects"):
        flash_effects_page()
    
    # Hiển thị footer
    render_footer()
    
    # Script Javascript đồng bộ theme giữa các trang
    st.markdown("""
    <script>
        // Đồng bộ theme từ localStorage
        (function() {
            // Đọc theme từ localStorage
            var savedTheme = localStorage.getItem('nuclear_sim_theme');
            
            // Nếu có theme đã lưu và khác với theme trong URL, thêm vào URL
            if (savedTheme) {
                var urlParams = new URLSearchParams(window.location.search);
                if (!urlParams.has('theme') || urlParams.get('theme') !== savedTheme) {
                    urlParams.set('theme', savedTheme);
                    window.history.replaceState({}, '', window.location.pathname + '?' + urlParams.toString());
                }
            } else {
                // Nếu không có theme đã lưu, kiểm tra chế độ hệ thống
                var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
                var systemTheme = prefersDark ? 'dark' : 'light';
                
                // Đặt theme vào localStorage
                localStorage.setItem('nuclear_sim_theme', systemTheme);
                
                // Thêm theme vào URL nếu chưa có
                var urlParams = new URLSearchParams(window.location.search);
                if (!urlParams.has('theme')) {
                    urlParams.set('theme', systemTheme);
                    window.history.replaceState({}, '', window.location.pathname + '?' + urlParams.toString());
                }
            }
            
            // Đặt theme attribute cho HTML tag
            document.documentElement.setAttribute('theme', savedTheme || systemTheme || 'light');
            document.documentElement.setAttribute('data-theme', savedTheme || systemTheme || 'light');
        })();
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_dashboard()