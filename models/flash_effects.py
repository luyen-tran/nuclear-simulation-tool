import numpy as np
from scipy.special import erf

class FlashEffectsModel:
    def __init__(self, yield_kt=20, burst_height=0):
        self.yield_kt = yield_kt
        self.burst_height = burst_height
        self.total_energy = yield_kt * 4.184e12  # joules
        
        # Khoảng 30-35% năng lượng là ánh sáng khả kiến
        self.light_fraction = 0.33
        self.light_energy = self.total_energy * self.light_fraction
        
    def calculate_illuminance(self, distance):
        """Tính cường độ ánh sáng (lux) theo khoảng cách"""
        # Tính khoảng cách nghiêng
        if self.burst_height > 0:
            slant_range = np.sqrt(distance**2 + self.burst_height**2)
        else:
            slant_range = distance
            
        # Công thức gần đúng tính cường độ sáng
        # Quả cầu lửa có độ sáng tạm thời cực cao (~nhiều tỷ lux)
        peak_illuminance = 3e12 * self.yield_kt / (4 * np.pi * slant_range**2)
        
        # Điều chỉnh độ suy giảm theo khí quyển
        transmittance = np.exp(-0.1 * slant_range/1000)  # Giảm theo khoảng cách
        
        return peak_illuminance * transmittance
    
    def calculate_eye_effects(self, distances):
        """Tính tác động đến mắt ở các khoảng cách"""
        illuminance_values = np.array([self.calculate_illuminance(d) for d in distances])
        
        # Ngưỡng gây hại cho mắt (lux)
        temporary_flash_blindness = 1e7  # Mù tạm thời
        retinal_burn_threshold = 1e9     # Bỏng võng mạc
        permanent_blindness = 5e9        # Mù vĩnh viễn
        
        # Tính xác suất tác động
        p_flash_blindness = 0.5 * (1 + erf((illuminance_values - temporary_flash_blindness) / (temporary_flash_blindness*0.2)))
        p_retinal_burn = 0.5 * (1 + erf((illuminance_values - retinal_burn_threshold) / (retinal_burn_threshold*0.2)))
        p_permanent_damage = 0.5 * (1 + erf((illuminance_values - permanent_blindness) / (permanent_blindness*0.2)))
        
        return {
            'distances': distances,
            'illuminance': illuminance_values,
            'temporary_blindness_probability': p_flash_blindness,
            'retinal_burn_probability': p_retinal_burn,
            'permanent_damage_probability': p_permanent_damage
        } 