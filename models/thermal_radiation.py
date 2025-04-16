import numpy as np
from scipy.special import erf

class ThermalRadiationModel:
    def __init__(self, yield_kt=20, burst_height=0, relative_humidity=0.5, visibility=20):
        """
        Khởi tạo mô hình bức xạ nhiệt của vụ nổ hạt nhân.
        
        Tham số:
            yield_kt: Sức công phá tính bằng kiloton TNT
            burst_height: Chiều cao vụ nổ tính bằng mét
            relative_humidity: Độ ẩm tương đối (0-1)
            visibility: Tầm nhìn khí quyển tính bằng km
        """
        self.yield_kt = yield_kt  # sức công phá tính bằng kiloton
        self.burst_height = burst_height  # chiều cao vụ nổ tính bằng mét
        self.relative_humidity = relative_humidity  # độ ẩm tương đối
        self.visibility = visibility  # tầm nhìn khí quyển (km)
        
        # Các hằng số cho bức xạ nhiệt
        self.thermal_fraction = 0.35  # phần năng lượng dưới dạng bức xạ nhiệt
        self.total_energy = yield_kt * 4.184e12  # tổng năng lượng tính bằng joule
        self.thermal_energy = self.thermal_fraction * self.total_energy
        
        # Hệ số giảm bức xạ theo độ ẩm
        self.humidity_attenuation = 0.1 + 0.4 * relative_humidity  # độ giảm bức xạ tăng theo độ ẩm
        
    def calculate_atmospheric_transmission(self, distance):
        """
        Tính hệ số truyền qua khí quyển theo khoảng cách.
        
        Tham số:
            distance: Khoảng cách tính bằng mét
            
        Trả về:
            Hệ số truyền qua khí quyển (0-1)
        """
        # Mô hình cải tiến có tính đến tầm nhìn và độ ẩm
        # Công thức dựa trên quy luật Beer-Lambert với các hệ số thực nghiệm
        distance_km = distance / 1000
        base_attenuation = np.exp(-0.2 * distance_km / self.visibility)
        humidity_effect = np.exp(-0.1 * distance_km * self.humidity_attenuation)
        return base_attenuation * humidity_effect
        
    def calculate_thermal_energy_density(self, distance, terrain_factor=1.0):
        """
        Tính mật độ năng lượng nhiệt ở khoảng cách cho trước.
        
        Tham số:
            distance: Khoảng cách tính bằng mét
            terrain_factor: Hệ số địa hình (mặc định = 1.0)
                           < 1.0: Địa hình có che chắn
                           = 1.0: Địa hình phẳng
                           > 1.0: Địa hình phản xạ (như nước, tuyết)
                           
        Trả về:
            Mật độ năng lượng nhiệt (J/m²)
        """
        # Tính toán hệ số truyền qua khí quyển
        transmission = self.calculate_atmospheric_transmission(distance)
        
        # Tính khoảng cách xiên nếu có chiều cao nổ
        if self.burst_height > 0:
            slant_range = np.sqrt(distance**2 + self.burst_height**2)
        else:
            slant_range = distance
            
        # Năng lượng trên đơn vị diện tích
        energy_density = self.thermal_energy / (4 * np.pi * slant_range**2) * transmission * terrain_factor
        return energy_density
    
    def calculate_thermal_effects(self, distances, terrain_factor=1.0):
        """
        Tính toán các ảnh hưởng nhiệt ở nhiều khoảng cách khác nhau.
        
        Tham số:
            distances: Mảng các khoảng cách tính bằng mét
            terrain_factor: Hệ số địa hình
            
        Trả về:
            Dictionary chứa khoảng cách, mật độ năng lượng, xác suất bỏng và nguy cơ cháy
        """
        energy_densities = np.array([self.calculate_thermal_energy_density(d, terrain_factor) for d in distances])
        
        # Ngưỡng bỏng da (J/m²)
        first_degree_burn = 2e5  # ngưỡng bỏng độ 1
        second_degree_burn = 4e5  # ngưỡng bỏng độ 2
        third_degree_burn = 6e5  # ngưỡng bỏng độ 3
        
        # Ngưỡng cháy vật liệu thông thường (J/m²)
        paper_ignition = 1e5  # giấy khô
        grass_ignition = 3e5  # cỏ khô
        wood_ignition = 8e5  # gỗ
        
        # Tính xác suất gây bỏng (sử dụng hàm lỗi cho đường cong chuyển tiếp mượt)
        p_first_degree = 0.5 * (1 + erf((energy_densities - first_degree_burn) / (0.2 * first_degree_burn)))
        p_second_degree = 0.5 * (1 + erf((energy_densities - second_degree_burn) / (0.2 * second_degree_burn)))
        p_third_degree = 0.5 * (1 + erf((energy_densities - third_degree_burn) / (0.2 * third_degree_burn)))
        
        # Tính xác suất gây cháy
        p_paper_ignition = 0.5 * (1 + erf((energy_densities - paper_ignition) / (0.2 * paper_ignition)))
        p_grass_ignition = 0.5 * (1 + erf((energy_densities - grass_ignition) / (0.2 * grass_ignition)))
        p_wood_ignition = 0.5 * (1 + erf((energy_densities - wood_ignition) / (0.2 * wood_ignition)))
        
        return {
            'distances': distances,
            'energy_density': energy_densities,
            'first_degree_burn_probability': p_first_degree,
            'second_degree_burn_probability': p_second_degree,
            'third_degree_burn_probability': p_third_degree,
            'paper_ignition_probability': p_paper_ignition,
            'grass_ignition_probability': p_grass_ignition,
            'wood_ignition_probability': p_wood_ignition
        }
        
    def get_damage_radius(self, effect_type, probability_threshold=0.5):
        """
        Ước tính bán kính gây thiệt hại cho loại ảnh hưởng cụ thể.
        
        Tham số:
            effect_type: Loại ảnh hưởng ('first_degree', 'second_degree', 'third_degree',
                        'paper_ignition', 'grass_ignition', 'wood_ignition')
            probability_threshold: Ngưỡng xác suất (0-1)
            
        Trả về:
            Bán kính ước tính (mét) nơi xác suất ảnh hưởng vượt quá ngưỡng
        """
        # Ánh xạ loại ảnh hưởng đến ngưỡng năng lượng
        effect_thresholds = {
            'first_degree': 2e5,
            'second_degree': 4e5,
            'third_degree': 6e5,
            'paper_ignition': 1e5,
            'grass_ignition': 3e5,
            'wood_ignition': 8e5
        }
        
        if effect_type not in effect_thresholds:
            raise ValueError(f"Loại ảnh hưởng không hợp lệ: {effect_type}")
            
        # Lấy ngưỡng năng lượng cho loại ảnh hưởng
        threshold = effect_thresholds[effect_type]
        
        # Tính toán ngưỡng năng lượng điều chỉnh theo xác suất
        # Biến đổi ngược hàm lỗi để tìm năng lượng cần thiết ở ngưỡng xác suất
        adjusted_threshold = threshold * (1 + 0.2 * erf(2 * probability_threshold - 1))
        
        # Tìm bán kính bằng phương pháp ước lượng thô
        # Giả định truyền khí quyển là 1.0 cho ước tính ban đầu
        initial_radius = np.sqrt(self.thermal_energy / (4 * np.pi * adjusted_threshold))
        
        # Tinh chỉnh ước tính bằng phương pháp lặp đơn giản
        radius = initial_radius
        for _ in range(5):  # 5 vòng lặp thường đủ để hội tụ
            transmission = self.calculate_atmospheric_transmission(radius)
            radius = np.sqrt(self.thermal_energy * transmission / (4 * np.pi * adjusted_threshold))
            
        return radius