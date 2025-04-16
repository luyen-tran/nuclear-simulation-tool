import streamlit as st
import plotly.graph_objects as go
import numpy as np
from ui.theme_manager import theme_manager
import plotly.io as pio

# Theme color definitions
DARK_THEME_COLORS = {
    'primary': ['#8dd3c7', '#fdb462', '#bebada', '#fb8072', '#80b1d3', '#b3de69'], 
    'line_colors': {
        'blue': '#80b1d3',
        'red': '#fb8072',
        'green': '#b3de69',
        'purple': '#bebada',
        'orange': '#fdb462'
    },
    'background': {
        'paper': 'rgba(30, 30, 30, 1)',
        'plot': 'rgba(40, 40, 40, 1)'
    },
    'text': {
        'title': '#FFFFFF',
        'axis': '#E0E0E0'
    },
    'colorscale': 'Viridis'
}

LIGHT_THEME_COLORS = {
    'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
    'line_colors': {
        'blue': '#1f77b4',
        'red': '#d62728',
        'green': '#2ca02c',
        'purple': '#9467bd',
        'orange': '#ff7f0e'
    },
    'background': {
        'paper': 'rgba(255, 255, 255, 1)',
        'plot': 'rgba(245, 245, 245, 1)'
    },
    'text': {
        'title': '#333333',
        'axis': '#555555'
    },
    'colorscale': 'Jet'
}

class ChartThemeManager:
    @staticmethod
    def get_color_palette():
        """Get color palette based on current theme"""
        return DARK_THEME_COLORS if theme_manager.is_dark_mode() else LIGHT_THEME_COLORS
    
    @staticmethod
    def get_color_for_theme(color_name):
        """Get appropriate color code for current theme"""
        palette = ChartThemeManager.get_color_palette()
        return palette['line_colors'].get(color_name, color_name)
    
    @staticmethod
    def get_colorscale():
        """Get appropriate colorscale for current theme"""
        palette = ChartThemeManager.get_color_palette()
        return palette['colorscale']
    
    @staticmethod
    def apply_theme_to_figure(fig):
        """Apply current theme to figure"""
        palette = ChartThemeManager.get_color_palette()
        
        # Apply template from theme manager
        fig.update_layout(template=theme_manager.get_template())
        
        # Apply colors based on theme
        fig.update_layout(
            title_font_color=palette['text']['title'],
            xaxis_title_font_color=palette['text']['axis'],
            yaxis_title_font_color=palette['text']['axis'],
            paper_bgcolor=palette['background']['paper'],
            plot_bgcolor=palette['background']['plot']
        )
        
        # Handle 3D charts
        if hasattr(fig.layout, 'scene'):
            fig.update_layout(
                scene=dict(
                    xaxis_title_font_color=palette['text']['axis'],
                    yaxis_title_font_color=palette['text']['axis'],
                    zaxis_title_font_color=palette['text']['axis']
                )
            )
        
        # Update trace colors
        if hasattr(fig, 'data') and fig.data:
            for trace in fig.data:
                # Update line colors
                if trace.type == 'scatter' and hasattr(trace, 'line') and trace.line.color:
                    if trace.line.color in palette['line_colors']:
                        trace.line.color = ChartThemeManager.get_color_for_theme(trace.line.color)
                
                # Update colorscale for heatmap and surface
                if trace.type in ['heatmap', 'surface']:
                    trace.colorscale = ChartThemeManager.get_colorscale()
        
        return fig

class ChartBuilder:
    @staticmethod
    def create_base_figure(title, x_label, y_label):
        """Create base figure with common properties"""
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template=theme_manager.get_template()
        )
        return fig
    
    @staticmethod
    def line_chart(x_data, y_data, title, x_label, y_label, color='blue'):
        """Create simple line chart"""
        fig = ChartBuilder.create_base_figure(title, x_label, y_label)
        
        themed_color = ChartThemeManager.get_color_for_theme(color)
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines',
            line=dict(color=themed_color, width=2)
        ))
        
        return fig
    
    @staticmethod
    def multi_line_chart(x_data, y_data_dict, title, x_label, y_label):
        """Create multi-line chart"""
        fig = ChartBuilder.create_base_figure(title, x_label, y_label)
        
        palette = ChartThemeManager.get_color_palette()
        colors = palette['primary']
        
        for i, (name, y_data) in enumerate(y_data_dict.items()):
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines',
                name=name,
                line=dict(color=colors[i % len(colors)], width=2)
            ))
        
        return fig
    
    @staticmethod
    def heatmap(x_data, y_data, z_data, title, x_label, y_label):
        """Create heatmap chart"""
        fig = ChartBuilder.create_base_figure(title, x_label, y_label)
        
        colorscale = ChartThemeManager.get_colorscale()
        
        fig.add_trace(go.Heatmap(
            z=z_data,
            x=x_data,
            y=y_data,
            colorscale=colorscale
        ))
        
        return fig
    
    @staticmethod
    def surface_3d(x_data, y_data, z_data, title, x_label, y_label, z_label):
        """Create 3D surface chart"""
        fig = go.Figure()
        
        colorscale = ChartThemeManager.get_colorscale()
        
        fig.add_trace(go.Surface(
            z=z_data,
            x=x_data,
            y=y_data,
            colorscale=colorscale
        ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=x_label,
                yaxis_title=y_label,
                zaxis_title=z_label
            ),
            template=theme_manager.get_template()
        )
        
        return fig

# Legacy function names for backward compatibility
def get_color_palette():
    """Get color palette based on current theme"""
    return ChartThemeManager.get_color_palette()

def get_color_for_theme(color_name):
    """Get appropriate color code for current theme"""
    return ChartThemeManager.get_color_for_theme(color_name)

def create_line_chart(x_data, y_data, title, x_label, y_label, color='blue', theme_template=None):
    """Create simple line chart"""
    return ChartBuilder.line_chart(x_data, y_data, title, x_label, y_label, color)

def create_multi_line_chart(x_data, y_data_dict, title, x_label, y_label, theme_template=None):
    """Create multi-line chart"""
    return ChartBuilder.multi_line_chart(x_data, y_data_dict, title, x_label, y_label)

def create_heatmap(x_data, y_data, z_data, title, x_label, y_label, theme_template=None):
    """Create heatmap chart"""
    return ChartBuilder.heatmap(x_data, y_data, z_data, title, x_label, y_label)

def create_3d_surface(x_data, y_data, z_data, title, x_label, y_label, z_label, theme_template=None):
    """Create 3D surface chart"""
    return ChartBuilder.surface_3d(x_data, y_data, z_data, title, x_label, y_label, z_label)

def update_figure_with_theme(fig):
    """Update figure with current theme"""
    return ChartThemeManager.apply_theme_to_figure(fig)

def plotly_chart_with_theme(fig, **kwargs):
    """Wrapper for st.plotly_chart with automatic theme update"""
    # Ensure theme_manager has set up global theme
    theme_manager._setup_global_theme()
    
    # Update figure with current theme
    updated_fig = ChartThemeManager.apply_theme_to_figure(fig)
    
    # Set default options for chart
    kwargs['use_container_width'] = kwargs.get('use_container_width', True)
    kwargs['config'] = kwargs.get('config', {})
    kwargs['config']['displayModeBar'] = kwargs['config'].get('displayModeBar', False)
    
    # Display chart
    return st.plotly_chart(updated_fig, **kwargs) 