import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class NuclearWeaponDesignModel:
    """
    Mô hình mô phỏng thiết kế vũ khí hạt nhân
    Hỗ trợ ba loại vũ khí chính: phân hạch, phân hạch tăng cường và nhiệt hạch
    """
    def __init__(self, weapon_type="fission", yield_kt=20, enrichment_level=0.93, temperature=300):
        """
        Khởi tạo mô hình thiết kế vũ khí hạt nhân
        
        Tham số:
            weapon_type (str): Loại vũ khí ("fission", "boosted", "thermonuclear")
            yield_kt (float): Năng lượng dự kiến tính bằng kiloton TNT
            enrichment_level (float): Mức độ làm giàu của vật liệu hạt nhân (0-1)
            temperature (float): Nhiệt độ môi trường tính bằng Kelvin
        """
        self.weapon_type = weapon_type
        self.yield_kt = yield_kt
        self.enrichment_level = enrichment_level
        self.temperature = temperature
        self.constants = {
            "fission_energy_u235": 8.2e13,  # J/kg - Năng lượng phân hạch U-235
            "fission_energy_pu239": 8.8e13,  # J/kg - Năng lượng phân hạch Pu-239
            "fusion_energy_dt": 3.4e14,     # J/kg - Năng lượng tổng hợp D-T
            "fusion_energy_li6dt": 2.9e14,  # J/kg - Năng lượng tổng hợp Li6-DT
            "kt_to_joules": 4.184e12,       # Chuyển đổi từ kt sang J
            "critical_mass_u235": 52,       # kg - Khối lượng tới hạn U-235
            "critical_mass_pu239": 10       # kg - Khối lượng tới hạn Pu-239
        }
        
    def validate_inputs(self):
        """
        Kiểm tra tính hợp lệ của các tham số đầu vào
        
        Trả về:
            bool: True nếu tất cả các tham số hợp lệ, False nếu không
            str: Thông báo lỗi nếu có
        """
        if self.weapon_type not in ["fission", "boosted", "thermonuclear"]:
            return False, f"Loại vũ khí '{self.weapon_type}' không được hỗ trợ. Hỗ trợ: fission, boosted, thermonuclear"
            
        if self.yield_kt <= 0:
            return False, f"Năng lượng phải dương, giá trị hiện tại: {self.yield_kt} kt"
            
        if not 0 < self.enrichment_level <= 1:
            return False, f"Mức độ làm giàu phải nằm trong khoảng (0, 1], giá trị hiện tại: {self.enrichment_level}"
            
        if self.temperature <= 0:
            return False, f"Nhiệt độ phải dương, giá trị hiện tại: {self.temperature} K"
            
        # Giới hạn hợp lý cho từng loại vũ khí
        if self.weapon_type == "fission" and self.yield_kt > 500:
            return False, f"Vũ khí phân hạch thường có năng lượng dưới 500kt, giá trị hiện tại: {self.yield_kt} kt"
            
        return True, "Tham số hợp lệ"
        
    def calculate_efficiency(self, design_params):
        """
        Tính toán hiệu suất dựa trên các tham số thiết kế
        
        Tham số:
            design_params (dict): Từ điển chứa các tham số thiết kế
            
        Trả về:
            float: Hiệu suất ước tính (0-1)
        """
        # Kiểm tra tính hợp lệ
        valid, message = self.validate_inputs()
        if not valid:
            raise ValueError(message)
            
        if self.weapon_type == "fission":
            # Thiết kế phân hạch đơn giản
            implosion_quality = design_params.get("implosion_quality", 0.7)  # Chất lượng của cơ chế nén
            neutron_initiator = design_params.get("neutron_initiator", 0.8)  # Hiệu quả của bộ khơi mào nơtron
            tamper_effectiveness = design_params.get("tamper_effectiveness", 0.6)  # Hiệu quả của lớp vỏ bọc
            fissile_purity = design_params.get("fissile_purity", self.enrichment_level)  # Độ tinh khiết nguyên liệu
            
            # Mô hình cải thiện: Xem xét ảnh hưởng của nhiệt độ và các yếu tố phi tuyến
            temp_factor = 1.0 - 0.001 * max(0, self.temperature - 300)  # Hiệu suất giảm khi nhiệt độ tăng
            
            # Hiệu suất phân hạch cơ bản khoảng 1-20%, phụ thuộc phi tuyến vào các yếu tố
            base_efficiency = 0.01 + 0.22 * np.power(implosion_quality, 1.2) * neutron_initiator * tamper_effectiveness
            
            # Mức độ làm giàu ảnh hưởng đáng kể đến hiệu suất
            enrichment_factor = np.power(fissile_purity, 1.5)
            
            efficiency = base_efficiency * enrichment_factor * temp_factor
            
        elif self.weapon_type == "boosted":
            # Thiết kế phân hạch được tăng cường bằng phản ứng tổng hợp DT
            fission_efficiency = design_params.get("fission_efficiency", 0.1)  # Hiệu suất phân hạch cơ bản
            tritium_amount = design_params.get("tritium_amount", 0.5)  # Lượng tritium (0-1)
            deuterium_amount = design_params.get("deuterium_amount", 0.5)  # Lượng deuterium (0-1)
            compression_quality = design_params.get("compression_quality", 0.8)  # Chất lượng nén
            
            # Hiệu ứng synergy - phản ứng DT sản sinh nơtron nhanh tăng cường phân hạch
            dt_synergy = np.sqrt(tritium_amount * deuterium_amount) * compression_quality
            
            # Tăng cường có thể tăng hiệu suất lên 2-4 lần, phụ thuộc vào chất lượng
            efficiency = fission_efficiency * (1 + 3 * dt_synergy)
            
            # Yếu tố giới hạn - quá nhiều tritium không cải thiện hiệu suất tuyến tính
            if tritium_amount > 0.7:
                efficiency *= 0.7 + 0.3 * (1 - tritium_amount) / 0.3
            
        elif self.weapon_type == "thermonuclear":
            # Thiết kế nhiệt hạch hai giai đoạn (Teller-Ulam)
            primary_yield_fraction = design_params.get("primary_yield_fraction", 0.2)  # % năng lượng từ giai đoạn đầu
            coupling_efficiency = design_params.get("coupling_efficiency", 0.7)  # Hiệu quả truyền năng lượng
            secondary_burn = design_params.get("secondary_burn", 0.3)  # Mức độ cháy của giai đoạn 2
            radiation_case_quality = design_params.get("radiation_case_quality", 0.8)  # Chất lượng vỏ bức xạ
            
            # Hiệu suất giai đoạn 1 (phân hạch)
            primary_params = {
                "implosion_quality": design_params.get("primary_implosion_quality", 0.75),
                "neutron_initiator": design_params.get("primary_neutron_initiator", 0.85),
                "tamper_effectiveness": design_params.get("primary_tamper_effectiveness", 0.7),
                "fissile_purity": self.enrichment_level
            }
            
            # Gọi đệ quy để tính hiệu suất của giai đoạn đầu
            primary_model = NuclearWeaponDesignModel("fission", self.yield_kt * primary_yield_fraction, 
                                                   self.enrichment_level, self.temperature)
            primary_efficiency = primary_model.calculate_efficiency(primary_params)
            
            # Hiệu suất giai đoạn 2 (tổng hợp) phụ thuộc vào nhiều yếu tố phức tạp
            radiation_coupling = coupling_efficiency * radiation_case_quality
            fusion_efficiency = radiation_coupling * secondary_burn * 0.5  # Hiệu suất tổng hợp tối đa 50%
            
            # Tổng hiệu suất là tổng có trọng số của hai giai đoạn
            efficiency = primary_yield_fraction * primary_efficiency + (1 - primary_yield_fraction) * fusion_efficiency
            
        else:
            # Loại vũ khí không xác định
            efficiency = 0.01  # Mặc định thấp
            
        # Đảm bảo hiệu suất nằm trong khoảng hợp lý
        return max(0.01, min(0.95, efficiency))
    
    def estimate_materials(self):
        """
        Ước tính vật liệu cần thiết dựa trên loại và năng lượng vũ khí
        
        Trả về:
            dict: Từ điển chứa ước tính các vật liệu cần thiết
        """
        materials = {}
        
        # Tính toán hiệu suất mặc định theo loại vũ khí
        default_params = {
            "fission": {
                "implosion_quality": 0.7,
                "neutron_initiator": 0.8,
                "tamper_effectiveness": 0.6
            },
            "boosted": {
                "fission_efficiency": 0.12,
                "tritium_amount": 0.5,
                "deuterium_amount": 0.5,
                "compression_quality": 0.8
            },
            "thermonuclear": {
                "primary_yield_fraction": 0.2,
                "coupling_efficiency": 0.7,
                "secondary_burn": 0.3,
                "radiation_case_quality": 0.8
            }
        }
        
        try:
            efficiency = self.calculate_efficiency(default_params.get(self.weapon_type, {}))
        except ValueError:
            efficiency = 0.15  # Giá trị mặc định nếu có lỗi
        
        if self.weapon_type == "fission":
            # Vũ khí phân hạch đơn giản
            # Năng lượng phóng ra = khối lượng vật liệu hạt nhân × hiệu suất × năng lượng phân hạch
            fission_energy = self.constants["fission_energy_u235"]  # J/kg cho U-235
            nuclear_material_mass = self.yield_kt * self.constants["kt_to_joules"] / (efficiency * fission_energy)
            
            # Tính tới khối lượng tới hạn tối thiểu
            min_critical_mass = self.constants["critical_mass_u235"] * (1 - self.enrichment_level * 0.5)
            nuclear_material_mass = max(nuclear_material_mass, min_critical_mass)
            
            materials = {
                'U-235 hoặc Pu-239 (kg)': nuclear_material_mass,
                'Vật liệu nổ thông thường (kg)': nuclear_material_mass * 4 + 10,
                'Vật liệu phản xạ/trì hoãn (kg)': nuclear_material_mass * 2.5,
                'Khối lượng tổng thể (kg)': nuclear_material_mass * 8 + 100,
                'Đường kính ước tính (cm)': 50 + 8 * np.power(nuclear_material_mass, 1/3)
            }
            
        elif self.weapon_type == "boosted":
            # Vũ khí phân hạch tăng cường
            # Cần ít vật liệu phân hạch hơn nhờ hiệu suất cao hơn
            fission_energy = self.constants["fission_energy_pu239"]  # J/kg cho Pu-239 (thường dùng)
            nuclear_material_mass = self.yield_kt * self.constants["kt_to_joules"] / (efficiency * fission_energy)
            
            # Tính tới khối lượng tới hạn tối thiểu cho plutonium
            min_critical_mass = self.constants["critical_mass_pu239"] * (1 - self.enrichment_level * 0.5)
            nuclear_material_mass = max(nuclear_material_mass, min_critical_mass)
            
            # Lượng tritium và deuterium theo năng lượng
            # Scaling phản ánh lượng DT cần cho năng lượng lớn hơn
            tritium_amount = 3 + np.power(self.yield_kt, 0.6) / 5  # gam
            deuterium_amount = 4 + np.power(self.yield_kt, 0.6) / 5  # gam
            
            materials = {
                'Pu-239 (kg)': nuclear_material_mass * 0.85,  # Cần ít vật liệu phân hạch hơn
                'Tritium (g)': tritium_amount,
                'Deuterium (g)': deuterium_amount, 
                'Vật liệu nổ thông thường (kg)': nuclear_material_mass * 3.5 + 15,
                'Khối lượng tổng thể (kg)': nuclear_material_mass * 7 + 80,
                'Đường kính ước tính (cm)': 45 + 6 * np.power(nuclear_material_mass, 1/3)
            }
            
        elif self.weapon_type == "thermonuclear":
            # Vũ khí nhiệt hạch hai giai đoạn (Teller-Ulam)
            # Giai đoạn 1 (phân hạch) - thường là 5-20% tổng năng lượng
            primary_fraction = 0.2  # 20% năng lượng từ giai đoạn đầu
            primary_yield = primary_fraction * self.yield_kt
            
            # Tính vật liệu cho giai đoạn đầu (phân hạch)
            primary_efficiency = 0.25  # Hiệu suất cao hơn cho thiết bị kích nổ
            fission_energy = self.constants["fission_energy_pu239"]  # J/kg
            primary_material = primary_yield * self.constants["kt_to_joules"] / (primary_efficiency * fission_energy)
            
            # Giai đoạn 2 (nhiệt hạch) - nguồn năng lượng chính
            secondary_yield = (1 - primary_fraction) * self.yield_kt
            
            # Vật liệu nhiệt hạch chính là lithium deuteride
            fusion_energy = self.constants["fusion_energy_li6dt"]  # J/kg
            fusion_efficiency = 0.35  # Hiệu suất điển hình cho các phản ứng nhiệt hạch giai đoạn 2
            
            lithium_deuteride = secondary_yield * self.constants["kt_to_joules"] / (fusion_efficiency * fusion_energy)
            
            # Tỷ lệ U-238 trong lớp vỏ phụ thuộc vào năng lượng
            u238_tamper_ratio = 2.5 + 0.5 * np.log10(max(1, self.yield_kt))
            
            materials = {
                'Pu-239 cho giai đoạn đầu (kg)': primary_material,
                'Tritium cho giai đoạn đầu (g)': 3 + primary_yield / 10,  # Nếu giai đoạn đầu được tăng cường
                'Lithium Deuteride cho giai đoạn 2 (kg)': lithium_deuteride,
                'U-238 vỏ bọc (kg)': lithium_deuteride * u238_tamper_ratio,
                'Vật liệu phản xạ bức xạ (kg)': 30 + self.yield_kt / 10,
                'Khối lượng tổng thể (kg)': 350 + self.yield_kt * 2.5,
                'Độ dài ước tính (cm)': 150 + 20 * np.power(self.yield_kt, 1/3)
            }
            
        return materials
    
    def get_design_characteristics(self):
        """
        Trả về các đặc tính chung của thiết kế vũ khí
        
        Trả về:
            dict: Từ điển chứa các đặc tính thiết kế
        """
        characteristics = {
            'Loại vũ khí': self.weapon_type,
            'Năng lượng (kt)': self.yield_kt,
            'Mức độ làm giàu vật liệu hạt nhân': f'{self.enrichment_level * 100:.1f}%',
            'Vật liệu': self.estimate_materials()
        }
        
        if self.weapon_type == "fission":
            characteristics.update({
                'Cơ chế': 'Nén cô đặc vật liệu phân hạch để đạt khối lượng trên tới hạn',
                'Hiệu suất điển hình': '10-20%',
                'Ứng dụng': 'Vũ khí chiến thuật, đầu đạn nhỏ gọn, thiết bị kích nổ cho nhiệt hạch',
                'Độ phức tạp': 'Thấp đến trung bình',
                'Hạn chế chính': 'Năng lượng giới hạn, hiệu suất thấp, yêu cầu vật liệu hạt nhân tinh khiết'
            })
        elif self.weapon_type == "boosted":
            characteristics.update({
                'Cơ chế': 'Phân hạch tăng cường bằng phản ứng nhiệt hạch D-T nhỏ',
                'Hiệu suất điển hình': '20-30%',
                'Ứng dụng': 'Đầu đạn nhỏ gọn năng lượng cao, vũ khí chiến thuật cải tiến',
                'Độ phức tạp': 'Trung bình',
                'Hạn chế chính': 'Yêu cầu tritium (bán rã ngắn), kỹ thuật nén phức tạp hơn'
            })
        elif self.weapon_type == "thermonuclear":
            characteristics.update({
                'Cơ chế': 'Thiết kế hai giai đoạn Teller-Ulam với bơm bức xạ X',
                'Hiệu suất điển hình': '30-40%',
                'Ứng dụng': 'Vũ khí chiến lược, đầu đạn năng lượng rất cao',
                'Độ phức tạp': 'Cao',
                'Hạn chế chính': 'Kích thước lớn, thiết kế phức tạp, chi phí cao'
            })
            
        return characteristics
    
    def optimize_design(self, target_yield, constraints=None, weapon_type=None):
        """
        Tối ưu hóa thiết kế để đạt được năng lượng mục tiêu với các ràng buộc
        
        Tham số:
            target_yield (float): Năng lượng mục tiêu (kt)
            constraints (dict): Các ràng buộc về khối lượng, kích thước, v.v.
            weapon_type (str): Loại vũ khí cần tối ưu hoá (nếu None thì dùng loại hiện tại)
            
        Trả về:
            dict: Bộ tham số tối ưu
            float: Hiệu suất ước tính
        """
        if weapon_type is not None:
            self.weapon_type = weapon_type
            
        self.yield_kt = target_yield
        if constraints is None:
            constraints = {}
            
        # Định nghĩa hàm mục tiêu: tối đa hóa hiệu suất
        def objective_function(params):
            if self.weapon_type == "fission":
                design_params = {
                    "implosion_quality": params[0],
                    "neutron_initiator": params[1],
                    "tamper_effectiveness": params[2],
                    "fissile_purity": params[3]
                }
            elif self.weapon_type == "boosted":
                design_params = {
                    "fission_efficiency": params[0],
                    "tritium_amount": params[1],
                    "deuterium_amount": params[2],
                    "compression_quality": params[3]
                }
            else:  # thermonuclear
                design_params = {
                    "primary_yield_fraction": params[0],
                    "coupling_efficiency": params[1],
                    "secondary_burn": params[2],
                    "radiation_case_quality": params[3]
                }
                
            # Đảo dấu vì minimize thực hiện cực tiểu hóa, chúng ta muốn cực đại hóa hiệu suất
            return -self.calculate_efficiency(design_params)
            
        # Giới hạn cho các tham số
        bounds = [(0.3, 0.95), (0.5, 0.95), (0.3, 0.95), (0.5, 0.99)]
        
        # Tối ưu hóa
        initial_guess = [0.7, 0.8, 0.6, 0.9]
        result = minimize(objective_function, initial_guess, bounds=bounds, method='L-BFGS-B')
        
        # Chuyển đổi kết quả về design_params
        optimized_params = {}
        if self.weapon_type == "fission":
            optimized_params = {
                "implosion_quality": result.x[0],
                "neutron_initiator": result.x[1],
                "tamper_effectiveness": result.x[2],
                "fissile_purity": result.x[3]
            }
        elif self.weapon_type == "boosted":
            optimized_params = {
                "fission_efficiency": result.x[0],
                "tritium_amount": result.x[1],
                "deuterium_amount": result.x[2],
                "compression_quality": result.x[3]
            }
        else:  # thermonuclear
            optimized_params = {
                "primary_yield_fraction": result.x[0],
                "coupling_efficiency": result.x[1],
                "secondary_burn": result.x[2],
                "radiation_case_quality": result.x[3]
            }
            
        efficiency = -result.fun  # Hiệu suất tối ưu
        
        return optimized_params, efficiency
        
    def plot_efficiency_vs_parameter(self, parameter_name, value_range, fixed_params=None):
        """
        Vẽ đồ thị hiệu suất theo một tham số thay đổi
        
        Tham số:
            parameter_name (str): Tên tham số cần khảo sát
            value_range (list): Danh sách các giá trị của tham số
            fixed_params (dict): Các tham số cố định khác
            
        Trả về:
            matplotlib.figure: Đồ thị hiệu suất
        """
        if fixed_params is None:
            if self.weapon_type == "fission":
                fixed_params = {
                    "implosion_quality": 0.7,
                    "neutron_initiator": 0.8,
                    "tamper_effectiveness": 0.6,
                    "fissile_purity": self.enrichment_level
                }
            elif self.weapon_type == "boosted":
                fixed_params = {
                    "fission_efficiency": 0.12,
                    "tritium_amount": 0.5,
                    "deuterium_amount": 0.5,
                    "compression_quality": 0.8
                }
            else:  # thermonuclear
                fixed_params = {
                    "primary_yield_fraction": 0.2,
                    "coupling_efficiency": 0.7,
                    "secondary_burn": 0.3,
                    "radiation_case_quality": 0.8
                }
                
        efficiencies = []
        for value in value_range:
            params = fixed_params.copy()
            params[parameter_name] = value
            efficiencies.append(self.calculate_efficiency(params))
            
        plt.figure(figsize=(10, 6))
        plt.plot(value_range, efficiencies, 'b-', marker='o')
        plt.title(f'Ảnh hưởng của {parameter_name} đến hiệu suất vũ khí {self.weapon_type}')
        plt.xlabel(parameter_name)
        plt.ylabel('Hiệu suất')
        plt.grid(True)
        
        return plt.gcf() 