import numpy as np
import matplotlib.pyplot as plt

class EMPModel:
    def __init__(self, yield_kt=20, burst_height=30, ground_conductivity=0.005):
        self.yield_kt = yield_kt
        self.burst_height = burst_height  # km
        self.ground_conductivity = ground_conductivity  # S/m
        self.total_energy = yield_kt * 4.184e12  # joules
        
    def calculate_emp_field_strength(self, distances):
        """Tính cường độ trường EMP theo khoảng cách"""
        # Cường độ trường EMP thay đổi theo độ cao và năng lượng vụ nổ
        emp_factor = 50000 * np.sqrt(self.yield_kt)  # V/m
        
        # Hiệu chỉnh theo độ cao nổ (cao hơn tạo EMP mạnh hơn)
        height_factor = 1.0 + (self.burst_height / 10)
        
        # Hiệu chỉnh theo độ dẫn điện mặt đất
        ground_factor = 1.0 - 0.3 * self.ground_conductivity / 0.01
        
        # Tính cường độ trường EMP theo khoảng cách
        field_strength = []
        for distance in distances:
            # Giảm theo khoảng cách
            if distance < 5:  # Trong vòng 5km
                strength = emp_factor * height_factor * ground_factor
            else:
                strength = emp_factor * height_factor * ground_factor * (5 / distance)**1.3
            field_strength.append(strength)
            
        return np.array(field_strength)
    
    def calculate_emp_effects(self, distances):
        """Tính tác động của EMP ở các khoảng cách khác nhau"""
        field_strength = self.calculate_emp_field_strength(distances)
        
        # Xác suất gây hại cho các thiết bị điện tử
        electronic_damage_prob = 1.0 - np.exp(-field_strength / 20000)
        power_grid_damage_prob = 1.0 - np.exp(-field_strength / 10000)
        communication_damage_prob = 1.0 - np.exp(-field_strength / 15000)
        
        return {
            'distances': distances,
            'field_strength': field_strength,  # V/m
            'electronic_damage_probability': electronic_damage_prob,
            'power_grid_damage_probability': power_grid_damage_prob,
            'communication_damage_probability': communication_damage_prob
        } 