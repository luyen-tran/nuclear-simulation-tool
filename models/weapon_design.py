import numpy as np
import matplotlib.pyplot as plt

class NuclearWeaponDesignModel:
    def __init__(self, weapon_type="fission", yield_kt=20):
        self.weapon_type = weapon_type  # "fission", "boosted", "thermonuclear"
        self.yield_kt = yield_kt
        
    def calculate_efficiency(self, design_params):
        """Tính toán hiệu suất dựa trên các tham số thiết kế"""
        if self.weapon_type == "fission":
            # Thiết kế phân hạch đơn giản
            implosion_quality = design_params.get("implosion_quality", 0.7)
            neutron_initiator = design_params.get("neutron_initiator", 0.8)
            tamper_effectiveness = design_params.get("tamper_effectiveness", 0.6)
            
            # Hiệu suất phân hạch khoảng 1-20%
            efficiency = 0.01 + 0.19 * implosion_quality * neutron_initiator * tamper_effectiveness
            
        elif self.weapon_type == "boosted":
            # Thiết kế phân hạch được tăng cường
            fission_efficiency = design_params.get("fission_efficiency", 0.1)
            tritium_amount = design_params.get("tritium_amount", 0.5)
            
            # Tăng cường có thể tăng hiệu suất lên 2-3 lần
            efficiency = fission_efficiency * (1 + 2 * tritium_amount)
            
        elif self.weapon_type == "thermonuclear":
            # Thiết kế nhiệt hạch hai giai đoạn
            primary_yield = design_params.get("primary_yield", 0.2)  # % của tổng năng lượng
            coupling_efficiency = design_params.get("coupling_efficiency", 0.7)
            secondary_burn = design_params.get("secondary_burn", 0.3)
            
            # Hiệu suất tổng hợp lên đến 40%
            primary_efficiency = 0.15  # Hiệu suất giai đoạn đầu
            fusion_efficiency = coupling_efficiency * secondary_burn * 0.4
            efficiency = primary_yield * primary_efficiency + (1 - primary_yield) * fusion_efficiency
            
        else:
            efficiency = 0.01  # Mặc định
            
        return efficiency
    
    def estimate_materials(self):
        """Ước tính vật liệu cần thiết dựa trên loại và năng lượng"""
        materials = {}
        
        if self.weapon_type == "fission":
            # Vũ khí phân hạch đơn giản
            # Khối lượng vật liệu hạt nhân = f(năng lượng, hiệu suất)
            efficiency = 0.15  # Giả định hiệu suất trung bình
            fission_energy = 8.2e13  # J/kg
            nuclear_material_mass = self.yield_kt * 4.184e12 / (efficiency * fission_energy)
            
            materials = {
                'U-235 hoặc Pu-239 (kg)': nuclear_material_mass,
                'Vật liệu nổ thông thường (kg)': nuclear_material_mass * 5,
                'Khối lượng tổng thể (kg)': nuclear_material_mass * 10
            }
            
        elif self.weapon_type == "boosted":
            # Vũ khí phân hạch tăng cường
            efficiency = 0.25  # Giả định hiệu suất cao hơn
            fission_energy = 8.2e13  # J/kg
            nuclear_material_mass = self.yield_kt * 4.184e12 / (efficiency * fission_energy)
            
            materials = {
                'U-235 hoặc Pu-239 (kg)': nuclear_material_mass * 0.8,  # Cần ít vật liệu hơn
                'Tritium (g)': 2 + self.yield_kt / 5,
                'Deuterium (g)': 3 + self.yield_kt / 5,
                'Khối lượng tổng thể (kg)': nuclear_material_mass * 8
            }
            
        elif self.weapon_type == "thermonuclear":
            # Vũ khí nhiệt hạch hai giai đoạn
            # Primary stage (phân hạch kích hoạt)
            primary_yield = 0.2 * self.yield_kt  # 20% năng lượng từ giai đoạn đầu
            primary_efficiency = 0.2
            fission_energy = 8.2e13  # J/kg
            primary_material = primary_yield * 4.184e12 / (primary_efficiency * fission_energy)
            
            # Secondary stage (nhiệt hạch chính)
            lithium_deuteride = (self.yield_kt - primary_yield) * 0.15  # Ước tính
            
            materials = {
                'U-235 hoặc Pu-239 cho giai đoạn đầu (kg)': primary_material,
                'Lithium Deuteride cho giai đoạn 2 (kg)': lithium_deuteride,
                'U-238 vỏ bọc (kg)': lithium_deuteride * 3,
                'Khối lượng tổng thể (kg)': 400 + self.yield_kt * 3
            }
            
        return materials
    
    def get_design_characteristics(self):
        """Trả về các đặc tính chung của thiết kế vũ khí"""
        characteristics = {
            'Loại vũ khí': self.weapon_type,
            'Năng lượng (kt)': self.yield_kt,
            'Vật liệu': self.estimate_materials()
        }
        
        if self.weapon_type == "fission":
            characteristics.update({
                'Cơ chế': 'Nén cô đặc vật liệu phân hạch để đạt khối lượng trên tới hạn',
                'Hiệu suất điển hình': '10-20%',
                'Đường kính ước tính': f'{60 + 10 * np.sqrt(self.yield_kt)} cm'
            })
        elif self.weapon_type == "boosted":
            characteristics.update({
                'Cơ chế': 'Phân hạch tăng cường bằng phản ứng nhiệt hạch D-T nhỏ',
                'Hiệu suất điển hình': '20-30%',
                'Đường kính ước tính': f'{50 + 5 * np.sqrt(self.yield_kt)} cm'
            })
        elif self.weapon_type == "thermonuclear":
            characteristics.update({
                'Cơ chế': 'Thiết kế hai giai đoạn Teller-Ulam',
                'Hiệu suất điển hình': '30-40%',
                'Độ dài ước tính': f'{1 + 0.25 * np.power(self.yield_kt, 1/3)} m'
            })
            
        return characteristics 