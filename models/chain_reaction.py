import numpy as np
from scipy.integrate import solve_ivp

class ChainReactionModel:
    def __init__(self, fission_cross_section=1.0, neutron_speed=2200, 
                 uranium_density=19.1, enrichment=0.85):
        self.fission_cross_section = fission_cross_section  # barns
        self.neutron_speed = neutron_speed  # m/s
        self.uranium_density = uranium_density  # g/cm³
        self.enrichment = enrichment  # fraction of U-235
        
    def calculate_critical_mass(self, geometry="sphere"):
        """Calculate critical mass based on geometry"""
        # Simplified critical mass calculation
        if geometry == "sphere":
            # Spherical critical mass approximation
            return 52 / (self.enrichment ** 2) * (1 - self.enrichment) ** 1.5
        elif geometry == "cylinder":
            # Cylinder approximation
            return 62 / (self.enrichment ** 2) * (1 - self.enrichment) ** 1.5
        else:
            return 75 / (self.enrichment ** 2) * (1 - self.enrichment) ** 1.5
    
    def simulate_chain_reaction(self, initial_neutrons=1, 
                               mass_ratio=1.5, time_span=(0, 0.001), 
                               time_steps=1000):
        """Simulate neutron population in chain reaction"""
        # mass_ratio is the ratio to critical mass
        
        def neutron_growth(t, n):
            # Growth rate depends on how far above critical mass
            k = 2.5  # neutrons per fission
            tau = 10e-8  # average neutron lifetime in seconds
            reactivity = (mass_ratio - 1.0) / mass_ratio
            return (k * reactivity - 1) * n / tau
        
        t_eval = np.linspace(time_span[0], time_span[1], time_steps)
        solution = solve_ivp(neutron_growth, time_span, [initial_neutrons], 
                             t_eval=t_eval)
        
        return solution.t, solution.y[0]