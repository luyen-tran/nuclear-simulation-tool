import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import time
from models.monte_carlo import MonteCarloNeutronTransport as MonteCarloModel
from ui.translator import translator as locale
from ui.theme_manager import theme_manager
from ui.components.header import render_header
from ui.conclusions import get_conclusions
from ui.components.charts import plotly_chart_with_theme

def render_page():
    """Hiển thị trang mô phỏng Monte Carlo cho neutron"""
    
    # Header
    render_header(locale.get_text("monte.header"))
    
    # Main inputs
    col1, col2 = st.columns(2)
    
    with col1:
        radius = st.slider(
            locale.get_text("monte.radius"),
            min_value=1.0,
            max_value=20.0,
            value=8.0,
            step=0.5,
            help=locale.get_text("help.system_radius")
        )
        
        num_neutrons = st.slider(
            locale.get_text("monte.num_neutrons"),
            min_value=100,
            max_value=10000,
            value=2000,
            step=100,
            help=locale.get_text("help.neutron_count")
        )
        
        spatial_distribution = st.selectbox(
            "Initial Distribution",
            options=["Point Source", "Uniform", "Shell"],
            index=1,
            help=locale.get_text("help.initial_distribution")
        )
    
    with col2:
        sigma_f = st.slider(
            locale.get_text("monte.fission"),
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01,
            help=locale.get_text("help.fission_xs")
        )
        
        sigma_s = st.slider(
            locale.get_text("monte.scattering"),
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.01,
            help=locale.get_text("help.scattering_xs")
        )
        
        sigma_a = st.slider(
            locale.get_text("monte.absorption"),
            min_value=0.0,
            max_value=1.0,
            value=0.05,
            step=0.01,
            help=locale.get_text("help.absorption_xs")
        )
    
    # Advanced options in expander
    with st.expander(locale.get_text("monte.advanced_options")):
        col1, col2 = st.columns(2)
        
        with col1:
            nu_bar = st.slider(
                locale.get_text("monte.average_fission_neutrons"),
                min_value=1.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
                help=locale.get_text("help.avg_neutrons")
            )
            
            num_groups = st.slider(
                "Number of Energy Groups",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help=locale.get_text("help.energy_groups")
            )
            
            max_gen = st.slider(
                "Maximum Generations",
                min_value=1,
                max_value=20,
                value=6,
                step=1,
                help=locale.get_text("help.max_generations")
            )
            
            show_progress = st.checkbox(locale.get_text("monte.show_progress"), value=True,
                help=locale.get_text("help.show_progress"))
            
            simulate_chain = st.checkbox(locale.get_text("monte.simulate_fission_chain"), value=True,
                help=locale.get_text("help.simulate_chain"))
            
            use_multiprocessing = st.checkbox("Parallel Processing", value=True,
                help=locale.get_text("help.multi_core"))
    
    # Run simulation button
    if st.button(locale.get_text("monte.button"), key="run_monte_carlo"):
        with st.spinner(locale.get_text("common.calculating")):
            # Record start time
            start_time = time.time()
            
            # Create and run model
            model = MonteCarloModel(
                radius=radius,
                fission_xs=sigma_f,
                scattering_xs=sigma_s,
                absorption_xs=sigma_a,
                fission_neutrons=nu_bar,
                energy_groups=num_groups,
                max_generations=max_gen,
                initial_distribution=spatial_distribution.lower()
            )
            
            # Run simulation
            results = model.simulate_neutrons(
                num_neutrons=num_neutrons,
                show_progress=show_progress,
                fission_chain=simulate_chain,
                use_parallel=use_multiprocessing
            )
            
            # Calculate timing
            execution_time = time.time() - start_time
            
            # Display results
            _display_results(results, execution_time, model)
    
    # Conclusions section
    with st.expander(locale.get_text("conclusions.title"), expanded=True):
        st.markdown(get_conclusions("monte_carlo", locale.current_lang))

def _display_results(results, execution_time, model):
    """Display Monte Carlo simulation results with interactive charts."""
    # Execution time
    st.success(locale.get_text("monte.execution_time", time=execution_time))
    
    # Display k-effective if available
    if 'k_effective' in results and 'k_error' in results:
        k_eff = results['k_effective']
        k_err = results['k_error']
        st.info(locale.get_text("monte.k_effective", value=k_eff, error=k_err))
        
        # Interpret criticality
        if abs(k_eff - 1.0) < 0.1:
            st.warning(locale.get_text("chart.critical"))
        elif k_eff < 0.9:
            st.success(locale.get_text("chart.subcritical"))
        else:
            st.error(locale.get_text("chart.supercritical"))
    
    # Layout for charts
    col1, col2 = st.columns(2)
    
    # Display counts in first column
    with col1:
        # Create summary table
        summary_data = {
            locale.get_text("chart.interaction_type"): [
                locale.get_text("monte.fissions"),
                locale.get_text("monte.absorptions"),
                locale.get_text("monte.escapes")
            ],
            locale.get_text("chart.count"): [
                results['fissions'],
                results['absorptions'],
                results['escapes']
            ]
        }
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True)
        
        # Interactions pie chart
        interaction_labels = [
            locale.get_text("monte.fissions"),
            locale.get_text("monte.absorptions"),
            locale.get_text("monte.escapes"),
            locale.get_text("monte.scattering")
        ]
        
        interaction_values = [
            results['fissions'],
            results['absorptions'],
            results['escapes'],
            # Estimate scattering events as total path length entries minus other interactions
            len(results['path_lengths']) - results['fissions'] - results['absorptions'] - results['escapes']
        ]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=interaction_labels,
            values=interaction_values,
            hole=.3
        )])
        
        fig_pie.update_layout(
            title=locale.get_text("chart.interaction_distribution")
        )
        
        plotly_chart_with_theme(fig_pie, use_container_width=True)
        
        # Neutron path length histogram if available
        if 'path_lengths' in results and len(results['path_lengths']) > 0:
            fig_path = go.Figure()
            
            fig_path.add_trace(go.Histogram(
                x=results['path_lengths'],
                nbinsx=30,
                marker_color='blue'
            ))
            
            fig_path.update_layout(
                title=locale.get_text("chart.path_length_distribution"),
                xaxis_title=locale.get_text("chart.path_length"),
                yaxis_title=locale.get_text("chart.frequency")
            )
            
            plotly_chart_with_theme(fig_path, use_container_width=True)
    
    # Display final positions in second column
    with col2:
        # Final positions histogram
        if 'final_positions' in results and len(results['final_positions']) > 0:
            # Extract radial distances - handle both array of distances and array of positions
            if isinstance(results['final_positions'][0], (list, np.ndarray)):
                radial_positions = np.linalg.norm(results['final_positions'], axis=1)
            else:
                radial_positions = results['final_positions']  # Already distances
            
            fig_pos = go.Figure()
            
            # Histogram of final positions
            fig_pos.add_trace(go.Histogram(
                x=radial_positions,
                nbinsx=30,
                marker_color='green',
                name=locale.get_text("chart.final_position")
            ))
            
            # Add vertical line for system boundary
            fig_pos.add_vline(
                x=model.radius,
                line_dash="dash",
                line_color="red",
                annotation_text=locale.get_text("chart.system_boundary"),
                annotation_position="top right"
            )
            
            fig_pos.update_layout(
                title=locale.get_text("chart.final_position"),
                xaxis_title=locale.get_text("chart.radial_position"),
                yaxis_title=locale.get_text("chart.frequency")
            )
            
            plotly_chart_with_theme(fig_pos, use_container_width=True)
        
        # Generation populations if available
        if 'generation_sizes' in results and len(results['generation_sizes']) > 0:
            fig_gen = go.Figure()
            
            generations = list(range(len(results['generation_sizes'])))
            
            fig_gen.add_trace(go.Bar(
                x=generations,
                y=results['generation_sizes'],
                marker_color='purple'
            ))
            
            fig_gen.update_layout(
                title=locale.get_text("chart.neutron_generation"),
                xaxis_title=locale.get_text("chart.generation"),
                yaxis_title=locale.get_text("chart.neutron_count"),
                xaxis=dict(tickmode='linear')
            )
            
            plotly_chart_with_theme(fig_gen, use_container_width=True) 