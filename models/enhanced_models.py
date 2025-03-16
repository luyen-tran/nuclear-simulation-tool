"""
Các lớp mô hình nâng cao cho ứng dụng mô phỏng vật lý hạt nhân
"""

import numpy as np
import pandas as pd
from scipy.special import erf

class EnhancedChainReactionModel:
    """Mô hình phản ứng dây chuyền nâng cao với nhiều tính năng chi tiết hơn"""
    
    def __init__(self, enrichment=0.85, neutrons_per_fission=2.43, tamper="none"):
        self.enrichment = enrichment
        self.neutrons_per_fission = neutrons_per_fission
        self.tamper = tamper
        
        # Các hằng số bổ sung
        self.tamper_factors = {
            "none": 1.0,
            "natural_u": 1.4,
            "beryllium": 1.8,
            "tungsten": 1.6
        }
        
        self.energy_per_fission = 3.2e-11  # J
    
    def calculate_critical_mass(self, geometry="sphere"):
        """Tính khối lượng tới hạn dựa trên hình học và tham số bổ sung"""
        
        # Hệ số cơ bản dựa trên hình học
        geometry_factor = 1.0
        if geometry == "sphere":
            geometry_factor = 1.0
        elif geometry == "cylinder":
            geometry_factor = 1.25
        else:  # slab
            geometry_factor = 1.5
        
        # Tính toán khối lượng tới hạn cơ bản
        base_critical_mass = 52 / (self.enrichment ** 2) * (1 - self.enrichment) ** 1.5
        
        # Áp dụng hiệu ứng tamper
        tamper_effect = self.tamper_factors.get(self.tamper, 1.0)
        
        # Điều chỉnh dựa trên số neutron trung bình trên mỗi lần phân hạch
        neutron_factor = 2.43 / self.neutrons_per_fission
        
        # Khối lượng tới hạn cuối cùng
        critical_mass = base_critical_mass * geometry_factor * neutron_factor / tamper_effect
        
        return critical_mass
    
    def calculate_efficiency(self, mass_ratio, tamper="none"):
        """Tính hiệu suất phân hạch dựa trên tỷ lệ khối lượng và tamper"""
        
        # Hiệu suất cơ bản tăng theo tỷ lệ khối lượng
        base_efficiency = 0.15 * (1 - np.exp(-(mass_ratio - 1) * 2))
        
        # Giới hạn trên của hiệu suất
        if mass_ratio < 1.0:
            return 0.0  # Dưới khối lượng tới hạn
        
        # Tamper cải thiện hiệu suất
        tamper_bonus = 1.0
        if tamper == "natural_u":
            tamper_bonus = 1.2
        elif tamper == "beryllium":
            tamper_bonus = 1.3
        elif tamper == "tungsten":
            tamper_bonus = 1.25
        
        # Hiệu suất tổng thể
        efficiency = base_efficiency * tamper_bonus
        
        # Giới hạn trên của hiệu suất
        return min(efficiency, 0.4)
    
    def detailed_simulation(self, initial_neutrons=10, mass_ratio=1.5):
        """Mô phỏng chi tiết phản ứng dây chuyền với thế hệ neutron"""
        
        # Tính hiệu suất cho tỷ lệ khối lượng đã cho
        efficiency = self.calculate_efficiency(mass_ratio, self.tamper)
        
        # Tính k-effective
        k_effective = mass_ratio * self.neutrons_per_fission / 2.43
        
        # Dự đoán số thế hệ trước khi phóng xạ alpha làm giải phóng năng lượng đáng kể
        if k_effective <= 1.0:
            num_generations = 5  # Dừng sớm cho hệ dưới tới hạn
        else:
            # Số thế hệ để đạt 10^20 neutron (ngưỡng năng lượng đáng kể)
            num_generations = int(np.log(1e20 / initial_neutrons) / np.log(k_effective) + 1)
            num_generations = min(num_generations, 100)  # Giới hạn tối đa
        
        # Mô phỏng các thế hệ
        neutron_population = [initial_neutrons]
        energy_released = [0.0]
        
        for gen in range(1, num_generations):
            next_pop = neutron_population[-1] * k_effective
            
            # Thêm một chút nhiễu
            next_pop *= (1 + np.random.normal(0, 0.02))
            
            # Cập nhật quần thể
            neutron_population.append(next_pop)
            
            # Tính năng lượng giải phóng
            fissions = next_pop / self.neutrons_per_fission
            new_energy = fissions * self.energy_per_fission
            total_energy = energy_released[-1] + new_energy
            energy_released.append(total_energy)
        
        # Tạo dòng thời gian
        # Thời gian giữa các thế hệ: 10 nanoseconds = 1e-8 seconds
        generation_time = 1e-8  # giây
        times = np.array([gen * generation_time for gen in range(num_generations)])
        
        # Tạo mảng neutron với nhiều điểm hơn cho khớp và mịn hơn
        neutron_times = np.linspace(times[0], times[-1], num=1000)
        neutron_interp = np.interp(neutron_times, times, neutron_population)
        
        return neutron_times, neutron_interp, neutron_population, energy_released
    
    def calculate_k_effective(self):
        """Tính hệ số nhân hiệu dụng"""
        # Giá trị mặc định phù hợp với mô hình
        return self.neutrons_per_fission * self.tamper_factors.get(self.tamper, 1.0) / 2.43
    
    def multi_parameter_analysis(self, mass_ratios, neutrons_per_fission_values):
        """Phân tích đa tham số về ảnh hưởng đến năng lượng phân hạch"""
        
        # Tạo một mảng 2D để lưu kết quả năng lượng
        results = np.zeros((len(neutrons_per_fission_values), len(mass_ratios)))
        
        # Tính toán năng lượng cho mỗi tổ hợp tham số
        for i, npf in enumerate(neutrons_per_fission_values):
            for j, mr in enumerate(mass_ratios):
                # Tạo một mô hình tạm thời với các tham số đã cho
                temp_model = EnhancedChainReactionModel(
                    enrichment=self.enrichment,
                    neutrons_per_fission=npf,
                    tamper=self.tamper
                )
                
                # Tính hiệu suất
                efficiency = temp_model.calculate_efficiency(mr, self.tamper)
                
                # Ước tính năng lượng giải phóng (kt)
                critical_mass = temp_model.calculate_critical_mass("sphere")
                material_mass = critical_mass * mr
                energy_kt = material_mass * efficiency * 17  # Ước tính 17 kt/kg cho hiệu suất 100%
                
                results[i, j] = energy_kt
        
        return results

# Hàm tiện ích để tạo mô hình chuỗi phản ứng nâng cao
def enhanced_chain_reaction_model(**kwargs):
    """Tạo một thể hiện mới của mô hình chuỗi phản ứng nâng cao"""
    return EnhancedChainReactionModel(**kwargs)

class AdvancedNeutronTransport:
    """Mô hình vận chuyển neutron nâng cao hỗ trợ tính toán đa nhóm và hình học phức tạp"""
    
    def __init__(self, num_energy_groups=1, geometry="slab", 
                 boundary_condition="vacuum", albedo=0.0,
                 material_config="homogeneous"):
        
        self.num_energy_groups = num_energy_groups
        self.geometry = geometry
        self.boundary_condition = boundary_condition
        self.albedo = albedo
        self.material_config = material_config
        
        # Khởi tạo thông số vật lý
        self.initialize_physics()
    
    def initialize_physics(self):
        """Khởi tạo các thông số vật lý"""
        
        # Tiết diện phân hạch cho từng nhóm năng lượng
        if self.num_energy_groups == 1:
            self.fission_xs = 0.05
            self.absorption_xs = 0.01
            self.scattering_xs = 0.2
            self.energy_range = ["0 - 20 MeV"]
        else:
            # Đa nhóm
            self.fission_xs = np.array([0.08, 0.05, 0.02, 0.01, 0.005, 0.001, 0.0005][:self.num_energy_groups])
            self.absorption_xs = np.array([0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06][:self.num_energy_groups])
            self.scattering_xs = np.array([0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.05][:self.num_energy_groups])
            
            # Phạm vi năng lượng cho mỗi nhóm
            energy_bounds = [20.0, 10.0, 5.0, 1.0, 0.5, 0.1, 0.01, 0.0001]
            self.energy_range = [
                f"{energy_bounds[i+1]} - {energy_bounds[i]} MeV" 
                for i in range(min(7, self.num_energy_groups))
            ]
            
            # Tạo ma trận tán xạ giữa các nhóm
            self.scattering_matrix = np.zeros((self.num_energy_groups, self.num_energy_groups))
            
            # Điền ma trận tán xạ (đơn giản hóa: chủ yếu tán xạ xuống các nhóm năng lượng thấp hơn)
            for i in range(self.num_energy_groups):
                self.scattering_matrix[i, i] = 0.5  # Tán xạ nội nhóm
                
                # Tán xạ đến nhóm năng lượng thấp hơn
                remaining = 0.5
                for j in range(i+1, self.num_energy_groups):
                    if j == self.num_energy_groups - 1:
                        self.scattering_matrix[i, j] = remaining
                    else:
                        self.scattering_matrix[i, j] = remaining * 0.5
                        remaining *= 0.5
    
    def solve_multigroup_equation(self, size=10.0):
        """Giải phương trình khuếch tán neutron đa nhóm"""
        
        # Số điểm không gian
        spatial_points = 100
        
        # Tạo lưới không gian
        x = np.linspace(0, size, spatial_points)
        dx = size / (spatial_points - 1)
        
        # Tạo một mảng để lưu dòng
        flux = np.zeros((spatial_points, self.num_energy_groups))
        
        # Khởi tạo dòng với các giá trị ban đầu
        for g in range(self.num_energy_groups):
            flux[:, g] = np.sin(np.pi * x / size)  # Dạng ban đầu hợp lý
        
        # Lặp phương pháp lũy tiến (đơn giản hóa so với giải chính xác)
        for _ in range(100):  # Số vòng lặp cố định
            new_flux = np.zeros_like(flux)
            
            # Lặp qua từng nhóm
            for g in range(self.num_energy_groups):
                # Hệ số khuếch tán
                D_g = 1.0 / (3.0 * (self.scattering_xs[g] + self.absorption_xs[g]))
                
                # Áp dụng toán tử khuếch tán
                for i in range(1, spatial_points-1):
                    diffusion_term = D_g * (flux[i+1, g] - 2*flux[i, g] + flux[i-1, g]) / (dx**2)
                    absorption_term = -self.absorption_xs[g] * flux[i, g]
                    
                    # Thêm nguồn từ phân hạch và tán xạ
                    fission_source = 0.0
                    scatter_source = 0.0
                    
                    # Nguồn phân hạch từ tất cả các nhóm
                    for g2 in range(self.num_energy_groups):
                        fission_source += self.fission_xs[g2] * flux[i, g2] * 2.43 / self.num_energy_groups
                    
                    # Tán xạ vào nhóm g từ các nhóm khác
                    for g2 in range(self.num_energy_groups):
                        scatter_source += self.scattering_matrix[g2, g] * self.scattering_xs[g2] * flux[i, g2]
                    
                    # Cập nhật dòng
                    new_flux[i, g] = flux[i, g] + 0.1 * (diffusion_term + absorption_term + fission_source + scatter_source)
                    
                # Áp dụng điều kiện biên
                if self.boundary_condition == "vacuum":
                    new_flux[0, g] = 0.0
                    new_flux[-1, g] = 0.0
                elif self.boundary_condition == "reflective":
                    new_flux[0, g] = new_flux[1, g]
                    new_flux[-1, g] = new_flux[-2, g]
                elif self.boundary_condition == "albedo":
                    new_flux[0, g] = self.albedo * new_flux[1, g]
                    new_flux[-1, g] = self.albedo * new_flux[-2, g]
            
            # Chuẩn hóa lại dòng
            normalization = np.max(new_flux)
            if normalization > 0:
                new_flux /= normalization
            
            # Cập nhật dòng
            flux = new_flux
        
        return {
            'position': x,
            'flux': flux,
            'energy_range': self.energy_range,
            'fission_xs': self.fission_xs,
            'scattering_xs': self.scattering_xs,
            'scattering_matrix': self.scattering_matrix
        }
    
    def solve_geometry_problem(self, size=10.0, method="diffusion"):
        """Giải bài toán với hình học cụ thể"""
        
        # Số điểm không gian
        spatial_points = 100
        
        # Tạo lưới không gian
        if self.geometry == "slab":
            # 1D
            x = np.linspace(0, size, spatial_points)
            dx = size / (spatial_points - 1)
            dim = 1
        elif self.geometry == "cylindrical":
            # 1D nhưng với bán kính r
            x = np.linspace(0, size, spatial_points)
            dx = size / (spatial_points - 1)
            dim = 2
        else:  # spherical
            x = np.linspace(0, size, spatial_points)
            dx = size / (spatial_points - 1)
            dim = 3
        
        # Thiết lập vùng vật liệu
        region_boundaries = []
        if self.material_config == "two_region":
            region_boundaries = [size/2]
        elif self.material_config == "three_region":
            region_boundaries = [size/3, 2*size/3]
        
        # Tạo một mảng để lưu dòng
        flux = np.zeros(spatial_points)
        
        # Khởi tạo dòng với các giá trị ban đầu
        if self.geometry == "slab":
            flux = np.sin(np.pi * x / size)
        elif self.geometry == "cylindrical":
            # Sử dụng hàm Bessel J0 (đơn giản hóa)
            r = x
            flux = np.exp(-r/size*3) * (1 + 0.2*np.sin(5*np.pi*r/size))
        else:  # spherical
            r = x
            flux = np.sin(np.pi * r / size) / (r + 0.001)  # Tránh chia cho 0
        
        # Chuẩn hóa ban đầu
        flux = flux / np.max(flux)
        
        # Tạo flux 2D cho hình học không phải slab
        flux_2d = None
        if self.geometry != "slab":
            # Tạo lưới 2D đơn giản
            grid_size = 50
            x_grid = np.linspace(-size, size, grid_size)
            y_grid = np.linspace(-size, size, grid_size)
            X, Y = np.meshgrid(x_grid, y_grid)
            
            # Tính bán kính tại mỗi điểm
            R = np.sqrt(X**2 + Y**2)
            
            # Tạo flux 2D
            flux_2d = np.zeros_like(R)
            for i in range(grid_size):
                for j in range(grid_size):
                    r_val = R[i, j]
                    if r_val <= size:
                        # Nội suy từ flux 1D
                        idx = int(r_val / size * (spatial_points-1))
                        idx = min(idx, spatial_points-1)
                        flux_2d[i, j] = flux[idx]
        
        # Tính buckling và leakage
        buckling = (np.pi / size) ** 2
        leakage = buckling / (buckling + 0.1)  # Giả lập đơn giản
        
        return {
            'position': x,
            'flux': flux,
            'flux_2d': flux_2d,
            'region_boundaries': region_boundaries,
            'max_flux': np.max(flux),
            'buckling': buckling,
            'leakage': leakage
        }

# Hàm tiện ích để tạo mô hình vận chuyển neutron nâng cao
def advanced_neutron_transport(**kwargs):
    """Tạo một thể hiện mới của mô hình vận chuyển neutron nâng cao"""
    return AdvancedNeutronTransport(**kwargs) 