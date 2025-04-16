import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from models.monte_carlo import MonteCarloNeutronTransport
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng Monte Carlo cho neutron"""
    
    # Header
    render_header(locale.get_text("monte.header"))
    
    # Các thông số đầu vào
    col1, col2 = st.columns(2)
    
    with col1:
        radius = st.slider(
            locale.get_text("monte.radius"),
            min_value=1.0,
            max_value=30.0,
            value=10.0,
            step=1.0,
            help="Bán kính của hệ thống tính bằng cm"
        )
        
        num_neutrons = st.slider(
            locale.get_text("monte.num_neutrons"),
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Số lượng neutron để mô phỏng"
        )
        
        initial_distribution = st.selectbox(
            "Phân bố ban đầu của neutron",
            options=["point", "uniform", "gaussian"],
            index=0,
            format_func=lambda x: {
                "point": "Tại tâm (điểm)",
                "uniform": "Đồng đều trong hệ thống", 
                "gaussian": "Gaussian xung quanh tâm"
            }.get(x, x),
            help="Phân bố không gian ban đầu của neutron"
        )
    
    with col2:
        fission_xs = st.slider(
            locale.get_text("monte.fission"),
            min_value=0.01,
            max_value=0.5,
            value=0.05,
            step=0.01,
            help="Tiết diện phân hạch"
        )
        
        scattering_xs = st.slider(
            locale.get_text("monte.scattering"),
            min_value=0.05,
            max_value=1.0,
            value=0.2,
            step=0.05,
            help="Tiết diện tán xạ"
        )
        
        absorption_xs = st.slider(
            locale.get_text("monte.absorption"),
            min_value=0.001,
            max_value=0.1,
            value=0.01,
            step=0.001,
            help="Tiết diện hấp thụ"
        )
    
    # Tùy chọn nâng cao
    with st.expander(locale.get_text("monte.advanced_options"), expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            fission_neutrons = st.slider(
                locale.get_text("monte.average_fission_neutrons"),
                min_value=1.0,
                max_value=5.0,
                value=2.43,
                step=0.01,
                help="Số neutron trung bình sinh ra từ mỗi phản ứng phân hạch"
            )
            
            energy_groups = st.slider(
                "Số nhóm năng lượng",
                min_value=1,
                max_value=7,
                value=1,
                step=1,
                help="Số nhóm năng lượng cho tính toán đa nhóm (1 = một nhóm)"
            )
            
            max_generations = st.slider(
                "Số thế hệ tối đa",
                min_value=5,
                max_value=50,
                value=20,
                step=5,
                help="Số thế hệ tối đa cho mô phỏng chuỗi phân hạch"
            )
        
        with col2:
            show_progress = st.checkbox(locale.get_text("monte.show_progress"), value=True,
                                       help="Hiển thị thanh tiến trình trong quá trình mô phỏng")
            
            fission_chain = st.checkbox(locale.get_text("monte.simulate_fission_chain"), value=True,
                                       help="Mô phỏng chuỗi phản ứng phân hạch để tính hệ số nhân neutron k-hiệu quả")
            
            use_parallel = st.checkbox("Sử dụng tính toán song song", value=False,
                                      help="Tăng tốc mô phỏng bằng cách sử dụng nhiều lõi CPU")
            
            if use_parallel:
                import multiprocessing as mp
                max_cores = mp.cpu_count()
                n_cores = st.slider("Số lõi CPU sử dụng", 
                                  min_value=1, 
                                  max_value=max_cores, 
                                  value=max(1, max_cores-1),
                                  help=f"Hệ thống của bạn có {max_cores} lõi CPU")
            else:
                n_cores = None
    
    # Chạy mô phỏng
    if st.button(locale.get_text("monte.button"), type="primary", use_container_width=True):
        with st.spinner("Đang chạy mô phỏng Monte Carlo..."):
            # Tạo model
            model = MonteCarloNeutronTransport(
                radius=radius,
                fission_xs=fission_xs,
                scattering_xs=scattering_xs,
                absorption_xs=absorption_xs,
                fission_neutrons=fission_neutrons,
                energy_groups=energy_groups,
                max_generations=max_generations,
                initial_distribution=initial_distribution
            )
            
            # Chạy mô phỏng
            results = model.simulate_neutrons(
                num_neutrons=num_neutrons,
                show_progress=show_progress,
                fission_chain=fission_chain,
                use_parallel=use_parallel,
                n_cores=n_cores
            )
            
            # Hiển thị thời gian chạy và thông tin
            st.info(locale.get_text("monte.execution_time", time=results['elapsed_time']))
            
            # Hiển thị tóm tắt thống kê
            st.subheader("Tóm tắt kết quả")
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Tổng số tương tác", 
                         value=results['fissions'] + results['absorptions'] + results['escapes'])
            with stats_col2:
                if 'max_generation' in results:
                    st.metric("Số thế hệ mô phỏng", value=results['max_generation'])
            with stats_col3:
                if results['k_effective'] is not None:
                    k_status = "🟢 Gần tới hạn"
                    if results['k_effective'] < 0.95:
                        k_status = "🔵 Dưới tới hạn"
                    elif results['k_effective'] > 1.05:
                        k_status = "🔴 Trên tới hạn"
                    st.metric("Trạng thái hệ thống", value=k_status)
            
            # Tạo biểu đồ phân bố tương tác
            interaction_counts = [results['fissions'], results['absorptions'], results['escapes']]
            interaction_labels = [locale.get_text("monte.fissions"), 
                                 locale.get_text("monte.absorptions"), 
                                 locale.get_text("monte.escapes")]
            
            fig1 = px.bar(
                x=interaction_labels,
                y=interaction_counts,
                color=interaction_labels,
                title=locale.get_text("chart.interaction_distribution")
            )
            
            fig1.update_layout(
                xaxis_title=locale.get_text("chart.interaction_type"),
                yaxis_title=locale.get_text("chart.count"),
                template=theme_manager.get_template()
            )
            
            plotly_chart_with_theme(fig1, use_container_width=True)
            
            # Tạo biểu đồ phân bố đường đi
            fig2 = px.histogram(
                results['path_lengths'],
                nbins=50,
                title=locale.get_text("chart.path_length_distribution"),
                color_discrete_sequence=['green']
            )
            
            fig2.update_layout(
                xaxis_title=locale.get_text("chart.path_length"),
                yaxis_title=locale.get_text("chart.frequency"),
                template=theme_manager.get_template()
            )
            
            # Biểu đồ vị trí cuối cùng
            fig3 = px.histogram(
                results['final_positions'],
                nbins=50,
                title=locale.get_text("chart.final_position"),
                color_discrete_sequence=['purple']
            )
            
            fig3.update_layout(
                xaxis_title=locale.get_text("chart.radial_position"),
                yaxis_title=locale.get_text("chart.frequency"),
                template=theme_manager.get_template()
            )
            
            # Thêm đường ranh giới hệ thống
            fig3.add_vline(x=radius, line_dash="dash", line_color="red",
                          annotation_text=locale.get_text("chart.system_boundary"))
            
            # Hiển thị hai biểu đồ trong một hàng
            col1, col2 = st.columns(2)
            with col1:
                plotly_chart_with_theme(fig2, use_container_width=True)
            with col2:
                plotly_chart_with_theme(fig3, use_container_width=True)
            
            # Kiểm tra và hiển thị kết quả tính toán k-hiệu quả
            if results['k_effective'] is not None:
                st.subheader(locale.get_text("monte.k_effective", value=results['k_effective'], error=results['k_error']))
                
                # Biểu đồ quần thể neutron theo thế hệ
                gen_fig = go.Figure()
                gen_fig.add_trace(go.Scatter(
                    x=list(range(len(results['generation_sizes']))),
                    y=results['generation_sizes'],
                    mode='lines+markers',
                    line=dict(color='blue', width=2)
                ))
                
                gen_fig.update_layout(
                    title=locale.get_text("chart.neutron_generation"),
                    xaxis_title=locale.get_text("chart.generation"),
                    yaxis_title=locale.get_text("chart.neutron_count"),
                    template=theme_manager.get_template()
                )
                
                plotly_chart_with_theme(gen_fig, use_container_width=True)
                
                # Hiển thị trạng thái hệ thống
                if results['k_effective'] < 0.95:
                    st.error(locale.get_text("chart.subcritical"))
                elif results['k_effective'] > 1.05:
                    st.warning(locale.get_text("chart.supercritical"))
                else:
                    st.success(locale.get_text("chart.critical"))
                
                # Hiển thị thông tin hội tụ
                if 'max_generation' in results and results['max_generation'] < max_generations:
                    st.success(f"Mô phỏng đã hội tụ sau {results['max_generation']} thế hệ.")
                    
            # Nếu sử dụng tính toán đa nhóm, hiển thị phân tích phổ năng lượng
            if energy_groups > 1:
                st.subheader("Phân tích phổ năng lượng")
                
                # Tạo biểu đồ cho phổ năng lượng
                energy_fig = go.Figure()
                
                # Giả định các nhóm năng lượng theo thứ tự giảm dần
                energy_boundaries = np.logspace(1, -5, energy_groups + 1)  # Từ 10 MeV đến 0.00001 MeV
                group_names = [f"Nhóm {i+1}<br>({energy_boundaries[i]:.2e}-{energy_boundaries[i+1]:.2e} MeV)" 
                              for i in range(energy_groups)]
                
                # Vẽ tiết diện theo nhóm năng lượng
                x = list(range(energy_groups))
                
                energy_fig.add_trace(go.Bar(
                    x=x, 
                    y=model.fission_xs if isinstance(model.fission_xs, np.ndarray) else [model.fission_xs] * energy_groups,
                    name='Tiết diện phân hạch',
                    marker_color='red'
                ))
                
                energy_fig.add_trace(go.Bar(
                    x=x, 
                    y=model.scattering_xs if isinstance(model.scattering_xs, np.ndarray) else [model.scattering_xs] * energy_groups,
                    name='Tiết diện tán xạ',
                    marker_color='blue'
                ))
                
                energy_fig.add_trace(go.Bar(
                    x=x, 
                    y=model.absorption_xs if isinstance(model.absorption_xs, np.ndarray) else [model.absorption_xs] * energy_groups,
                    name='Tiết diện hấp thụ',
                    marker_color='green'
                ))
                
                energy_fig.update_layout(
                    title="Phân tích tiết diện theo nhóm năng lượng",
                    xaxis_title="Nhóm năng lượng",
                    yaxis_title="Tiết diện (cm⁻¹)",
                    barmode='group',
                    xaxis=dict(
                        tickmode='array',
                        tickvals=x,
                        ticktext=group_names
                    ),
                    template=theme_manager.get_template()
                )
                
                plotly_chart_with_theme(energy_fig, use_container_width=True)
                
                st.info("Trong tính toán đa nhóm, nhóm 1 tương ứng với năng lượng cao nhất và giảm dần theo số thứ tự nhóm")
    
    # Phần kết luận khoa học
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("monte_carlo", locale.current_lang)) 