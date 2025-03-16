import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

class MonteCarloNeutronTransport:
    def __init__(self, radius=10.0, 
                 fission_xs=0.05, scattering_xs=0.2, absorption_xs=0.01,
                 fission_neutrons=2.43, energy_groups=1):
        """
        Enhanced Monte Carlo neutron transport simulation.
        
        Parameters:
        -----------
        radius : float
            Radius of spherical geometry in cm
        fission_xs : float or array
            Fission cross section in cm^-1 (energy-dependent if array)
        scattering_xs : float or array
            Scattering cross section in cm^-1
        absorption_xs : float or array
            Absorption cross section in cm^-1
        fission_neutrons : float
            Average number of neutrons produced per fission
        energy_groups : int
            Number of energy groups for multi-group calculation
        """
        self.radius = radius
        self.energy_groups = energy_groups
        self.fission_neutrons = fission_neutrons
        
        # Handle energy-dependent cross sections
        if energy_groups > 1:
            # Convert to arrays if not already
            self.fission_xs = np.atleast_1d(fission_xs)
            self.scattering_xs = np.atleast_1d(scattering_xs)
            self.absorption_xs = np.atleast_1d(absorption_xs)
        else:
            self.fission_xs = fission_xs
            self.scattering_xs = scattering_xs
            self.absorption_xs = absorption_xs
            
        self.total_xs = self.fission_xs + self.scattering_xs + self.absorption_xs
        
    def _get_cross_sections(self, energy_group=0):
        """Get cross sections for a specific energy group"""
        if self.energy_groups > 1:
            fission = self.fission_xs[energy_group]
            scatter = self.scattering_xs[energy_group]
            absorb = self.absorption_xs[energy_group]
            total = self.total_xs[energy_group]
        else:
            fission = self.fission_xs
            scatter = self.scattering_xs
            absorb = self.absorption_xs
            total = self.total_xs
        
        return fission, scatter, absorb, total
    
    def _sample_direction(self, isotropic=True):
        """Sample a random direction in 3D space"""
        if isotropic:
            theta = np.arccos(2*np.random.random() - 1)
            phi = 2 * np.pi * np.random.random()
            direction = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])
        else:
            # Could implement anisotropic scattering here
            pass
        
        return direction
        
    def simulate_neutrons(self, num_neutrons=1000, max_interactions=100, 
                          show_progress=True, fission_chain=True):
        """
        Monte Carlo simulation of neutron transport
        
        Parameters:
        -----------
        num_neutrons : int
            Initial number of neutrons to simulate
        max_interactions : int
            Maximum number of interactions per neutron history
        show_progress : bool
            Whether to show a progress bar
        fission_chain : bool
            Whether to simulate fission chains (k-effective calculation)
        
        Returns:
        --------
        dict : Results of the simulation
        """
        # Arrays to track results
        n_fissions = 0
        n_absorptions = 0
        n_escapes = 0
        path_lengths = []
        final_positions = []
        
        # For criticality calculations
        generation_sizes = [num_neutrons]
        fission_sites = []
        
        # Neutrons to simulate (may grow with fission)
        neutrons = [{'pos': np.array([0.0, 0.0, 0.0]), 
                     'energy_group': 0} for _ in range(num_neutrons)]
        
        generation = 0
        start_time = time.time()
        
        while neutrons and generation < 10:  # Limit to 10 generations
            generation += 1
            next_gen_neutrons = []
            
            # Track this generation
            if show_progress:
                iterator = tqdm(neutrons, desc=f"Generation {generation}, neutrons: {len(neutrons)}")
            else:
                iterator = neutrons
                
            for neutron in iterator:
                pos = neutron['pos']
                energy_group = neutron['energy_group']
                alive = True
                interactions = 0
                
                while alive and interactions < max_interactions:
                    # Get cross sections for current energy group
                    fission_xs, scatter_xs, absorb_xs, total_xs = self._get_cross_sections(energy_group)
                    
                    # Sample mean free path
                    mfp = -np.log(np.random.random()) / total_xs
                    path_lengths.append(mfp)
                    
                    # Random direction
                    direction = self._sample_direction()
                    
                    # Move neutron
                    pos = pos + mfp * direction
                    
                    # Check if neutron has escaped
                    if np.linalg.norm(pos) > self.radius:
                        n_escapes += 1
                        alive = False
                        continue
                    
                    # Determine interaction type
                    interaction_type = np.random.random() * total_xs
                    
                    if interaction_type < fission_xs:
                        n_fissions += 1
                        alive = False
                        
                        # Record fission site for criticality calculations
                        if fission_chain:
                            fission_sites.append(pos.copy())
                            
                            # Create new neutrons for next generation
                            n_new = np.random.poisson(self.fission_neutrons)
                            for _ in range(n_new):
                                next_gen_neutrons.append({
                                    'pos': pos.copy(),
                                    'energy_group': np.random.randint(0, self.energy_groups)
                                })
                                
                    elif interaction_type < fission_xs + absorb_xs:
                        n_absorptions += 1
                        alive = False
                    else:
                        # Scattering - continue with new direction and possibly new energy
                        if self.energy_groups > 1:
                            # Simple energy group transition for multi-group
                            energy_group = np.random.randint(0, self.energy_groups)
                    
                    interactions += 1
                    
                final_positions.append(np.linalg.norm(pos))
                
            neutrons = next_gen_neutrons if fission_chain else []
            generation_sizes.append(len(next_gen_neutrons))
        
        # Calculate k-effective if we did fission chain
        k_effective = None
        k_error = None
        if fission_chain and len(generation_sizes) > 2:
            # Calculate k-effective as ratio of successive generations
            k_values = [generation_sizes[i+1]/generation_sizes[i] 
                      for i in range(len(generation_sizes)-1) if generation_sizes[i] > 0]
            k_effective = np.mean(k_values)
            k_error = np.std(k_values) / np.sqrt(len(k_values)) if len(k_values) > 1 else 0
        
        elapsed_time = time.time() - start_time
            
        return {
            'fissions': n_fissions,
            'absorptions': n_absorptions,
            'escapes': n_escapes,
            'path_lengths': path_lengths,
            'final_positions': final_positions,
            'k_effective': k_effective,
            'k_error': k_error,
            'generation_sizes': generation_sizes,
            'elapsed_time': elapsed_time
        }
    
    def visualize_results(self, results):
        """
        Visualize simulation results with better plots
        
        Parameters:
        -----------
        results : dict
            Results from simulate_neutrons method
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Interaction distribution
        interaction_counts = [results['fissions'], results['absorptions'], results['escapes']]
        interaction_labels = ['Fission', 'Absorption', 'Escape']
        axes[0, 0].bar(interaction_labels, interaction_counts)
        axes[0, 0].set_title('Neutron Interaction Distribution')
        axes[0, 0].set_ylabel('Count')
        
        # Plot 2: Path length distribution
        axes[0, 1].hist(results['path_lengths'], bins=50, alpha=0.7)
        axes[0, 1].set_title('Neutron Path Length Distribution')
        axes[0, 1].set_xlabel('Path Length (cm)')
        axes[0, 1].set_ylabel('Frequency')
        
        # Plot 3: Final position distribution
        axes[1, 0].hist(results['final_positions'], bins=50, alpha=0.7)
        axes[1, 0].set_title('Final Radial Position Distribution')
        axes[1, 0].set_xlabel('Radial Position (cm)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].axvline(x=self.radius, color='r', linestyle='--', 
                          label=f'System Boundary (r={self.radius}cm)')
        axes[1, 0].legend()
        
        # Plot 4: Generation sizes for criticality (if available)
        if 'k_effective' in results and results['k_effective'] is not None:
            generations = range(len(results['generation_sizes']))
            axes[1, 1].plot(generations, results['generation_sizes'], 'o-')
            axes[1, 1].set_title(f'Neutron Population per Generation\nk-eff = {results["k_effective"]:.4f} ± {results["k_error"]:.4f}')
            axes[1, 1].set_xlabel('Generation')
            axes[1, 1].set_ylabel('Number of Neutrons')
            axes[1, 1].grid(True)
        else:
            axes[1, 1].text(0.5, 0.5, 'No criticality data available', 
                           horizontalalignment='center', verticalalignment='center')
        
        fig.tight_layout()
        return fig