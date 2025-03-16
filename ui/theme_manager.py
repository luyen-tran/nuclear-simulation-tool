class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "name": "light",
                "display_name": "Sáng"
            },
            "dark": {
                "name": "dark",
                "display_name": "Tối"
            }
        }
        # Áp dụng theme mặc định khi khởi tạo
        self._setup_global_theme()
    
    def set_theme(self, theme_code):
        """Set current theme"""
        if theme_code in self.themes:
            self.current_theme = theme_code
            # Cập nhật theme toàn cục khi theme thay đổi
            self._setup_global_theme()
    
    def get_theme(self):
        """Get current theme"""
        return self.current_theme
    
    def is_dark_mode(self):
        """Check if current theme is dark mode"""
        return self.current_theme == "dark"
    
    def _setup_global_theme(self):
        """Thiết lập theme Plotly toàn cục"""
        import plotly.io as pio
        import plotly.graph_objects as go
        
        # Tạo template hoàn toàn mới
        template = go.layout.Template()
        
        # Tùy chỉnh màu sắc dựa trên theme hiện tại
        if self.is_dark_mode():
            # Dark mode colors
            custom_colors = ['#8dd3c7', '#fdb462', '#bebada', '#fb8072', '#80b1d3', '#b3de69']
            template.layout.update(
                paper_bgcolor='rgba(30, 30, 30, 1)',
                plot_bgcolor='rgba(40, 40, 40, 1)',
                font=dict(color='white'),
                colorway=custom_colors
            )
            
            # Cập nhật màu sắc cho các thành phần biểu đồ trong chế độ tối
            template.layout.xaxis.update(
                gridcolor='rgba(80, 80, 80, 0.3)',
                zerolinecolor='rgba(80, 80, 80, 0.5)'
            )
            template.layout.yaxis.update(
                gridcolor='rgba(80, 80, 80, 0.3)',
                zerolinecolor='rgba(80, 80, 80, 0.5)'
            )
        else:
            # Light mode colors
            custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            template.layout.update(
                paper_bgcolor='rgba(255, 255, 255, 1)',
                plot_bgcolor='rgba(245, 245, 245, 1)',
                font=dict(color='black'),
                colorway=custom_colors
            )
            
            # Cập nhật màu sắc cho các thành phần biểu đồ trong chế độ sáng
            template.layout.xaxis.update(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zerolinecolor='rgba(150, 150, 150, 0.5)'
            )
            template.layout.yaxis.update(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zerolinecolor='rgba(150, 150, 150, 0.5)'
            )
        
        # Cài đặt các thuộc tính chung
        template.layout.update(
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1
            ),
            # Tắt tất cả các tính năng tự động điều chỉnh
            autosize=True,
            hovermode='closest',
            transition_duration=0  # Tắt hiệu ứng chuyển đổi để ngăn theme hệ thống
        )
        
        # Đăng ký template với tên duy nhất cho ứng dụng
        template_name = 'custom_app_template'
        pio.templates[template_name] = template
        
        # Đặt template này làm mặc định và vô hiệu hóa template khác
        pio.templates.default = template_name
    
    def get_template(self):
        """Get plotly template based on current theme"""
        # Đảm bảo template toàn cục đã được cài đặt
        self._setup_global_theme()
        
        import plotly.io as pio
        # Trả về template mặc định hiện tại
        return pio.templates[pio.templates.default]
    
    def get_display_name(self, theme_code=None):
        """Get display name for theme"""
        if theme_code is None:
            theme_code = self.current_theme
        return self.themes.get(theme_code, {}).get("display_name", theme_code)


# Tạo đối tượng singleton
theme_manager = ThemeManager() 