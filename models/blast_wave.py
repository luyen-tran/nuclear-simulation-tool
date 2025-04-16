import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from numba import jit
import warnings

# Tách hàm tính bán kính ra khỏi lớp để có thể tối ưu hóa với numba
@jit(nopython=True)
def calculate_blast_radius(energy, ambient_density, time):
    """
    Tính bán kính sóng xung kích sử dụng công thức Sedov-Taylor
    R(t) = β·(E·t²/ρ)^(1/5)
    
    β: hệ số không thứ nguyên cho vụ nổ hình cầu
    E: năng lượng vụ nổ (J)
    t: thời gian (s)
    ρ: mật độ không khí (kg/m³)
    """
    beta = 1.15  # hệ số không thứ nguyên cho vụ nổ hình cầu
    return beta * (energy * time**2 / ambient_density)**(1/5)

class SedovTaylorModel:
    def __init__(self, energy_kt=20, ambient_density=1.225, gamma=1.4, altitude=0):
        # Chuyển đổi từ kiloton sang joule: 1 kt TNT = 4.184e12 J
        self.energy = energy_kt * 4.184e12  
        self.ambient_density = ambient_density  # kg/m³ - mật độ không khí xung quanh
        self.gamma = gamma  # tỉ số nhiệt dung riêng (ratio of specific heats)
        self.altitude = altitude  # độ cao so với mặt đất (m)
        
        # Tính toán áp suất không khí theo độ cao
        if altitude > 0:
            # Mô hình khí quyển tiêu chuẩn quốc tế
            self.ambient_density = ambient_density * np.exp(-altitude/8000)
    
    def blast_radius(self, time):
        """
        Tính bán kính sóng xung kích sử dụng công thức Sedov-Taylor
        Sử dụng hàm tối ưu bên ngoài lớp
        """
        return calculate_blast_radius(self.energy, self.ambient_density, time)
    
    def overpressure(self, distance, time):
        """
        Tính áp suất dư tại một điểm cách tâm vụ nổ một khoảng distance tại thời điểm time
        Sử dụng mô hình sóng Friedlander cải tiến để mô phỏng sự suy giảm áp suất theo thời gian
        """
        R = self.blast_radius(time)
        
        # Handle numpy arrays by vectorizing the operation
        if isinstance(distance, np.ndarray):
            # Create output array of same shape
            result = np.zeros_like(distance, dtype=float)
            
            # Find points where distance > R
            beyond_radius = distance > R
            
            # Calculate relative distance for all points
            rel_distance = np.divide(distance, R, out=np.zeros_like(distance, dtype=float), where=~beyond_radius)
            
            # Calculate shock pressure
            shock_pressure = 0.75 * self.ambient_density * (R / time)**2 / self.gamma
            
            # Apply near-shock condition (rel_distance > 0.95)
            near_shock = (~beyond_radius) & (rel_distance > 0.95)
            if np.any(near_shock):
                result[near_shock] = shock_pressure * (1 - rel_distance[near_shock]/0.95)
            
            # Apply internal condition (rel_distance <= 0.95)
            internal = (~beyond_radius) & (~near_shock)
            if np.any(internal):
                tau = 0.5
                result[internal] = shock_pressure * (1 - rel_distance[internal]) * np.exp(-rel_distance[internal]/tau)
                
            return result
        else:
            # Original scalar implementation
            if distance > R:
                return 0.0  # Áp suất dư bằng 0 nếu sóng xung kích chưa tới
            
            # Tính áp suất tại mặt sóng xung kích - cải thiện tính chính xác
            shock_pressure = 0.75 * self.ambient_density * (R / time)**2 / self.gamma
            
            # Sử dụng mô hình sóng Friedlander cải tiến cho sự suy giảm áp suất
            rel_distance = distance / R
            if rel_distance > 0.95:  # Gần mặt sóng xung kích
                return shock_pressure * (1 - rel_distance/0.95)
            else:
                # Suy giảm hàm mũ phía sau mặt sóng xung kích
                tau = 0.5  # Thời gian đặc trưng cho sự suy giảm
                return shock_pressure * (1 - rel_distance) * np.exp(-rel_distance/tau)
    
    def simulate_blast_wave(self, max_distance=10000, times=None, num_points=200):
        """
        Mô phỏng sự lan truyền của sóng xung kích theo thời gian và khoảng cách
        
        Args:
            max_distance: Khoảng cách tối đa tính từ tâm vụ nổ (m)
            times: Dãy các mốc thời gian để mô phỏng (s)
            num_points: Số điểm trên trục khoảng cách
            
        Returns:
            Dictionary chứa kết quả mô phỏng (thời gian, khoảng cách, bán kính, áp suất)
        """
        if times is None:
            times = np.linspace(0.1, 30.0, 100)  # mảng thời gian (giây)
            
        distances = np.linspace(0, max_distance, num_points)  # mảng khoảng cách (mét)
        
        # Tính bán kính sóng xung kích tại mỗi thời điểm
        radius_values = np.array([self.blast_radius(t) for t in times])
        
        # Tạo lưới khoảng cách và thời gian để tính áp suất
        pressures = np.zeros((len(distances), len(times)))
        
        # Tính toán áp suất cho từng thời điểm
        for j, time in enumerate(times):
            R = radius_values[j]
            
            # Tính áp suất tại các điểm trong phạm vi sóng xung kích
            for i, distance in enumerate(distances):
                if distance <= R:
                    # Tính áp suất dư tại điểm này
                    rel_distance = distance / R
                    shock_pressure = 0.75 * self.ambient_density * (R / time)**2 / self.gamma
                    
                    if rel_distance > 0.95:  # Gần mặt sóng xung kích
                        pressures[i, j] = shock_pressure * (1 - rel_distance/0.95)
                    else:
                        # Suy giảm hàm mũ phía sau mặt sóng xung kích
                        tau = 0.5
                        pressures[i, j] = shock_pressure * (1 - rel_distance) * np.exp(-rel_distance/tau)
                
        return {
            'times': times,
            'distances': distances,
            'radius': radius_values,
            'pressures': pressures
        }
    
    def damage_assessment(self, overpressure):
        """
        Đánh giá mức độ thiệt hại dựa trên áp suất dư (Pa)
        Trả về dictionary mô tả thiệt hại kèm giá trị boolean
        """
        # Ngưỡng thiệt hại dựa trên nghiên cứu về hiệu ứng vũ khí hạt nhân
        damage_levels = {
            1000: "Thiệt hại nhẹ (cửa sổ vỡ)",
            3000: "Thiệt hại nhẹ đến công trình (kính cửa sổ vỡ hoàn toàn)",
            7000: "Thiệt hại trung bình đến công trình gia cố",
            15000: "Hầu hết các tòa nhà dân cư sụp đổ",
            35000: "Công trình bê tông cốt thép bị hư hại nghiêm trọng",
            70000: "Phá hủy hoàn toàn hầu hết các công trình"
        }
        
        result = {}
        for threshold, description in sorted(damage_levels.items()):
            result[description] = (overpressure >= threshold)
        
        return result
    
    def radiation_effects(self, distance, energy_kt=None):
        """
        Tính toán các hiệu ứng bức xạ tại khoảng cách nhất định
        
        Returns:
            Dict chứa:
            - initial_radiation: Bức xạ ion hóa ban đầu (Gy)
            - fallout_radiation: Bức xạ phóng xạ rơi (Gy, 1 giờ sau vụ nổ)
            - lethal_radius: Bán kính gây tử vong do bức xạ (m)
        """
        if energy_kt is None:
            energy_kt = self.energy / 4.184e12
            
        # Bức xạ ion hóa ban đầu (sơ bộ)
        # Chỉ đáng kể trong phạm vi nhỏ (vài km) với vũ khí công suất thấp
        # Formula from Glasstone & Dolan
        initial_rad_factor = 0.10  # 10% năng lượng đi vào bức xạ ban đầu (tùy thuộc thiết kế vũ khí)
        initial_radiation = initial_rad_factor * energy_kt * 1e12 / (4 * np.pi * distance**2)
        initial_radiation = initial_radiation * np.exp(-distance/500)  # Suy giảm do hấp thụ không khí
        
        # Chuyển đổi sang đơn vị Gray (Gy)
        initial_radiation = initial_radiation / 1e4
        
        # Tính phóng xạ rơi (rất phức tạp, đây chỉ là ước tính)
        if self.altitude < 200:  # Chỉ áp dụng cho nổ mặt đất hoặc gần mặt đất
            # Sử dụng công thức Way-Wigner để ước tính
            fallout_factor = max(0, 1 - self.altitude/200) * 0.2
            fallout_radiation = fallout_factor * energy_kt * 1e3 / (distance**1.5)
            fallout_radiation = fallout_radiation * np.exp(-distance/1000)
        else:
            fallout_radiation = 0  # Nổ trên cao ít gây phóng xạ rơi
            
        # Bán kính gây tử vong do bức xạ (ước tính)
        lethal_dose = 5  # 5 Gy thường gây tử vong
        if initial_radiation > 0:
            lethal_radius = np.sqrt((initial_rad_factor * energy_kt * 1e12) / (4 * np.pi * lethal_dose * 1e4))
        else:
            lethal_radius = 0
            
        return {
            'initial_radiation': initial_radiation,
            'fallout_radiation': fallout_radiation,
            'lethal_radius': lethal_radius
        }
    
    def calculate_effects(self, distance, energy_kt=None):
        """
        Tính toán các hiệu ứng khác nhau tại khoảng cách cho trước
        
        Returns:
            Dict chứa:
            - max_overpressure: Áp suất dư tối đa (Pa)
            - arrival_time: Thời gian sóng xung kích tới (s)
            - dynamic_pressure: Áp suất động đỉnh (Pa)
            - wind_speed: Tốc độ gió đỉnh (m/s)
            - thermal_radiation: Bức xạ nhiệt (J/m²)
            - radiation: Hiệu ứng bức xạ (dict)
        """
        if energy_kt is None:
            energy_kt = self.energy / 4.184e12
        
        # Tìm thời điểm sóng xung kích tới vị trí này
        def distance_diff(t):
            return self.blast_radius(t) - distance
        
        # Giải phương trình để tìm thời gian tới (khi bán kính = khoảng cách)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = root_scalar(distance_diff, bracket=[0.1, 100], method='brentq')
                arrival_time = result.root if result.converged else None
        except:
            arrival_time = None
        
        if arrival_time is None or arrival_time <= 0:
            return {
                'max_overpressure': 0,
                'arrival_time': float('inf'),
                'dynamic_pressure': 0,
                'wind_speed': 0,
                'thermal_radiation': 0,
                'radiation': self.radiation_effects(distance, energy_kt)
            }
        
        # Tính áp suất dư đỉnh
        max_overpressure = self.overpressure(distance, arrival_time)
        
        # Tính áp suất động và tốc độ gió
        shock_velocity = self.blast_radius(arrival_time) / arrival_time
        wind_speed = 2 * shock_velocity / (self.gamma + 1)  # Từ quan hệ Rankine-Hugoniot
        dynamic_pressure = 0.5 * self.ambient_density * wind_speed**2
        
        # Mô hình bức xạ nhiệt (tương đối)
        # Khoảng 35% năng lượng chuyển thành bức xạ nhiệt trong nổ trên không
        thermal_factor = 0.35 * (1 - 0.5 * max(0, min(1, self.altitude/500)))
        
        # Hiệu chỉnh theo mật độ không khí
        attenuation = np.exp(-0.1 * distance/1000)  # Suy giảm qua khí quyển
        thermal_radiation = thermal_factor * self.energy * attenuation / (4 * np.pi * distance**2)
        
        # Thêm hiệu ứng bức xạ vào kết quả
        radiation = self.radiation_effects(distance, energy_kt)
        
        return {
            'max_overpressure': max_overpressure,
            'arrival_time': arrival_time,
            'dynamic_pressure': dynamic_pressure,
            'wind_speed': wind_speed,
            'thermal_radiation': thermal_radiation,
            'radiation': radiation
        }
    
    def visualize_blast_wave(self, simulation_data, time_index=None, show_damage=True, lang='vi'):
        """
        Hiển thị trực quan sự lan truyền của sóng xung kích
        
        Args:
            simulation_data: Kết quả từ hàm simulate_blast_wave()
            time_index: Chỉ số của thời điểm để hiển thị (None để hiển thị tất cả)
            show_damage: Có hiển thị ngưỡng thiệt hại hay không
            lang: Ngôn ngữ hiển thị ('vi' cho tiếng Việt, 'en' cho tiếng Anh)
        """
        times = simulation_data['times']
        distances = simulation_data['distances']
        pressures = simulation_data['pressures']
        
        # Chuẩn bị nhãn theo ngôn ngữ
        from ui.translator import translator as locale
        
        # Sử dụng translator thay vì hardcode các chuỗi ngôn ngữ
        current_lang = locale.current_lang
        locale.set_lang(lang)  # Tạm thời đặt ngôn ngữ theo tham số
        
        labels = {
            'pressure_time': locale.get_text("blast.chart_title", time=times[time_index] if time_index is not None else 0),
            'distance': locale.get_text("blast.x_axis"),
            'pressure': locale.get_text("blast.y_axis"),
            'window': locale.get_text("chart.window_breakage"),
            'moderate': locale.get_text("chart.moderate_damage"),
            'collapse': locale.get_text("chart.severe_damage"),
            'concrete': locale.get_text("chart.reinforced_damage"),
            'propagation': locale.get_text("blast.chart_title_animation"),
            'time': locale.get_text("chart.time_seconds"),
            'shock_front': locale.get_text("blast.shock_front")
        }
        
        if time_index is not None:
            # Vẽ đồ thị áp suất theo khoảng cách tại một thời điểm cụ thể
            plt.figure(figsize=(10, 6))
            plt.plot(distances, pressures[:, time_index])
            plt.title(labels['pressure_time'])
            plt.xlabel(labels['distance'])
            plt.ylabel(labels['pressure'])
            plt.grid(True)
            
            # Đánh dấu ngưỡng thiệt hại
            if show_damage:
                thresholds = [(3000, labels['window']), 
                             (7000, labels['moderate']),
                             (15000, labels['collapse']),
                             (35000, labels['concrete'])]
                for threshold, label in thresholds:
                    plt.axhline(y=threshold, color='r', linestyle='--', alpha=0.7)
                    plt.text(distances[-1]*0.8, threshold*1.1, label)
                
        else:
            # Tạo biểu đồ đường đồng mức của áp suất theo khoảng cách và thời gian
            plt.figure(figsize=(12, 8))
            X, Y = np.meshgrid(times, distances)
            
            # Sử dụng thang logarit để hiển thị tốt hơn
            levels = np.logspace(2, 6, 20)
            contour = plt.contourf(X, Y, pressures, levels=levels, 
                                  cmap='hot', norm=plt.cm.colors.LogNorm())
            
            # Thêm đường biểu diễn mặt sóng xung kích
            plt.plot(times, simulation_data['radius'], 'w--', linewidth=2, 
                    label=labels['shock_front'])
            
            plt.colorbar(contour, label=labels['pressure'])
            plt.title(labels['propagation'])
            plt.xlabel(labels['time'])
            plt.ylabel(labels['distance'])
            plt.legend()
            
        # Khôi phục ngôn ngữ ban đầu
        locale.set_lang(current_lang)
            
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, distances=[1000, 2000, 5000, 10000], lang='vi'):
        """
        Tạo báo cáo chi tiết về thiệt hại tại các khoảng cách cho trước
        
        Args:
            distances: Danh sách các khoảng cách (m) để đánh giá
            lang: Ngôn ngữ báo cáo ('vi' cho tiếng Việt, 'en' cho tiếng Anh)
        """
        # Sử dụng translator thay vì hardcode các chuỗi ngôn ngữ
        from ui.translator import translator as locale
        
        # Lưu ngôn ngữ hiện tại
        current_lang = locale.current_lang
        locale.set_lang(lang)  # Tạm thời đặt ngôn ngữ theo tham số
        
        # Chuẩn bị bản dịch từ hệ thống dịch
        translations = {
            'title': locale.get_text("blast.report.title").format(yield_kt=self.energy/4.184e12),
            'at_distance': locale.get_text("blast.report.at_distance"),
            'arrival': locale.get_text("blast.report.arrival"),
            'peak_pressure': locale.get_text("blast.report.peak_pressure"),
            'peak_wind': locale.get_text("blast.report.peak_wind"),
            'thermal': locale.get_text("blast.report.thermal"),
            'initial_rad': locale.get_text("blast.report.initial_rad"),
            'fallout': locale.get_text("blast.report.fallout"),
            'damage': locale.get_text("blast.report.damage"),
            'no_damage': locale.get_text("blast.report.no_damage"),
            'note': locale.get_text("blast.report.note"),
            'purpose': locale.get_text("blast.report.purpose")
        }
        
        print(translations['title'])
        print("-" * 50)
        
        for distance in distances:
            effects = self.calculate_effects(distance)
            
            print(translations['at_distance'].format(distance/1000))
            print(translations['arrival'].format(effects['arrival_time']))
            print(translations['peak_pressure'].format(effects['max_overpressure']/1000))
            print(translations['peak_wind'].format(effects['wind_speed'], effects['wind_speed']*3.6))
            print(translations['thermal'].format(effects['thermal_radiation']/1000))
            print(translations['initial_rad'].format(effects['radiation']['initial_radiation']))
            print(translations['fallout'].format(effects['radiation']['fallout_radiation']))
            
            # Đánh giá thiệt hại
            damage = self.damage_assessment(effects['max_overpressure'])
            print(translations['damage'])
            damage_found = False
            for description, is_damaged in damage.items():
                if is_damaged:
                    print(f"    - {description}")
                    damage_found = True
            
            if not damage_found:
                print(translations['no_damage'])
            
        print(translations['note'])
        print(translations['purpose'])
        
        # Khôi phục ngôn ngữ ban đầu
        locale.set_lang(current_lang)