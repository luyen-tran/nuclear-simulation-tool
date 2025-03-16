import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class FalloutModel:
    def __init__(self, yield_kt=20, fission_fraction=0.5, burst_height=0):
        self.yield_kt = yield_kt
        self.fission_fraction = fission_fraction  # tỷ lệ năng lượng phân hạch
        self.burst_height = burst_height  # m
        
        # Hằng số phân rã của một số đồng vị chính
        self.isotopes = {
            'I-131': {'half_life': 8.02 * 24 * 3600, 'yield': 0.029},
            'Cs-137': {'half_life': 30.17 * 365.25 * 24 * 3600, 'yield': 0.061},
            'Sr-90': {'half_life': 28.8 * 365.25 * 24 * 3600, 'yield': 0.058},
            'Ba-140': {'half_life': 12.75 * 24 * 3600, 'yield': 0.062}
        }
    
    def calculate_initial_activity(self):
        """Tính hoạt độ phóng xạ ban đầu của các đồng vị"""
        # 1kt phân hạch tạo ra khoảng 1.45e23 phân hạch
        fissions = 1.45e23 * self.yield_kt * self.fission_fraction
        
        initial_activities = {}
        for isotope, data in self.isotopes.items():
            # Tính toán hoạt độ ban đầu dựa trên năng suất và số phân hạch
            decay_constant = np.log(2) / data['half_life']  # 1/s
            initial_amount = fissions * data['yield']
            initial_activities[isotope] = initial_amount * decay_constant  # Bq
            
        return initial_activities
    
    def calculate_dose_rate(self, distance, time):
        """Tính tốc độ liều lượng phóng xạ theo khoảng cách và thời gian"""
        # Công thức t^-1.2 của Way-Wigner
        if self.burst_height > 100:  # Nổ trên cao
            # Mưa phóng xạ giảm đáng kể
            return 0.0
            
        # Nổ mặt đất hoặc gần mặt đất
        initial_activities = self.calculate_initial_activity()
        
        dose_rate = 0
        for isotope, data in self.isotopes.items():
            decay_constant = np.log(2) / data['half_life']
            activity = initial_activities[isotope] * np.exp(-decay_constant * time)
            
            # Giảm theo khoảng cách và thay đổi theo thời gian
            # Phóng xạ ban đầu phân bố không đều
            if distance < 1:  # Trong vòng 1km
                dose_contribution = activity * 0.5 / (4 * np.pi)
            else:
                dose_contribution = activity * 0.5 / (4 * np.pi * distance**2)
                
            # Giảm theo độ sâu
            attenuation = np.exp(-0.01 * distance)
            dose_rate += dose_contribution * attenuation
            
        # Way-Wigner: R = R₁·t^(-1.2)
        way_wigner_factor = (time / 3600)**(-1.2) if time > 3600 else 1.0
        
        return dose_rate * way_wigner_factor
    
    def simulate_fallout_pattern(self, max_distance=100, wind_speed=10, 
                               wind_direction=0, times=[1, 24, 168, 720]):
        """Mô phỏng mẫu mưa phóng xạ theo gió"""
        # Tạo lưới điểm
        x = np.linspace(-max_distance, max_distance, 100)
        y = np.linspace(-max_distance, max_distance, 100)
        X, Y = np.meshgrid(x, y)
        
        results = {}
        for time_hours in times:
            time_seconds = time_hours * 3600
            dose_rate = np.zeros_like(X)
            
            # Tính mô hình mưa phóng xạ
            for i in range(len(x)):
                for j in range(len(y)):
                    # Tính khoảng cách từ tâm
                    distance = np.sqrt(X[i,j]**2 + Y[i,j]**2)
                    
                    # Ảnh hưởng của gió
                    # Gió thổi theo hướng chỉ định
                    wx = X[i,j] + wind_speed * time_hours * np.cos(wind_direction)
                    wy = Y[i,j] + wind_speed * time_hours * np.sin(wind_direction)
                    wind_distance = np.sqrt(wx**2 + wy**2)
                    
                    # Kết hợp khoảng cách thực và ảnh hưởng gió
                    effective_distance = 0.3 * distance + 0.7 * wind_distance
                    
                    dose_rate[i,j] = self.calculate_dose_rate(effective_distance, time_seconds)
            
            results[f"{time_hours}h"] = dose_rate
            
        return {
            'grid_x': X,
            'grid_y': Y,
            'dose_rates': results
        } 