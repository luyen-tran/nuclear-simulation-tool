import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

class NeutronTransportModel:
    def __init__(self, spatial_points=100, scattering_xs=0.1, 
                 absorption_xs=0.01, fission_xs=0.05):
        self.spatial_points = spatial_points
        self.scattering_xs = scattering_xs  # Scattering cross-section
        self.absorption_xs = absorption_xs  # Absorption cross-section
        self.fission_xs = fission_xs        # Fission cross-section
        
    def solve_diffusion_equation(self, size=10.0, boundary_condition="vacuum"):
        """
        Solve the one-group neutron diffusion equation:
        -D∇²Φ + Σₐ·Φ = νΣf·Φ
        
        With vacuum boundary conditions
        """
        # Set up spatial grid
        dx = size / self.spatial_points
        x = np.linspace(dx/2, size-dx/2, self.spatial_points)
        
        # Diffusion coefficient (approximation)
        D = 1.0 / (3.0 * (self.scattering_xs + self.absorption_xs))
        
        # Build the diffusion matrix (1D case)
        main_diag = np.ones(self.spatial_points) * (2*D/(dx**2) + self.absorption_xs)
        off_diag = np.ones(self.spatial_points-1) * (-D/(dx**2))
        
        A = diags([main_diag, off_diag, off_diag], [0, -1, 1]).toarray()
        
        # Source term (fission source)
        S = np.ones(self.spatial_points) * self.fission_xs * 2.43  # ν = 2.43 neutrons per fission
        
        # Apply boundary conditions
        if boundary_condition == "vacuum":
            # Adjust for vacuum boundary conditions
            A[0, 0] += D/(dx**2)
            A[-1, -1] += D/(dx**2)
        
        # Solve the system
        flux = np.linalg.solve(A, S)
        
        return x, flux