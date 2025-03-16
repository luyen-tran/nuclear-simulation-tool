import streamlit as st
import plotly.graph_objects as go
import numpy as np
from ui.theme_manager import theme_manager
import plotly.io as pio

# Định nghĩa bảng màu cho từng theme
DARK_THEME_COLORS = {
    'primary': ['#8dd3c7', '#fdb462', '#bebada', '#fb8072', '#80b1d3', '#b3de69'], 
    'line_colors': {
        'blue': '#80b1d3',
        'red': '#fb8072',
        'green': '#b3de69',
        'purple': '#bebada',
        'orange': '#fdb462'
    }
}

LIGHT_THEME_COLORS = {
    'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
    'line_colors': {
        'blue': '#1f77b4',
        'red': '#d62728',
        'green': '#2ca02c',
        'purple': '#9467bd',
        'orange': '#ff7f0e'
    }
}

def get_color_palette():
    """Lấy bảng màu dựa theo theme hiện tại"""
    if theme_manager.is_dark_mode():
        return DARK_THEME_COLORS
    else:
        return LIGHT_THEME_COLORS

def get_color_for_theme(color_name):
    """Lấy mã màu phù hợp với theme hiện tại"""
    palette = get_color_palette()
    return palette['line_colors'].get(color_name, color_name)

def create_line_chart(x_data, y_data, title, x_label, y_label, color='blue', theme_template=None):
    """Tạo biểu đồ đường đơn giản"""
    fig = go.Figure()
    
    # Luôn lấy template mới nhất từ theme_manager
    theme_template = theme_manager.get_template()
    
    # Lấy màu phù hợp với theme hiện tại
    themed_color = get_color_for_theme(color)
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        line=dict(color=themed_color, width=2)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_template
        
    )
    
    return fig

def create_multi_line_chart(x_data, y_data_dict, title, x_label, y_label, theme_template=None):
    """Tạo biểu đồ nhiều đường"""
    fig = go.Figure()
    
    # Luôn lấy template mới nhất từ theme_manager
    theme_template = theme_manager.get_template()
    
    # Lấy bảng màu theo theme
    palette = get_color_palette()
    colors = palette['primary']
    
    color_idx = 0
    
    for name, y_data in y_data_dict.items():
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines',
            name=name,
            line=dict(color=colors[color_idx % len(colors)], width=2)
        ))
        color_idx += 1
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_template
    )
    
    return fig

def create_heatmap(x_data, y_data, z_data, title, x_label, y_label, theme_template=None):
    """Tạo biểu đồ nhiệt"""
    
    # Luôn lấy template mới nhất từ theme_manager
    theme_template = theme_manager.get_template()
    
    # Chọn colorscale phù hợp với theme
    colorscale = 'Viridis' if theme_manager.is_dark_mode() else 'Jet'
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_data,
        y=y_data,
        colorscale=colorscale
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_template
    )
    
    return fig

def create_3d_surface(x_data, y_data, z_data, title, x_label, y_label, z_label, theme_template=None):
    """Tạo biểu đồ bề mặt 3D"""
    
    # Luôn lấy template mới nhất từ theme_manager
    theme_template = theme_manager.get_template()
    
    # Chọn colorscale phù hợp với theme
    colorscale = 'Viridis' if theme_manager.is_dark_mode() else 'Jet'
    
    fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data, colorscale=colorscale)])
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label
        ),
        template=theme_template
    )
    
    return fig

def update_figure_with_theme(fig):
    """Cập nhật template của biểu đồ theo theme hiện tại
    
    Hàm này nên được gọi ngay trước khi hiển thị biểu đồ với st.plotly_chart
    để đảm bảo template luôn phản ánh theme hiện tại.
    
    Args:
        fig (plotly.graph_objects.Figure): Biểu đồ cần cập nhật
        
    Returns:
        plotly.graph_objects.Figure: Biểu đồ đã cập nhật
    """
    fig.update_layout(template=theme_manager.get_template())
    
    # Thiết lập màu cho title và tiêu đề trục dựa trên theme
    title_color = '#FFFFFF' if theme_manager.is_dark_mode() else '#333333'
    axis_title_color = '#E0E0E0' if theme_manager.is_dark_mode() else '#555555'
    
    # Cập nhật màu cho title và các tiêu đề trục
    fig.update_layout(
        title_font_color=title_color,
        xaxis_title_font_color=axis_title_color,
        yaxis_title_font_color=axis_title_color
    )
    
    # Cập nhật màu cho tiêu đề trục z (nếu có)
    if hasattr(fig, 'layout') and hasattr(fig.layout, 'scene'):
        fig.update_layout(
            scene=dict(
                xaxis_title_font_color=axis_title_color,
                yaxis_title_font_color=axis_title_color,
                zaxis_title_font_color=axis_title_color
            )
        )
    
    # Cập nhật các thuộc tính màu sắc trong fig theo theme hiện tại
    if hasattr(fig, 'data') and fig.data:
        palette = get_color_palette()
        for i, trace in enumerate(fig.data):
            # Cập nhật màu cho các đường (line)
            if trace.type == 'scatter' and hasattr(trace, 'line') and trace.line.color:
                if trace.line.color in ['blue', 'red', 'green', 'purple', 'orange']:
                    trace.line.color = get_color_for_theme(trace.line.color)
            
            # Cập nhật colorscale cho heatmap và surface
            if trace.type in ['heatmap', 'surface']:
                trace.colorscale = 'Viridis' if theme_manager.is_dark_mode() else 'Jet'
    
    return fig

def plotly_chart_with_theme(fig, **kwargs):
    """Wrapper cho hàm st.plotly_chart với cập nhật theme tự động
    
    Hàm này giúp đảm bảo mọi biểu đồ plotly luôn được cập nhật theme
    ngay trước khi hiển thị.
    
    Args:
        fig (plotly.graph_objects.Figure): Biểu đồ cần hiển thị
        **kwargs: Các tham số bổ sung cho st.plotly_chart
    """
    import streamlit as st
    
    # Đảm bảo theme_manager đã cài đặt theme toàn cục
    theme_manager._setup_global_theme()
    
    # Cập nhật biểu đồ với theme hiện tại
    updated_fig = update_figure_with_theme(fig)
    
    # Ghi đè trực tiếp thuộc tính màu sắc theo theme
    updated_fig.update_layout(
        paper_bgcolor='rgba(30, 30, 30, 1)' if theme_manager.is_dark_mode() else 'rgba(255, 255, 255, 1)',
        plot_bgcolor='rgba(40, 40, 40, 1)' if theme_manager.is_dark_mode() else 'rgba(245, 245, 245, 1)'
    )
    
    # Thiết lập tùy chọn cơ bản cho biểu đồ
    kwargs['use_container_width'] = kwargs.get('use_container_width', True)
    kwargs['config'] = kwargs.get('config', {})
    kwargs['config']['displayModeBar'] = kwargs['config'].get('displayModeBar', False)
    
    # Hiển thị biểu đồ
    return st.plotly_chart(updated_fig, **kwargs) 