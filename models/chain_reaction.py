import numpy as np
from scipy.integrate import solve_ivp

class ChainReactionModel:
    def __init__(self, fission_cross_section=1.0, neutron_speed=2200, 
                 uranium_density=19.1, enrichment=0.85, 
                 neutrons_per_fission=2.5, neutron_lifetime=10e-8):
        # Thông số cơ bản của mô hình phản ứng hạt nhân
        self.fission_cross_section = fission_cross_section  # barns - tiết diện phân hạch
        self.neutron_speed = neutron_speed  # m/s - vận tốc của neutron
        self.uranium_density = uranium_density  # g/cm³ - mật độ uranium
        self.enrichment = enrichment  # fraction of U-235 - tỷ lệ làm giàu U-235
        self.neutrons_per_fission = neutrons_per_fission  # số lượng neutron sinh ra mỗi phân hạch
        self.neutron_lifetime = neutron_lifetime  # s - thời gian sống trung bình của neutron
        
        # Hằng số vật lý và nguyên tử
        self.avogadro = 6.022e23  # Số Avogadro
        self.u235_mass = 235.04  # g/mol - khối lượng U-235
        self.u238_mass = 238.05  # g/mol - khối lượng U-238
        
    def calculate_macroscopic_cross_section(self):
        """Tính toán tiết diện phân hạch vĩ mô"""
        # Tính số mật độ nguyên tử U-235
        avg_molar_mass = self.enrichment * self.u235_mass + (1 - self.enrichment) * self.u238_mass
        atom_density = self.uranium_density * self.avogadro / avg_molar_mass  # atoms/cm³
        u235_density = atom_density * self.enrichment  # atoms/cm³
        
        # Chuyển đổi từ barn sang cm²
        micro_xs_cm2 = self.fission_cross_section * 1e-24  # 1 barn = 10^-24 cm²
        
        # Tiết diện vĩ mô (cm^-1)
        return u235_density * micro_xs_cm2
        
    def calculate_critical_mass(self, geometry="sphere"):
        """Tính toán khối lượng tới hạn dựa trên hình dạng"""
        # Tiết diện vĩ mô
        sigma_f = self.calculate_macroscopic_cross_section()
        
        # Tính toán khối lượng tới hạn chính xác hơn dựa trên hình dạng
        if geometry == "sphere":
            # Gần đúng cho hình cầu - Buckling hình học = (π/R)²
            buckling = (np.pi / (self.neutrons_per_fission * sigma_f))**2
            radius = np.pi / np.sqrt(buckling)  # cm
            volume = (4/3) * np.pi * radius**3  # cm³
        elif geometry == "cylinder":
            # Giả sử chiều cao bằng đường kính - buckling phức tạp hơn
            buckling = (2.405 / (self.neutrons_per_fission * sigma_f))**2
            radius = 2.405 / np.sqrt(buckling)  # cm
            height = 2 * radius
            volume = np.pi * radius**2 * height  # cm³
        else:  # cube hoặc hình dạng khác
            buckling = (np.pi / (self.neutrons_per_fission * sigma_f))**2
            length = np.pi / np.sqrt(buckling / 3)  # cm
            volume = length**3  # cm³
            
        # Chuyển đổi thể tích thành khối lượng
        critical_mass = volume * self.uranium_density  # g
        return critical_mass / 1000  # kg
    
    def simulate_chain_reaction(self, initial_neutrons=1, 
                               mass_ratio=1.5, time_span=(0, 0.001), 
                               time_steps=1000, include_delayed=False):
        """Mô phỏng số lượng neutron trong phản ứng dây chuyền
        
        Parameters:
        ----------
        initial_neutrons: số lượng neutron ban đầu
        mass_ratio: tỷ lệ so với khối lượng tới hạn
        time_span: khoảng thời gian mô phỏng (giây)
        time_steps: số bước thời gian
        include_delayed: có tính đến neutron trễ hay không
        """
        # Tính toán hệ số nhân hiệu dụng
        # k_eff tỷ lệ thuận với khối lượng/khối lượng tới hạn
        k_eff = mass_ratio * self.neutrons_per_fission
        
        # Tính toán độ phản ứng
        reactivity = (k_eff - 1.0) / k_eff
        
        if include_delayed:
            # Mô hình với neutron trễ (chính xác hơn)
            # Thông số cho neutron trễ
            beta = 0.0065  # tỷ lệ neutron trễ
            lambda_d = 0.1  # hằng số phân rã (1/s)
            
            def neutron_kinetics(t, y):
                n, c = y  # n: số lượng neutron, c: tiền neutron trễ
                
                # Phương trình động học
                dn_dt = (reactivity - beta) * n / self.neutron_lifetime + lambda_d * c
                dc_dt = beta * n / self.neutron_lifetime - lambda_d * c
                
                return [dn_dt, dc_dt]
            
            # Điều kiện ban đầu [neutron, precursors]
            y0 = [initial_neutrons, 0]
            
            t_eval = np.linspace(time_span[0], time_span[1], time_steps)
            solution = solve_ivp(neutron_kinetics, time_span, y0, 
                                 method='BDF', t_eval=t_eval)
            
            return solution.t, solution.y[0]  # Chỉ trả về số lượng neutron
        else:
            # Mô hình đơn giản chỉ với neutron tức thời
            def neutron_growth(t, n):
                # Tốc độ tăng trưởng phụ thuộc vào mức độ vượt quá khối lượng tới hạn
                return (k_eff - 1) * n / self.neutron_lifetime
            
            t_eval = np.linspace(time_span[0], time_span[1], time_steps)
            solution = solve_ivp(neutron_growth, time_span, [initial_neutrons], 
                                 method='RK45', t_eval=t_eval)
            
            return solution.t, solution.y[0]
            
    def calculate_energy_release(self, neutron_count, fission_energy=200):
        """Tính toán năng lượng giải phóng từ số lượng neutron đã tạo ra phản ứng phân hạch
        
        Parameters:
        ----------
        neutron_count: mảng số lượng neutron theo thời gian
        fission_energy: năng lượng giải phóng mỗi phân hạch (MeV)
        
        Returns:
        --------
        energy: năng lượng giải phóng (J)
        """
        # Chuyển đổi MeV thành J (1 MeV = 1.602e-13 J)
        energy_per_fission_J = fission_energy * 1.602e-13
        
        # Ước tính số lượng phân hạch dựa trên số lượng neutron
        # Giả sử mỗi neutron cuối cùng sẽ gây ra một phân hạch
        total_fissions = np.trapz(neutron_count, dx=1)
        
        # Năng lượng tổng
        return total_fissions * energy_per_fission_J