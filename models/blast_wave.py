import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

class SedovTaylorModel:
    def __init__(self, energy_kt=20, ambient_density=1.225, gamma=1.4):
        # Convert kt to joules: 1 kt TNT = 4.184e12 J
        self.energy = energy_kt * 4.184e12  
        self.ambient_density = ambient_density  # kg/m³
        self.gamma = gamma  # ratio of specific heats
        
    def blast_radius(self, time):
        """
        Calculate blast wave radius using Sedov-Taylor solution
        R(t) = β·(E·t²/ρ)^(1/5)
        """
        beta = 1.15  # dimensionless constant for spherical blast
        return beta * (self.energy * time**2 / self.ambient_density)**(1/5)
    
    def overpressure(self, distance, time):
        """Calculate overpressure at distance and time"""
        R = self.blast_radius(time)
        if distance > R:
            return 0.0
        
        # Improved overpressure calculation with more realistic pressure profile
        shock_pressure = 0.75 * self.ambient_density * (R / time)**2 / self.gamma
        
        # Using modified Friedlander waveform for more realistic pressure decay
        rel_distance = distance / R
        if rel_distance > 0.95:  # Near the shock front
            return shock_pressure * (1 - rel_distance/0.95)
        else:
            # Exponential decay behind the shock front
            tau = 0.5  # Characteristic decay time
            return shock_pressure * (1 - rel_distance) * np.exp(-rel_distance/tau)
    
    def simulate_blast_wave(self, max_distance=10000, times=None):
        """Simulate blast wave propagation"""
        if times is None:
            times = np.linspace(0.1, 30.0, 100)  # seconds
            
        distances = np.linspace(0, max_distance, 200)  # meters
        
        radius_values = [self.blast_radius(t) for t in times]
        
        # Create a grid of distances and times
        pressures = np.zeros((len(distances), len(times)))
        
        for i, distance in enumerate(distances):
            for j, time in enumerate(times):
                pressures[i, j] = self.overpressure(distance, time)
                
        return {
            'times': times,
            'distances': distances,
            'radius': radius_values,
            'pressures': pressures
        }
    
    def damage_assessment(self, overpressure):
        """
        Assess damage based on overpressure levels (in Pa)
        Returns dictionary of damage descriptions with boolean values
        """
        # Standard damage thresholds based on nuclear weapons effects research
        damage_levels = {
            3000: "Light damage to structures (windows break)",
            7000: "Moderate damage to reinforced structures",
            15000: "Most residential buildings collapse",
            35000: "Reinforced concrete structures severely damaged",
            70000: "Complete destruction of most buildings"
        }
        
        result = {}
        for threshold, description in sorted(damage_levels.items()):
            result[description] = (overpressure >= threshold)
        
        return result
    
    def calculate_effects(self, distance, energy_kt=None):
        """
        Calculate various effects at given distance
        
        Returns dict with:
        - max_overpressure: Maximum overpressure (Pa)
        - arrival_time: Time of blast arrival (s)
        - dynamic_pressure: Peak dynamic pressure (Pa)
        - wind_speed: Peak wind speed (m/s)
        - thermal_radiation: Thermal radiation (J/m²)
        """
        if energy_kt is None:
            energy_kt = self.energy / 4.184e12
        
        # Find when blast reaches this distance
        def distance_diff(t):
            return self.blast_radius(t) - distance
        
        # Solve for arrival time (when radius = distance)
        try:
            result = root_scalar(distance_diff, bracket=[0.1, 100])
            arrival_time = result.root if result.converged else None
        except:
            arrival_time = None
        
        if arrival_time is None or arrival_time <= 0:
            return {
                'max_overpressure': 0,
                'arrival_time': float('inf'),
                'dynamic_pressure': 0,
                'wind_speed': 0,
                'thermal_radiation': 0
            }
        
        # Calculate peak overpressure
        max_overpressure = self.overpressure(distance, arrival_time)
        
        # Calculate dynamic pressure and wind speed
        shock_velocity = self.blast_radius(arrival_time) / arrival_time
        wind_speed = 2 * shock_velocity / (self.gamma + 1)  # From Rankine-Hugoniot relations
        dynamic_pressure = 0.5 * self.ambient_density * wind_speed**2
        
        # Simple thermal radiation model (very approximate)
        # About 35% of energy goes to thermal radiation in air bursts
        thermal_factor = 0.35
        thermal_radiation = thermal_factor * self.energy / (4 * np.pi * distance**2)
        
        return {
            'max_overpressure': max_overpressure,
            'arrival_time': arrival_time,
            'dynamic_pressure': dynamic_pressure,
            'wind_speed': wind_speed,
            'thermal_radiation': thermal_radiation
        }
    
    def visualize_blast_wave(self, simulation_data, time_index=None, show_damage=True):
        """
        Visualize blast wave propagation
        
        Args:
            simulation_data: Output from simulate_blast_wave()
            time_index: Index of time point to visualize (None for all)
            show_damage: Whether to show damage thresholds
        """
        times = simulation_data['times']
        distances = simulation_data['distances']
        pressures = simulation_data['pressures']
        
        if time_index is not None:
            # Plot pressure vs distance for specific time
            plt.figure(figsize=(10, 6))
            plt.plot(distances, pressures[:, time_index])
            plt.title(f'Blast Wave Pressure at t={times[time_index]:.2f}s')
            plt.xlabel('Distance (m)')
            plt.ylabel('Overpressure (Pa)')
            plt.grid(True)
            
            # Mark damage thresholds
            if show_damage:
                thresholds = [(3000, 'Window breakage'), 
                             (7000, 'Moderate structural damage'),
                             (15000, 'Building collapse'),
                             (35000, 'Concrete damage')]
                for threshold, label in thresholds:
                    plt.axhline(y=threshold, color='r', linestyle='--', alpha=0.7)
                    plt.text(distances[-1]*0.8, threshold*1.1, label)
                
        else:
            # Create contour plot of pressure over distance and time
            plt.figure(figsize=(12, 8))
            X, Y = np.meshgrid(times, distances)
            
            # Use log scale for better visualization
            levels = np.logspace(2, 6, 20)
            contour = plt.contourf(X, Y, pressures, levels=levels, 
                                   cmap='hot', norm=plt.cm.colors.LogNorm())
            
            # Add shock front line
            plt.plot(times, simulation_data['radius'], 'w--', linewidth=2, 
                    label='Shock front')
            
            plt.colorbar(contour, label='Overpressure (Pa)')
            plt.title('Blast Wave Propagation')
            plt.xlabel('Time (s)')
            plt.ylabel('Distance (m)')
            plt.legend()
            
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, distances=[1000, 2000, 5000, 10000]):
        """Generate a detailed damage report for specified distances"""
        print(f"Nuclear Blast Analysis Report ({self.energy/4.184e12:.1f} kt yield)")
        print("-" * 50)
        
        for distance in distances:
            effects = self.calculate_effects(distance)
            
            print(f"\nAt {distance/1000:.1f} km from ground zero:")
            print(f"  Blast arrival: {effects['arrival_time']:.2f} seconds")
            print(f"  Peak overpressure: {effects['max_overpressure']/1000:.2f} kPa")
            print(f"  Peak wind speed: {effects['wind_speed']:.1f} m/s ({effects['wind_speed']*3.6:.1f} km/h)")
            print(f"  Thermal radiation: {effects['thermal_radiation']/1000:.1f} kJ/m²")
            
            # Damage assessment
            damage = self.damage_assessment(effects['max_overpressure'])
            print("  Damage assessment:")
            damage_found = False
            for description, is_damaged in damage.items():
                if is_damaged:
                    print(f"    - {description}")
                    damage_found = True
            
            if not damage_found:
                print("    - No significant structural damage")
            
        print("\nNote: This simulation uses the Sedov-Taylor blast wave model and")
        print("provides approximate results for educational purposes only.")