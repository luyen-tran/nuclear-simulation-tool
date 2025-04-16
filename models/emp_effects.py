import numpy as np
import matplotlib.pyplot as plt

class EMPModel:
    def __init__(self, yield_kt=20, burst_height=30, ground_conductivity=0.005, detonation_type="high-altitude"):
        """
        Khởi tạo mô hình EMP (Electromagnetic Pulse) từ vụ nổ hạt nhân
        
        Tham số:
            yield_kt (float): Năng lượng vụ nổ tính bằng kiloton TNT
            burst_height (float): Độ cao vụ nổ tính bằng km
            ground_conductivity (float): Độ dẫn điện của mặt đất (S/m)
            detonation_type (str): Loại vụ nổ, có thể là "high-altitude" (trên cao), 
                                  "surface" (mặt đất) hoặc "air-burst" (trên không)
        """
        # Kiểm tra tính hợp lệ của tham số đầu vào
        if yield_kt <= 0:
            raise ValueError("Năng lượng vụ nổ phải lớn hơn 0")
        if burst_height < 0:
            raise ValueError("Độ cao vụ nổ không thể âm")
        if ground_conductivity <= 0:
            raise ValueError("Độ dẫn điện mặt đất phải lớn hơn 0")
        if detonation_type not in ["high-altitude", "surface", "air-burst"]:
            raise ValueError("Loại vụ nổ không hợp lệ")
            
        self.yield_kt = yield_kt
        self.burst_height = burst_height  # km
        self.ground_conductivity = ground_conductivity  # S/m
        self.detonation_type = detonation_type
        self.total_energy = yield_kt * 4.184e12  # joules
        
        # Tỷ lệ phần trăm năng lượng chuyển thành EMP, phụ thuộc loại vụ nổ
        self.emp_energy_ratio = {
            "high-altitude": 0.003,    # 0.3% năng lượng thành EMP ở vụ nổ tầm cao
            "air-burst": 0.0005,       # 0.05% cho vụ nổ trên không thấp
            "surface": 0.0001          # 0.01% cho vụ nổ mặt đất
        }[detonation_type]
        
        # Năng lượng EMP 
        self.emp_energy = self.total_energy * self.emp_energy_ratio
        
        # Tần số đặc trưng của xung EMP (Hz)
        self.emp_frequency = {
            "high-altitude": 10e6,     # 10 MHz cho vụ nổ tầm cao
            "air-burst": 1e6,          # 1 MHz cho vụ nổ trên không
            "surface": 100e3           # 100 kHz cho vụ nổ mặt đất
        }[detonation_type]
        
        # Thời gian xung EMP (giây)
        self.emp_duration = {
            "high-altitude": 1e-6,     # 1 microsecond cho vụ nổ tầm cao
            "air-burst": 10e-6,        # 10 microseconds cho vụ nổ trên không
            "surface": 100e-6          # 100 microseconds cho vụ nổ mặt đất
        }[detonation_type]
        
    def calculate_emp_field_strength(self, distances):
        """
        Tính cường độ trường EMP theo khoảng cách
        
        Tham số:
            distances (array): Mảng các khoảng cách tính từ tâm vụ nổ (km)
            
        Trả về:
            array: Cường độ trường EMP tại mỗi khoảng cách (V/m)
        """
        # Chuyển đổi khoảng cách từ km sang m
        distances_m = np.asarray(distances) * 1000
        
        # Tính cường độ trường EMP cơ sở dựa trên năng lượng vụ nổ và loại vụ nổ
        if self.detonation_type == "high-altitude":
            # Công thức dựa trên mô hình EMP của vụ nổ tầm cao
            # E0 ~ (Năng lượng)^(1/2) cho HEMP (High-altitude EMP)
            emp_base = 50000 * np.sqrt(self.yield_kt)  # V/m
        else:
            # Công thức cho vụ nổ thấp hơn
            emp_base = 15000 * np.sqrt(self.yield_kt)  # V/m
        
        # Hiệu chỉnh theo độ cao nổ (hàm phi tuyến thực tế hơn)
        if self.detonation_type == "high-altitude":
            # Với vụ nổ tầm cao, độ cao là yếu tố quan trọng
            height_factor = 1.0 + np.log10(1 + self.burst_height / 20)
        else:
            # Với vụ nổ thấp hơn, tác động của độ cao giảm
            height_factor = 1.0 + 0.05 * np.log10(1 + self.burst_height)
        
        # Hiệu chỉnh theo độ dẫn điện mặt đất (mô hình cải tiến)
        # Đất dẫn điện tốt sẽ làm giảm cường độ EMP do hiệu ứng phản xạ và hấp thụ
        conductivity_reference = 0.01  # S/m (giá trị tham chiếu)
        ground_factor = 1.0 - 0.4 * np.tanh(self.ground_conductivity / conductivity_reference)
        
        # Mảng kết quả
        field_strength = np.zeros_like(distances_m, dtype=float)
        
        # Tính cường độ trường theo khoảng cách với mô hình vật lý chính xác hơn
        for i, distance in enumerate(distances_m):
            if self.detonation_type == "high-altitude":
                # Vụ nổ tầm cao có phạm vi ảnh hưởng lớn hơn và giảm chậm hơn theo khoảng cách
                effective_distance = max(distance, 1000)  # Tránh giá trị quá lớn ở gần tâm vụ nổ
                attenuation = (40000 / effective_distance) ** 1.1  # Giảm theo khoảng cách
                attenuation = min(1.0, attenuation)  # Giới hạn giá trị tối đa
            else:
                # Vụ nổ thấp hơn giảm nhanh hơn theo khoảng cách
                effective_distance = max(distance, 500)
                attenuation = (3000 / effective_distance) ** 1.5
                attenuation = min(1.0, attenuation)
            
            # Kết hợp các thành phần
            field_strength[i] = emp_base * height_factor * ground_factor * attenuation
            
        return field_strength
    
    def calculate_emp_effects(self, distances):
        """
        Tính tác động của EMP ở các khoảng cách khác nhau
        
        Tham số:
            distances (array): Mảng các khoảng cách tính từ tâm vụ nổ (km)
            
        Trả về:
            dict: Từ điển chứa kết quả phân tích EMP, bao gồm:
                - cường độ trường (V/m)
                - xác suất hư hỏng thiết bị điện tử
                - thời gian phục hồi ước tính
                - phân loại mức độ tác động
        """
        field_strength = self.calculate_emp_field_strength(distances)
        
        # Ngưỡng hư hỏng cho các loại thiết bị (V/m)
        threshold_consumer_electronics = 5000      # Thiết bị điện tử tiêu dùng
        threshold_commercial_equipment = 10000     # Thiết bị thương mại
        threshold_power_grid = 8000               # Lưới điện
        threshold_communication = 7000            # Thiết bị thông tin liên lạc
        threshold_military_hardened = 50000       # Thiết bị quân sự cứng cáp
        
        # Mô hình xác suất hư hỏng tinh vi hơn (sigmoid)
        def damage_probability(strength, threshold, steepness=5e-4):
            """Tính xác suất hư hỏng với mô hình sigmoid"""
            return 1.0 / (1.0 + np.exp(-steepness * (strength - threshold)))
        
        # Tính xác suất hư hỏng cho từng loại thiết bị
        consumer_damage_prob = damage_probability(field_strength, threshold_consumer_electronics)
        commercial_damage_prob = damage_probability(field_strength, threshold_commercial_equipment)
        power_grid_damage_prob = damage_probability(field_strength, threshold_power_grid)
        communication_damage_prob = damage_probability(field_strength, threshold_communication)
        military_damage_prob = damage_probability(field_strength, threshold_military_hardened)
        
        # Ước tính thời gian phục hồi (ngày)
        max_recovery_time = 180  # 6 tháng cho các tác động nghiêm trọng nhất
        recovery_time = max_recovery_time * power_grid_damage_prob * communication_damage_prob
        
        # Phân loại mức độ tác động
        impact_levels = np.zeros_like(distances, dtype=object)
        for i, strength in enumerate(field_strength):
            if strength < 1000:
                impact_levels[i] = "Không đáng kể"
            elif strength < 5000:
                impact_levels[i] = "Nhẹ"
            elif strength < 15000:
                impact_levels[i] = "Trung bình"
            elif strength < 30000:
                impact_levels[i] = "Nghiêm trọng"
            else:
                impact_levels[i] = "Thảm khốc"
        
        return {
            'distances': distances,
            'field_strength': field_strength,  # V/m
            'consumer_electronics_damage': consumer_damage_prob,
            'commercial_equipment_damage': commercial_damage_prob,
            'power_grid_damage': power_grid_damage_prob,
            'communication_damage': communication_damage_prob,
            'military_hardened_damage': military_damage_prob,
            'estimated_recovery_time': recovery_time,  # ngày
            'impact_level': impact_levels
        }
    
    def visualize_emp_effects(self, max_distance=100, points=100):
        """
        Trực quan hóa tác động của EMP theo khoảng cách
        
        Tham số:
            max_distance (float): Khoảng cách tối đa để hiển thị (km)
            points (int): Số điểm dữ liệu để tính toán
        """
        distances = np.linspace(1, max_distance, points)
        effects = self.calculate_emp_effects(distances)
        
        # Tạo figure với 2 subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Subplot 1: Cường độ trường
        ax1.plot(distances, effects['field_strength'], 'b-', linewidth=2)
        ax1.set_xlabel('Khoảng cách từ vụ nổ (km)')
        ax1.set_ylabel('Cường độ trường EMP (V/m)')
        ax1.set_title(f'Cường độ trường EMP - {self.yield_kt}kt, {self.burst_height}km, {self.detonation_type}')
        ax1.grid(True)
        ax1.set_yscale('log')
        
        # Subplot 2: Xác suất hư hỏng
        ax2.plot(distances, effects['consumer_electronics_damage'], 'r-', label='Thiết bị điện tử tiêu dùng')
        ax2.plot(distances, effects['commercial_equipment_damage'], 'g-', label='Thiết bị thương mại')
        ax2.plot(distances, effects['power_grid_damage'], 'b-', label='Lưới điện')
        ax2.plot(distances, effects['communication_damage'], 'm-', label='Hệ thống thông tin')
        ax2.plot(distances, effects['military_hardened_damage'], 'k-', label='Thiết bị quân sự cứng cáp')
        ax2.set_xlabel('Khoảng cách từ vụ nổ (km)')
        ax2.set_ylabel('Xác suất hư hỏng')
        ax2.set_title('Xác suất hư hỏng theo loại thiết bị')
        ax2.grid(True)
        ax2.legend()
        
        plt.tight_layout()
        return fig 