import numpy as np
from scipy.special import erf

class ThermalRadiationModel:
    def __init__(self, yield_kt=20, burst_height=0):
        self.yield_kt = yield_kt  # yield in kilotons
        self.burst_height = burst_height  # height of burst in meters
        
        # Constants for thermal radiation
        self.thermal_fraction = 0.35  # fraction of energy as thermal radiation
        self.total_energy = yield_kt * 4.184e12  # total energy in joules
        self.thermal_energy = self.thermal_fraction * self.total_energy
        
    def calculate_thermal_energy_density(self, distance):
        """Calculate thermal energy density at given distance"""
        # Simple inverse square law with atmospheric transmission
        transmission = np.exp(-0.01 * distance)  # simplified atmospheric attenuation
        
        # Account for burst height using slant range
        if self.burst_height > 0:
            slant_range = np.sqrt(distance**2 + self.burst_height**2)
        else:
            slant_range = distance
            
        # Energy per unit area
        energy_density = self.thermal_energy / (4 * np.pi * slant_range**2) * transmission
        return energy_density
    
    def calculate_thermal_effects(self, distances):
        """Calculate thermal effects at various distances"""
        energy_densities = np.array([self.calculate_thermal_energy_density(d) for d in distances])
        
        # Convert energy densities to effects
        # Thresholds in J/m²
        first_degree_burn = 2e5
        second_degree_burn = 4e5
        third_degree_burn = 6e5
        
        # Calculate probabilities of effects (using error function for smooth transition)
        p_first_degree = 0.5 * (1 + erf((energy_densities - first_degree_burn) / (0.2 * first_degree_burn)))
        p_second_degree = 0.5 * (1 + erf((energy_densities - second_degree_burn) / (0.2 * second_degree_burn)))
        p_third_degree = 0.5 * (1 + erf((energy_densities - third_degree_burn) / (0.2 * third_degree_burn)))
        
        return {
            'distances': distances,
            'energy_density': energy_densities,
            'first_degree_burn_probability': p_first_degree,
            'second_degree_burn_probability': p_second_degree,
            'third_degree_burn_probability': p_third_degree
        }