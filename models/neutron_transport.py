import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

class NeutronTransportModel:
    def __init__(self, spatial_points=100, scattering_xs=0.1, 
                 absorption_xs=0.01, fission_xs=0.05, nu=2.43, dimension=1):
        """
        Khởi tạo mô hình vận chuyển nơtron
        """
        self.spatial_points = spatial_points  # Số điểm không gian
        self.scattering_xs = scattering_xs    # Tiết diện tán xạ
        self.absorption_xs = absorption_xs    # Tiết diện hấp thụ
        self.fission_xs = fission_xs          # Tiết diện phân hạch
        self.nu = nu                          # Số nơtron trung bình sinh ra mỗi phân hạch
        self.dimension = dimension            # Số chiều không gian (1D, 2D hoặc 3D)
        
    def calculate_diffusion_coefficient(self, energy_group=0):
        """
        Tính hệ số khuếch tán
        D = 1/(3(Σs + Σa))
        """
        return 1.0 / (3.0 * (self.scattering_xs + self.absorption_xs))
    
    def solve_diffusion_equation(self, size=10.0, boundary_condition="vacuum", source_distribution=None):
        """
        Giải phương trình khuếch tán nơtron một nhóm:
        -D∇²Φ + Σₐ·Φ = νΣf·Φ
        
        Với các điều kiện biên khác nhau
        
        Tham số:
            size: Kích thước vùng tính toán (cm)
            boundary_condition: Điều kiện biên ('vacuum', 'reflective', 'periodic')
            source_distribution: Phân bố nguồn (None = đồng nhất)
            
        Trả về:
            x: Tọa độ không gian
            flux: Phân bố thông lượng nơtron
        """
        # Thiết lập lưới không gian
        dx = size / self.spatial_points
        x = np.linspace(dx/2, size-dx/2, self.spatial_points)
        
        # Hệ số khuếch tán (xấp xỉ)
        D = self.calculate_diffusion_coefficient()
        
        # Xây dựng ma trận khuếch tán (trường hợp 1D)
        main_diag = np.ones(self.spatial_points) * (2*D/(dx**2) + self.absorption_xs)
        off_diag = np.ones(self.spatial_points-1) * (-D/(dx**2))
        
        # Tạo ma trận hệ thống
        A = diags([main_diag, off_diag, off_diag], [0, -1, 1]).toarray()
        
        # Thành phần nguồn (nguồn phân hạch)
        if source_distribution is None:
            # Nguồn đồng nhất
            S = np.ones(self.spatial_points) * self.fission_xs * self.nu
        else:
            # Sử dụng phân bố nguồn được cung cấp
            S = source_distribution
        
        # Áp dụng điều kiện biên
        if boundary_condition == "vacuum":
            # Điều chỉnh cho điều kiện biên chân không
            A[0, 0] += D/(dx**2)
            A[-1, -1] += D/(dx**2)
        elif boundary_condition == "reflective":
            # Điều kiện biên phản xạ (đạo hàm bằng 0)
            A[0, 1] *= 2
            A[-1, -2] *= 2
        elif boundary_condition == "periodic":
            # Điều kiện biên tuần hoàn
            A[0, -1] = -D/(dx**2)
            A[-1, 0] = -D/(dx**2)
        else:
            raise ValueError("Điều kiện biên không được hỗ trợ: {}".format(boundary_condition))
        
        # Giải hệ phương trình
        try:
            flux = np.linalg.solve(A, S)
        except np.linalg.LinAlgError:
            # Sử dụng phương pháp giải thưa nếu ma trận có vấn đề
            flux = spsolve(diags([main_diag, off_diag, off_diag], [0, -1, 1]), S)
        
        return x, flux
    
    def solve_multigroup_diffusion(self, num_groups=2, sizes=None, cross_sections=None):
        """
        Giải phương trình khuếch tán nơtron đa nhóm
        
        Tham số:
            num_groups: Số nhóm năng lượng
            sizes: Kích thước vùng tính toán cho mỗi nhóm
            cross_sections: Tiết diện cho mỗi nhóm năng lượng
            
        Trả về:
            fluxes: Danh sách thông lượng nơtron cho mỗi nhóm năng lượng
        """
        if sizes is None:
            sizes = [10.0] * num_groups
            
        fluxes = []
        
        # Giải phương trình cho từng nhóm năng lượng
        for g in range(num_groups):
            # Sử dụng tiết diện mặc định nếu không được cung cấp
            if cross_sections is not None:
                self.scattering_xs = cross_sections[g]['scattering']
                self.absorption_xs = cross_sections[g]['absorption']
                self.fission_xs = cross_sections[g]['fission']
            
            x, flux = self.solve_diffusion_equation(size=sizes[g])
            fluxes.append((x, flux))
            
        return fluxes
    
    def plot_flux(self, x, flux, title="Phân bố thông lượng nơtron"):
        """
        Vẽ đồ thị thông lượng nơtron
        """
        plt.figure(figsize=(10, 6))
        plt.plot(x, flux)
        plt.title(title)
        plt.xlabel("Vị trí (cm)")
        plt.ylabel("Thông lượng nơtron (n/cm²·s)")
        plt.grid(True)
        return plt.gcf()