import numpy as np
from scipy.special import erf

class FlashEffectsModel:
    """
    Mô hình tính toán hiệu ứng ánh sáng hạt nhân.
    Mô phỏng cường độ ánh sáng và tác động đến mắt từ vụ nổ hạt nhân.
    """
    def __init__(self, yield_kt=20, burst_height=0, day_condition="Ngày"):
        """
        Khởi tạo mô hình hiệu ứng ánh sáng.
        
        Tham số:
            yield_kt (float): Năng lượng vụ nổ (kiloton TNT)
            burst_height (float): Độ cao vụ nổ (mét)
            day_condition (str): Điều kiện thời gian trong ngày ("Ngày", "Chạng vạng", "Đêm")
        """
        # Thông số cơ bản
        self.yield_kt = yield_kt
        self.burst_height = burst_height  # mét
        self.total_energy = yield_kt * 4.184e12  # joules (1 kt = 4.184e12 J)
        
        # Hệ số điều chỉnh theo thời gian trong ngày
        self.day_condition = day_condition
        self.pupil_dilation = {
            "Ngày": 1.0,
            "Chạng vạng": 1.5,
            "Đêm": 2.5
        }
        self.dilation_factor = self.pupil_dilation.get(day_condition, 1.0)
        
        # Phân bổ năng lượng ánh sáng
        # Khoảng 30-35% năng lượng là ánh sáng khả kiến và bức xạ nhiệt
        self.light_fraction = 0.33
        self.light_energy = self.total_energy * self.light_fraction
        
        # Các ngưỡng gây hại cho mắt (lux)
        # Dựa trên nghiên cứu khoa học và dữ liệu thực nghiệm
        self.flash_blindness_threshold = 7e3   # Mù tạm thời
        self.retinal_burn_threshold = 6e5      # Bỏng võng mạc
        self.permanent_damage_threshold = 4e6  # Mù vĩnh viễn
        
    def calculate_illuminance(self, distance_km):
        """
        Tính cường độ ánh sáng (lux) theo khoảng cách.
        
        Công thức mở rộng kết hợp:
          - Suy giảm bình phương nghịch (inverse square law)
          - Suy giảm qua khí quyển (atmospheric attenuation)
          - Hiệu ứng hấp thụ và tán xạ
        
        Tham số:
            distance_km (float): Khoảng cách ngang tính từ tâm vụ nổ (km)
            
        Trả về:
            float: Cường độ ánh sáng tại khoảng cách đó (lux)
        """
        # Chuyển đổi đơn vị
        distance_m = distance_km * 1000  # Chuyển km thành m
        
        # Tính khoảng cách nghiêng (đường thẳng từ điểm nổ đến điểm quan sát)
        if self.burst_height > 0:
            slant_range_m = np.sqrt(distance_m**2 + self.burst_height**2)
        else:
            slant_range_m = distance_m
        
        # Chuyển lại sang km để tính suy giảm khí quyển
        slant_range_km = slant_range_m / 1000
        
        # Mô hình cải tiến dựa trên công thức Y^(2/3) để phù hợp với dữ liệu thực nghiệm
        # Quả cầu lửa có độ sáng tạm thời cực cao (nhiều tỷ lux)
        # Công thức này kết hợp hiệu ứng kích thước quả cầu lửa theo năng lượng
        base_illuminance = 9e9 * (self.yield_kt**(2/3)) / (slant_range_km**2)
        
        # Hệ số suy giảm khí quyển phụ thuộc khoảng cách và độ cao
        # Tham số 10 là hệ số điều chỉnh để phù hợp với dữ liệu thực tế
        attenuation_factor = np.exp(-slant_range_km/(self.burst_height/1000 + 10))
        
        return base_illuminance * attenuation_factor
    
    def calculate_eye_effects(self, distances_km):
        """
        Tính tác động đến mắt ở các khoảng cách khác nhau.
        
        Tham số:
            distances_km (array): Mảng các khoảng cách (km) cần tính
            
        Trả về:
            dict: Từ điển chứa kết quả tính toán xác suất tổn thương mắt
        """
        # Tính cường độ ánh sáng tại mỗi khoảng cách
        illuminance_values = np.array([self.calculate_illuminance(d) for d in distances_km])
        
        # Điều chỉnh theo độ giãn đồng tử (thời gian trong ngày)
        adjusted_illuminance = illuminance_values * self.dilation_factor
        
        # Sử dụng hàm sigmoid cải tiến để tính xác suất tổn thương
        # Công thức: p = 1 - 1/(1 + exp((I - Threshold)/(Threshold*scale)))
        # Hệ số 0.1 điều chỉnh độ dốc của đường cong xác suất
        flash_blindness_prob = 1 - 1/(1 + np.exp((adjusted_illuminance - self.flash_blindness_threshold)/(self.flash_blindness_threshold*0.1)))
        retinal_burn_prob = 1 - 1/(1 + np.exp((adjusted_illuminance - self.retinal_burn_threshold)/(self.retinal_burn_threshold*0.1)))
        permanent_damage_prob = 1 - 1/(1 + np.exp((adjusted_illuminance - self.permanent_damage_threshold)/(self.permanent_damage_threshold*0.1)))
        
        # Đảm bảo các xác suất nằm trong khoảng [0, 1]
        flash_blindness_prob = np.clip(flash_blindness_prob, 0, 1)
        retinal_burn_prob = np.clip(retinal_burn_prob, 0, 1)
        permanent_damage_prob = np.clip(permanent_damage_prob, 0, 1)
        
        return {
            'distances': distances_km,
            'illuminance': illuminance_values,
            'temporary_blindness_probability': flash_blindness_prob,
            'retinal_burn_probability': retinal_burn_prob,
            'permanent_damage_probability': permanent_damage_prob
        }
    
    def set_day_condition(self, condition):
        """
        Cập nhật điều kiện thời gian trong ngày.
        
        Tham số:
            condition (str): Điều kiện thời gian ("Ngày", "Chạng vạng", "Đêm")
        """
        self.day_condition = condition
        self.dilation_factor = self.pupil_dilation.get(condition, 1.0)
        
    def get_max_effect_distance(self, effect_type="temporary_blindness", probability=0.5):
        """
        Ước tính khoảng cách tối đa mà tác động cụ thể có xác suất xảy ra lớn hơn ngưỡng cho trước.
        
        Tham số:
            effect_type (str): Loại tác động ("temporary_blindness", "retinal_burn", "permanent_damage")
            probability (float): Ngưỡng xác suất (0-1)
            
        Trả về:
            float: Khoảng cách tối đa (km) có xác suất ảnh hưởng lớn hơn ngưỡng
        """
        # Mảng khoảng cách để tìm kiếm
        test_distances = np.logspace(-1, 2, 200)  # Từ 0.1 đến 100 km
        
        # Tính các tác động
        effects = self.calculate_eye_effects(test_distances)
        
        # Lấy mảng xác suất tương ứng
        if effect_type == "temporary_blindness":
            prob_array = effects['temporary_blindness_probability']
        elif effect_type == "retinal_burn":
            prob_array = effects['retinal_burn_probability']
        elif effect_type == "permanent_damage":
            prob_array = effects['permanent_damage_probability']
        else:
            return 0
        
        # Tìm điểm xa nhất có xác suất lớn hơn ngưỡng
        indices = np.where(prob_array >= probability)[0]
        
        if len(indices) > 0:
            max_index = indices[-1]
            return test_distances[max_index]
        else:
            return 0 