import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

class FalloutModel:
    def __init__(self, yield_kt=20, fission_fraction=0.5, burst_height=0, soil_type="normal"):
        """
        Khởi tạo mô hình mưa phóng xạ hạt nhân.
        
        Tham số:
            yield_kt: Năng lượng vụ nổ (kiloton TNT)
            fission_fraction: Tỷ lệ năng lượng từ phản ứng phân hạch (0-1)
            burst_height: Độ cao vụ nổ (mét)
            soil_type: Loại đất ảnh hưởng đến mưa phóng xạ ("normal", "dry", "wet")
        """
        self.yield_kt = yield_kt
        self.fission_fraction = fission_fraction
        self.burst_height = burst_height
        self.soil_type = soil_type
        
        # Tác động của loại đất đến mưa phóng xạ
        self.soil_factors = {
            "dry": 0.7,     # Đất khô làm giảm lượng phóng xạ cuốn theo
            "normal": 1.0,  # Điều kiện chuẩn
            "wet": 1.3      # Đất ẩm ướt làm tăng lượng phóng xạ cuốn theo
        }
        
        # Đồng vị phóng xạ chính và đặc tính
        # Thời gian bán rã (giây), năng suất (tỷ lệ đồng vị/phân hạch), năng lượng phát xạ (MeV)
        self.isotopes = {
            'I-131': {'half_life': 8.02 * 24 * 3600, 'yield': 0.029, 'energy': 0.606},
            'Cs-137': {'half_life': 30.17 * 365.25 * 24 * 3600, 'yield': 0.061, 'energy': 0.662},
            'Sr-90': {'half_life': 28.8 * 365.25 * 24 * 3600, 'yield': 0.058, 'energy': 0.546},
            'Ba-140': {'half_life': 12.75 * 24 * 3600, 'yield': 0.062, 'energy': 0.537},
            'Ce-141': {'half_life': 32.5 * 24 * 3600, 'yield': 0.057, 'energy': 0.145},
            'Zr-95': {'half_life': 64.0 * 24 * 3600, 'yield': 0.065, 'energy': 0.757},
            'Ru-103': {'half_life': 39.3 * 24 * 3600, 'yield': 0.03, 'energy': 0.497}
        }
        
        # Hệ số chuyển đổi từ hoạt độ sang liều lượng hiệu dụng (Sv/Bq)
        self.dose_conversion_factors = {
            'I-131': 2.2e-8,
            'Cs-137': 1.3e-8,
            'Sr-90': 2.8e-8,
            'Ba-140': 1.0e-8,
            'Ce-141': 7.1e-9,
            'Zr-95': 9.5e-9,
            'Ru-103': 7.3e-9
        }
        
        # Tính toán diện tích mưa phóng xạ dựa trên năng lượng vụ nổ
        self.fallout_radius = self._calculate_fallout_radius()
    
    def _calculate_fallout_radius(self):
        """Tính toán bán kính ảnh hưởng của mưa phóng xạ (km)"""
        # Công thức thực nghiệm: r = k * W^0.5 với W là năng lượng vụ nổ (kt)
        # và k là hằng số phụ thuộc vào chiều cao vụ nổ
        if self.burst_height <= 0:  # Nổ mặt đất
            k = 2.5
        elif self.burst_height < 100:  # Nổ thấp
            k = 1.8
        else:  # Nổ trên cao
            k = 0.8
        
        return k * np.sqrt(self.yield_kt * self.fission_fraction)
    
    def calculate_initial_activity(self):
        """
        Tính toán hoạt độ phóng xạ ban đầu của các đồng vị.
        
        Mỗi kiloton (kt) phân hạch tạo ra khoảng 1.45e23 phản ứng phân hạch,
        mỗi phản ứng tạo ra một số đồng vị phóng xạ theo tỷ lệ khác nhau.
        
        Trả về:
            Dictionary chứa hoạt độ ban đầu (Bq) của mỗi đồng vị
        """
        # Số phản ứng phân hạch dựa trên năng lượng vụ nổ và tỷ lệ phân hạch
        fissions = 1.45e23 * self.yield_kt * self.fission_fraction
        
        initial_activities = {}
        for isotope, data in self.isotopes.items():
            # Hằng số phân rã λ = ln(2)/t_half
            decay_constant = np.log(2) / data['half_life']  # 1/s
            
            # Số nguyên tử ban đầu = số phân hạch * năng suất đồng vị
            initial_amount = fissions * data['yield']
            
            # Hoạt độ ban đầu (Bq) = λ * N
            initial_activities[isotope] = initial_amount * decay_constant
            
        return initial_activities
    
    def calculate_dose_rate(self, distance, time, height=0):
        """
        Tính tốc độ liều lượng phóng xạ theo khoảng cách, thời gian và độ cao.
        
        Tham số:
            distance: Khoảng cách từ điểm nổ (km)
            time: Thời gian sau vụ nổ (giây)
            height: Độ cao so với mặt đất (m)
            
        Trả về:
            Tốc độ liều lượng (Sv/h) tại vị trí và thời điểm cụ thể
        """
        # Kiểm tra nổ trên cao để xác định mức độ mưa phóng xạ
        fallout_factor = 1.0
        if self.burst_height > 0:
            # Mưa phóng xạ giảm theo độ cao vụ nổ
            fallout_factor = np.exp(-self.burst_height / 300)
        
        if self.burst_height > 1000:  # Nổ tầng cao (airburst)
            return 0.0  # Không có mưa phóng xạ đáng kể
        
        # Hệ số liên quan đến đất (ảnh hưởng đến lượng vật chất bị cuốn theo)
        soil_factor = self.soil_factors.get(self.soil_type, 1.0)
        
        # Tính hoạt độ ban đầu của các đồng vị
        initial_activities = self.calculate_initial_activity()
        
        # Tính liều lượng tổng từ mỗi đồng vị
        dose_rate = 0
        for isotope, data in self.isotopes.items():
            # Hằng số phân rã
            decay_constant = np.log(2) / data['half_life']
            
            # Hoạt độ tại thời điểm t (theo luật phân rã phóng xạ)
            activity = initial_activities[isotope] * np.exp(-decay_constant * time)
            
            # Hệ số chuyển đổi từ hoạt độ sang liều lượng
            dose_conv = self.dose_conversion_factors[isotope]
            
            # Tính liều lượng dựa trên khoảng cách (giảm theo hàm nghịch đảo bình phương)
            if distance < 0.001:  # Tránh chia cho 0
                distance = 0.001
                
            # Phân bố theo khoảng cách (mô hình Gaussian cải tiến)
            distance_factor = np.exp(-(distance**2) / (2 * (self.fallout_radius/3)**2))
            
            # Hiệu ứng độ cao - phóng xạ giảm theo độ cao
            height_factor = np.exp(-height / 100)
            
            # Đóng góp liều lượng từ đồng vị này
            energy_factor = data['energy'] / 0.5  # Chuẩn hóa theo năng lượng trung bình 0.5 MeV
            dose_contribution = activity * dose_conv * distance_factor * height_factor * energy_factor
            
            dose_rate += dose_contribution
        
        # Áp dụng công thức Way-Wigner (t^-1.2) cho sự suy giảm tổng
        # Chỉ áp dụng sau 1 giờ để tránh giá trị quá lớn ở thời điểm ban đầu
        if time > 3600:
            way_wigner_factor = (time / 3600)**(-1.2)
        else:
            way_wigner_factor = 1.0
        
        # Kết hợp các yếu tố
        final_dose_rate = dose_rate * way_wigner_factor * fallout_factor * soil_factor
        
        # Chuyển đổi sang đơn vị Sv/h
        return final_dose_rate * 3600
    
    def simulate_fallout_pattern(self, max_distance=100, resolution=100, wind_speed=10, 
                               wind_direction=0, stability_class='D', times=[1, 24, 168, 720]):
        """
        Mô phỏng mẫu mưa phóng xạ theo điều kiện môi trường.
        
        Tham số:
            max_distance: Khoảng cách tối đa từ tâm vụ nổ (km)
            resolution: Độ phân giải của lưới điểm
            wind_speed: Tốc độ gió (km/h)
            wind_direction: Hướng gió (rad), 0 là hướng Đông, π/2 là hướng Bắc
            stability_class: Phân loại ổn định Pasquill-Gifford ('A' đến 'F')
            times: Danh sách các mốc thời gian (giờ) để mô phỏng
            
        Trả về:
            Dictionary chứa lưới tọa độ và liều lượng tại các thời điểm
        """
        # Tạo lưới điểm
        x = np.linspace(-max_distance, max_distance, resolution)
        y = np.linspace(-max_distance, max_distance, resolution)
        X, Y = np.meshgrid(x, y)
        
        # Hệ số khuếch tán theo phân loại ổn định khí quyển
        stability_factors = {
            'A': 0.18,  # Rất không ổn định - khuếch tán mạnh
            'B': 0.14,  # Không ổn định vừa
            'C': 0.10,  # Hơi không ổn định
            'D': 0.06,  # Trung tính
            'E': 0.04,  # Hơi ổn định
            'F': 0.02   # Rất ổn định - khuếch tán yếu
        }
        diffusion_factor = stability_factors.get(stability_class, 0.06)
        
        results = {}
        for time_hours in times:
            time_seconds = time_hours * 3600
            dose_rate = np.zeros_like(X)
            
            # Tính toán trên lưới điểm
            for i in range(len(x)):
                for j in range(len(y)):
                    # Tọa độ điểm hiện tại
                    point_x, point_y = X[i,j], Y[i,j]
                    
                    # Khoảng cách từ tâm vụ nổ
                    distance = np.sqrt(point_x**2 + point_y**2)
                    
                    # Chuyển tọa độ sang hệ quy chiếu gió
                    # Góc giữa vector vị trí và vector gió
                    angle = np.arctan2(point_y, point_x) - wind_direction
                    
                    # Thành phần dọc và ngang so với hướng gió
                    along_wind = distance * np.cos(angle)
                    cross_wind = distance * np.sin(angle)
                    
                    # Mô hình Gaussian cải tiến cho mưa phóng xạ
                    # Tâm mưa phóng xạ dịch chuyển theo gió
                    wind_displacement = wind_speed * time_hours
                    
                    # Khoảng cách hiệu dụng bị ảnh hưởng bởi gió và khuếch tán
                    sigma_y = diffusion_factor * np.sqrt(wind_displacement)  # Khuếch tán ngang
                    
                    # Vị trí tương đối so với tâm mưa phóng xạ dịch chuyển
                    dx = along_wind - wind_displacement
                    dy = cross_wind
                    
                    # Hệ số suy giảm theo khoảng cách ngang với hướng gió
                    crosswind_factor = np.exp(-(dy**2) / (2 * sigma_y**2))
                    
                    # Hệ số phân bố theo hướng gió (hàm mũ có điều chỉnh)
                    if dx < 0:  # Phía trước tâm dịch chuyển
                        alongwind_factor = np.exp(-np.abs(dx) / (wind_displacement/3))
                    else:  # Phía sau tâm dịch chuyển (kéo dài hơn)
                        alongwind_factor = np.exp(-dx / (wind_displacement/1.5))
                    
                    # Tính khoảng cách hiệu dụng có tính đến các yếu tố ảnh hưởng
                    effective_distance = distance * (1 - 0.7 * crosswind_factor * alongwind_factor)
                    
                    # Tính liều lượng tại điểm này
                    dose_rate[i,j] = self.calculate_dose_rate(effective_distance, time_seconds)
            
            results[f"{time_hours}h"] = dose_rate
        
        return {
            'grid_x': X,
            'grid_y': Y,
            'dose_rates': results
        }
    
    def estimate_fallout_arrival(self, distance, wind_speed):
        """
        Ước tính thời gian mưa phóng xạ đến một địa điểm cụ thể.
        
        Tham số:
            distance: Khoảng cách từ vụ nổ (km)
            wind_speed: Tốc độ gió (km/h)
            
        Trả về:
            Thời gian ước tính mưa phóng xạ đến địa điểm (giờ)
        """
        # Tính toán thời gian ước tính (giờ)
        if wind_speed < 0.1:  # Tránh chia cho 0
            wind_speed = 0.1
            
        # Thời gian = khoảng cách / tốc độ, có điều chỉnh theo độ cao mây nấm
        cloud_height_factor = 1 + 0.2 * np.log10(self.yield_kt)
        
        return (distance / wind_speed) * cloud_height_factor
    
    def calculate_integrated_dose(self, distance, time_start, time_end, wind_speed=10, wind_direction=0):
        """
        Tính toán liều tích lũy trong khoảng thời gian từ time_start đến time_end.
        
        Tham số:
            distance: Khoảng cách từ tâm vụ nổ (km)
            time_start: Thời gian bắt đầu tích lũy (giờ)
            time_end: Thời gian kết thúc tích lũy (giờ)
            wind_speed: Tốc độ gió (km/h)
            wind_direction: Hướng gió (rad)
            
        Trả về:
            Liều tích lũy (Sv) trong khoảng thời gian chỉ định
        """
        # Chuyển đổi thời gian từ giờ sang giây
        t_start = time_start * 3600
        t_end = time_end * 3600
        
        # Tính thời gian mưa phóng xạ đến địa điểm (giờ)
        arrival_time = self.estimate_fallout_arrival(distance, wind_speed) * 3600
        
        # Nếu mưa phóng xạ chưa đến trong khoảng thời gian xét
        if arrival_time > t_end:
            return 0.0
        
        # Điều chỉnh thời gian bắt đầu nếu mưa phóng xạ đến sau thời điểm bắt đầu
        if arrival_time > t_start:
            t_start = arrival_time
        
        # Số điểm lấy mẫu để tính tích phân
        num_samples = 50
        
        # Thời gian lấy mẫu (thang logarit để bắt được sự thay đổi nhanh ở đầu)
        if t_start < 1:  # Tránh log(0)
            t_start = 1
        
        log_times = np.logspace(np.log10(t_start), np.log10(t_end), num_samples)
        
        # Tính liều lượng tại mỗi thời điểm
        dose_rates = []
        for t in log_times:
            # Tính góc giữa vector vị trí và vector gió
            # Đơn giản hóa bằng cách xét khoảng cách hiệu dụng
            wind_displacement = (wind_speed * (t / 3600)) / distance
            wind_effect = 1 - 0.5 * wind_displacement if wind_displacement < 1 else 0.5
            
            effective_distance = distance * wind_effect
            dose_rates.append(self.calculate_dose_rate(effective_distance, t))
        
        # Tích phân số để tính liều tích lũy (phương pháp hình thang)
        integrated_dose = 0
        for i in range(1, len(log_times)):
            dt = log_times[i] - log_times[i-1]
            avg_dose_rate = (dose_rates[i] + dose_rates[i-1]) / 2
            integrated_dose += avg_dose_rate * dt
        
        # Trả về liều tích lũy (Sv)
        return integrated_dose 