import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import multiprocessing as mp
from functools import partial

class MonteCarloNeutronTransport:
    def __init__(self, radius=10.0, 
                 fission_xs=0.05, scattering_xs=0.2, absorption_xs=0.01,
                 fission_neutrons=2.43, energy_groups=1, max_generations=20,
                 initial_distribution='point'):
        """
        Mô phỏng vận chuyển neutron bằng phương pháp Monte Carlo.
        
        Tham số:
        -----------
        radius : float
            Bán kính hình cầu của lò phản ứng (cm)
        fission_xs : float hoặc array
            Tiết diện phân hạch (cm^-1), phụ thuộc năng lượng nếu là mảng
        scattering_xs : float hoặc array
            Tiết diện tán xạ (cm^-1)
        absorption_xs : float hoặc array
            Tiết diện hấp thụ (cm^-1)
        fission_neutrons : float
            Số neutron trung bình sinh ra từ mỗi phản ứng phân hạch
        energy_groups : int
            Số nhóm năng lượng cho tính toán đa nhóm
        max_generations : int
            Số thế hệ tối đa cho mô phỏng chuỗi phân hạch
        initial_distribution : str
            Phân bố ban đầu của neutron ('point', 'uniform', 'gaussian')
        """
        self.radius = radius
        self.energy_groups = energy_groups
        self.fission_neutrons = fission_neutrons
        self.max_generations = max_generations
        self.initial_distribution = initial_distribution
        
        # Xử lý tiết diện phụ thuộc năng lượng
        if energy_groups > 1:
            # Chuyển đổi thành mảng nếu chưa phải
            if not isinstance(fission_xs, (list, np.ndarray)) or len(np.atleast_1d(fission_xs)) != energy_groups:
                self.fission_xs = np.ones(energy_groups) * fission_xs
            else:
                self.fission_xs = np.array(fission_xs)
                
            if not isinstance(scattering_xs, (list, np.ndarray)) or len(np.atleast_1d(scattering_xs)) != energy_groups:
                self.scattering_xs = np.ones(energy_groups) * scattering_xs
            else:
                self.scattering_xs = np.array(scattering_xs)
                
            if not isinstance(absorption_xs, (list, np.ndarray)) or len(np.atleast_1d(absorption_xs)) != energy_groups:
                self.absorption_xs = np.ones(energy_groups) * absorption_xs
            else:
                self.absorption_xs = np.array(absorption_xs)
        else:
            self.fission_xs = fission_xs
            self.scattering_xs = scattering_xs
            self.absorption_xs = absorption_xs
            
        self.total_xs = self.fission_xs + self.scattering_xs + self.absorption_xs
        
        # Ma trận tán xạ cho tính toán đa nhóm (mặc định cho tán xạ đồng đều giữa các nhóm)
        if energy_groups > 1:
            self.scatter_matrix = np.ones((energy_groups, energy_groups)) / energy_groups
        
    def _get_cross_sections(self, energy_group=0):
        """Lấy tiết diện cho một nhóm năng lượng cụ thể"""
        if self.energy_groups > 1:
            fission = self.fission_xs[energy_group]
            scatter = self.scattering_xs[energy_group]
            absorb = self.absorption_xs[energy_group]
            total = self.total_xs[energy_group]
        else:
            fission = self.fission_xs
            scatter = self.scattering_xs
            absorb = self.absorption_xs
            total = self.total_xs
        
        return fission, scatter, absorb, total
    
    def _sample_direction(self, isotropic=True, previous_direction=None, scattering_angle=None):
        """
        Lấy mẫu hướng ngẫu nhiên trong không gian 3D
        
        Tham số:
        --------
        isotropic : bool
            Nếu True, lấy mẫu hướng đẳng hướng
        previous_direction : ndarray
            Hướng trước đó (sử dụng cho tán xạ bất đẳng hướng)
        scattering_angle : float
            Góc tán xạ trung bình (rad)
        """
        if isotropic:
            # Lấy mẫu đẳng hướng trong không gian 3D
            theta = np.arccos(2*np.random.random() - 1)
            phi = 2 * np.pi * np.random.random()
            direction = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])
        else:
            # Tán xạ bất đẳng hướng
            if previous_direction is not None and scattering_angle is not None:
                # Lấy mẫu góc tán xạ từ phân bố
                mu = np.random.normal(np.cos(scattering_angle), 0.1)
                mu = np.clip(mu, -1, 1)  # Giới hạn trong phạm vi hợp lệ
                
                # Tạo hệ tọa độ địa phương với trục z là hướng trước đó
                z_axis = previous_direction / np.linalg.norm(previous_direction)
                
                # Chọn trục x ngẫu nhiên vuông góc với z
                x_axis = np.array([1.0, 0.0, 0.0])
                if abs(np.dot(x_axis, z_axis)) > 0.9:
                    x_axis = np.array([0.0, 1.0, 0.0])
                
                x_axis = x_axis - np.dot(x_axis, z_axis) * z_axis
                x_axis = x_axis / np.linalg.norm(x_axis)
                
                # Trục y vuông góc với x và z
                y_axis = np.cross(z_axis, x_axis)
                
                # Tính hướng mới
                phi = 2 * np.pi * np.random.random()
                direction = (mu * z_axis + 
                            np.sqrt(1 - mu**2) * (np.cos(phi) * x_axis + np.sin(phi) * y_axis))
            else:
                # Mặc định quay lại đẳng hướng nếu thiếu tham số
                return self._sample_direction(isotropic=True)
        
        return direction
    
    def _initialize_neutrons(self, num_neutrons):
        """
        Khởi tạo neutron với phân bố không gian cụ thể
        
        Tham số:
        --------
        num_neutrons : int
            Số lượng neutron cần khởi tạo
        
        Trả về:
        -------
        list : Danh sách các neutron
        """
        neutrons = []
        
        for _ in range(num_neutrons):
            if self.initial_distribution == 'point':
                # Phân bố điểm (tại tâm)
                pos = np.array([0.0, 0.0, 0.0])
            elif self.initial_distribution == 'uniform':
                # Phân bố đều trong hình cầu
                r = self.radius * np.random.random()**(1/3)  # Phân bố đều theo thể tích
                theta = np.arccos(2*np.random.random() - 1)
                phi = 2 * np.pi * np.random.random()
                pos = np.array([
                    r * np.sin(theta) * np.cos(phi),
                    r * np.sin(theta) * np.sin(phi),
                    r * np.cos(theta)
                ])
            elif self.initial_distribution == 'gaussian':
                # Phân bố Gaussian xung quanh tâm
                sigma = self.radius / 3.0  # Độ lệch chuẩn
                pos = np.random.normal(0, sigma, 3)
            else:
                # Mặc định là tâm nếu không xác định
                pos = np.array([0.0, 0.0, 0.0])
            
            # Năng lượng ban đầu
            if self.energy_groups > 1:
                # Nếu là tính toán đa nhóm, mặc định là nhóm năng lượng cao nhất (0)
                energy_group = 0
            else:
                energy_group = 0
                
            neutrons.append({
                'pos': pos, 
                'energy_group': energy_group,
                'weight': 1.0  # Trọng số cho kỹ thuật giảm phương sai
            })
        
        return neutrons
        
    def _process_neutron_batch(self, neutrons, max_interactions, fission_chain=True):
        """
        Xử lý một lô neutron (hỗ trợ tính toán song song)
        
        Tham số:
        --------
        neutrons : list
            Danh sách các neutron cần xử lý
        max_interactions : int
            Số lượng tương tác tối đa cho mỗi neutron
        fission_chain : bool
            Liệu có mô phỏng chuỗi phân hạch hay không
            
        Trả về:
        -------
        tuple : (kết quả, neutron thế hệ tiếp theo)
        """
        n_fissions = 0
        n_absorptions = 0
        n_escapes = 0
        path_lengths = []
        final_positions = []
        next_gen_neutrons = []
        fission_sites = []
        
        for neutron in neutrons:
            pos = neutron['pos'].copy()
            energy_group = neutron['energy_group']
            weight = neutron['weight']
            alive = True
            interactions = 0
            
            while alive and interactions < max_interactions:
                # Lấy tiết diện cho nhóm năng lượng hiện tại
                fission_xs, scatter_xs, absorb_xs, total_xs = self._get_cross_sections(energy_group)
                
                # Lấy mẫu đường tự do trung bình
                mfp = -np.log(np.random.random()) / total_xs
                path_lengths.append(mfp)
                
                # Hướng di chuyển ngẫu nhiên
                direction = self._sample_direction()
                
                # Di chuyển neutron
                pos = pos + mfp * direction
                
                # Kiểm tra xem neutron đã thoát ra khỏi hệ thống chưa
                if np.linalg.norm(pos) > self.radius:
                    n_escapes += 1
                    alive = False
                    continue
                
                # Xác định loại tương tác
                interaction_type = np.random.random() * total_xs
                
                if interaction_type < fission_xs:
                    n_fissions += 1
                    alive = False
                    
                    # Ghi lại vị trí phân hạch cho tính toán độ tới hạn
                    if fission_chain:
                        fission_sites.append(pos.copy())
                        
                        # Tạo neutron mới cho thế hệ tiếp theo
                        n_new = np.random.poisson(self.fission_neutrons)
                        for _ in range(n_new):
                            # Đối với tính toán đa nhóm, chọn nhóm năng lượng theo phổ phân hạch
                            if self.energy_groups > 1:
                                # Giả sử phổ phân hạch ưu tiên năng lượng cao (nhóm 0)
                                probs = np.exp(-np.arange(self.energy_groups))
                                probs = probs / np.sum(probs)
                                new_energy_group = np.random.choice(np.arange(self.energy_groups), p=probs)
                            else:
                                new_energy_group = 0
                                
                            next_gen_neutrons.append({
                                'pos': pos.copy(),
                                'energy_group': new_energy_group,
                                'weight': weight
                            })
                            
                elif interaction_type < fission_xs + absorb_xs:
                    n_absorptions += 1
                    alive = False
                else:
                    # Tán xạ - tiếp tục với hướng mới và có thể là năng lượng mới
                    if self.energy_groups > 1:
                        # Chuyển tiếp nhóm năng lượng sau tán xạ
                        scatter_probs = self.scatter_matrix[energy_group]
                        energy_group = np.random.choice(np.arange(self.energy_groups), p=scatter_probs)
                
                interactions += 1
                
            final_positions.append(np.linalg.norm(pos))
            
        return {
            'fissions': n_fissions,
            'absorptions': n_absorptions,
            'escapes': n_escapes,
            'path_lengths': path_lengths,
            'final_positions': final_positions,
            'fission_sites': fission_sites
        }, next_gen_neutrons
        
    def simulate_neutrons(self, num_neutrons=1000, max_interactions=100, 
                          show_progress=True, fission_chain=True, 
                          use_parallel=False, n_cores=None):
        """
        Mô phỏng Monte Carlo cho quá trình vận chuyển neutron
        
        Tham số:
        -----------
        num_neutrons : int
            Số lượng neutron ban đầu để mô phỏng
        max_interactions : int
            Số lượng tương tác tối đa cho mỗi lịch sử neutron
        show_progress : bool
            Hiển thị thanh tiến trình hay không
        fission_chain : bool
            Mô phỏng chuỗi phân hạch (tính toán k-hiệu quả)
        use_parallel : bool
            Sử dụng tính toán song song để tăng tốc
        n_cores : int
            Số lõi CPU sử dụng cho tính toán song song
        
        Trả về:
        --------
        dict : Kết quả của mô phỏng
        """
        # Mảng để theo dõi kết quả
        n_fissions = 0
        n_absorptions = 0
        n_escapes = 0
        path_lengths = []
        final_positions = []
        
        # Cho tính toán độ tới hạn
        generation_sizes = [num_neutrons]
        fission_sites = []
        
        # Khởi tạo neutron (có thể tăng lên với phân hạch)
        neutrons = self._initialize_neutrons(num_neutrons)
        
        generation = 0
        start_time = time.time()
        
        # Thiết lập đa luồng nếu được yêu cầu
        if use_parallel and n_cores is None:
            n_cores = max(1, mp.cpu_count() - 1)  # Để lại một lõi cho hệ thống
        
        while neutrons and generation < self.max_generations:  # Giới hạn số thế hệ
            generation += 1
            next_gen_neutrons = []
            
            # Hiển thị thông tin thế hệ
            if show_progress:
                desc = f"Thế hệ {generation}, số neutron: {len(neutrons)}"
                if use_parallel:
                    print(desc)
                    iterator = neutrons
                else:
                    iterator = tqdm(neutrons, desc=desc)
            else:
                iterator = neutrons
            
            # Xử lý neutron song song nếu được yêu cầu
            if use_parallel and len(neutrons) > 100:  # Chỉ song song hóa nếu đủ nhiều neutron
                # Chia neutron thành các lô cho các lõi
                batch_size = max(1, len(neutrons) // n_cores)
                batches = [neutrons[i:i+batch_size] for i in range(0, len(neutrons), batch_size)]
                
                # Xử lý song song
                with mp.Pool(n_cores) as pool:
                    process_func = partial(self._process_neutron_batch, 
                                           max_interactions=max_interactions, 
                                           fission_chain=fission_chain)
                    results = pool.map(process_func, batches)
                
                # Tổng hợp kết quả
                for res, new_neutrons in results:
                    n_fissions += res['fissions']
                    n_absorptions += res['absorptions']
                    n_escapes += res['escapes']
                    path_lengths.extend(res['path_lengths'])
                    final_positions.extend(res['final_positions'])
                    fission_sites.extend(res['fission_sites'])
                    next_gen_neutrons.extend(new_neutrons)
            else:
                # Xử lý tuần tự
                for neutron in iterator:
                    pos = neutron['pos']
                    energy_group = neutron['energy_group']
                    weight = neutron['weight']
                    alive = True
                    interactions = 0
                    
                    while alive and interactions < max_interactions:
                        # Lấy tiết diện cho nhóm năng lượng hiện tại
                        fission_xs, scatter_xs, absorb_xs, total_xs = self._get_cross_sections(energy_group)
                        
                        # Lấy mẫu đường tự do trung bình
                        mfp = -np.log(np.random.random()) / total_xs
                        path_lengths.append(mfp)
                        
                        # Hướng di chuyển ngẫu nhiên (sử dụng tán xạ đẳng hướng)
                        direction = self._sample_direction()
                        
                        # Di chuyển neutron
                        pos = pos + mfp * direction
                        
                        # Kiểm tra xem neutron đã thoát ra khỏi hệ thống chưa
                        if np.linalg.norm(pos) > self.radius:
                            n_escapes += 1
                            alive = False
                            continue
                        
                        # Xác định loại tương tác
                        interaction_type = np.random.random() * total_xs
                        
                        if interaction_type < fission_xs:
                            n_fissions += 1
                            alive = False
                            
                            # Ghi lại vị trí phân hạch cho tính toán độ tới hạn
                            if fission_chain:
                                fission_sites.append(pos.copy())
                                
                                # Tạo neutron mới cho thế hệ tiếp theo
                                n_new = np.random.poisson(self.fission_neutrons)
                                for _ in range(n_new):
                                    if self.energy_groups > 1:
                                        # Phổ phân hạch ưu tiên năng lượng cao
                                        probs = np.exp(-np.arange(self.energy_groups))
                                        probs = probs / np.sum(probs)
                                        new_energy_group = np.random.choice(np.arange(self.energy_groups), p=probs)
                                    else:
                                        new_energy_group = 0
                                        
                                    next_gen_neutrons.append({
                                        'pos': pos.copy(),
                                        'energy_group': new_energy_group,
                                        'weight': weight
                                    })
                                    
                        elif interaction_type < fission_xs + absorb_xs:
                            n_absorptions += 1
                            alive = False
                        else:
                            # Tán xạ - tiếp tục với hướng mới và có thể là năng lượng mới
                            if self.energy_groups > 1:
                                # Chuyển tiếp nhóm năng lượng
                                scatter_probs = self.scatter_matrix[energy_group]
                                energy_group = np.random.choice(np.arange(self.energy_groups), p=scatter_probs)
                        
                        interactions += 1
                        
                    final_positions.append(np.linalg.norm(pos))
                    
            # Cập nhật neutron cho thế hệ tiếp theo
            neutrons = next_gen_neutrons if fission_chain else []
            generation_sizes.append(len(next_gen_neutrons))
            
            # Kiểm tra sự hội tụ của k-hiệu quả
            if fission_chain and len(generation_sizes) > 3 and generation_sizes[-1] > 0:
                k_previous = generation_sizes[-1] / generation_sizes[-2] if generation_sizes[-2] > 0 else 0
                k_current = generation_sizes[-2] / generation_sizes[-3] if generation_sizes[-3] > 0 else 0
                
                # Thoát vòng lặp nếu k-hiệu quả hội tụ (sai số < 1%)
                if abs(k_current - k_previous) / k_current < 0.01 and generation >= 5:
                    if show_progress:
                        print(f"Đã hội tụ sau {generation} thế hệ.")
                    break
        
        # Tính k-hiệu quả nếu chúng ta đã mô phỏng chuỗi phân hạch
        k_effective = None
        k_error = None
        if fission_chain and len(generation_sizes) > 2:
            # Tính k-hiệu quả là tỷ lệ của các thế hệ liên tiếp
            # Bỏ qua thế hệ đầu tiên để tránh hiệu ứng nguồn
            k_values = [generation_sizes[i+1]/generation_sizes[i] 
                      for i in range(1, len(generation_sizes)-1) if generation_sizes[i] > 0]
            
            if k_values:
                k_effective = np.mean(k_values)
                k_error = np.std(k_values) / np.sqrt(len(k_values)) if len(k_values) > 1 else 0
        
        elapsed_time = time.time() - start_time
            
        return {
            'fissions': n_fissions,
            'absorptions': n_absorptions,
            'escapes': n_escapes,
            'path_lengths': path_lengths,
            'final_positions': final_positions,
            'k_effective': k_effective,
            'k_error': k_error,
            'generation_sizes': generation_sizes,
            'elapsed_time': elapsed_time,
            'max_generation': generation
        }
    
    def visualize_results(self, results):
        """
        Trực quan hóa kết quả mô phỏng với các đồ thị
        
        Tham số:
        -----------
        results : dict
            Kết quả từ phương thức simulate_neutrons
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Đồ thị 1: Phân bố tương tác
        interaction_counts = [results['fissions'], results['absorptions'], results['escapes']]
        interaction_labels = ['Phân hạch', 'Hấp thụ', 'Thoát']
        axes[0, 0].bar(interaction_labels, interaction_counts, color=['red', 'blue', 'green'])
        axes[0, 0].set_title('Phân bố tương tác neutron')
        axes[0, 0].set_ylabel('Số lượng')
        
        # Đồ thị 2: Phân bố độ dài đường đi
        axes[0, 1].hist(results['path_lengths'], bins=50, alpha=0.7, color='purple')
        axes[0, 1].set_title('Phân bố độ dài đường đi của neutron')
        axes[0, 1].set_xlabel('Độ dài đường đi (cm)')
        axes[0, 1].set_ylabel('Tần suất')
        
        # Đồ thị 3: Phân bố vị trí cuối cùng
        axes[1, 0].hist(results['final_positions'], bins=50, alpha=0.7, color='orange')
        axes[1, 0].set_title('Phân bố vị trí bán kính cuối cùng')
        axes[1, 0].set_xlabel('Vị trí bán kính (cm)')
        axes[1, 0].set_ylabel('Tần suất')
        axes[1, 0].axvline(x=self.radius, color='r', linestyle='--', 
                          label=f'Ranh giới hệ thống (r={self.radius}cm)')
        axes[1, 0].legend()
        
        # Đồ thị 4: Kích thước thế hệ cho tính toán độ tới hạn (nếu có)
        if 'k_effective' in results and results['k_effective'] is not None:
            generations = range(len(results['generation_sizes']))
            axes[1, 1].plot(generations, results['generation_sizes'], 'o-', color='teal')
            axes[1, 1].set_title(f'Quần thể neutron theo thế hệ\nk-eff = {results["k_effective"]:.4f} ± {results["k_error"]:.4f}')
            axes[1, 1].set_xlabel('Thế hệ')
            axes[1, 1].set_ylabel('Số lượng neutron')
            axes[1, 1].grid(True)
            
            # Hiển thị trạng thái hệ thống
            if results['k_effective'] < 0.95:
                status = "Dưới tới hạn"
            elif results['k_effective'] > 1.05:
                status = "Trên tới hạn"
            else:
                status = "Gần tới hạn"
                
            axes[1, 1].text(0.5, 0.9, f"Trạng thái: {status}", 
                           transform=axes[1, 1].transAxes, ha='center',
                           bbox=dict(facecolor='white', alpha=0.8))
        else:
            axes[1, 1].text(0.5, 0.5, 'Không có dữ liệu về độ tới hạn', 
                           horizontalalignment='center', verticalalignment='center')
        
        fig.tight_layout()
        return fig
    
    def analyze_energy_spectrum(self, results):
        """
        Phân tích phổ năng lượng từ kết quả mô phỏng đa nhóm
        
        Tham số:
        --------
        results : dict
            Kết quả từ phương thức simulate_neutrons
        
        Trả về:
        -------
        fig : matplotlib Figure
            Hình ảnh phân tích
        """
        if self.energy_groups <= 1:
            return None
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Giả định các nhóm năng lượng theo thứ tự giảm dần
        energy_boundaries = np.logspace(1, -5, self.energy_groups + 1)  # Từ 10 MeV đến 0.00001 MeV
        group_names = [f"Nhóm {i+1}\n({energy_boundaries[i]:.2e}-{energy_boundaries[i+1]:.2e} MeV)" 
                      for i in range(self.energy_groups)]
        
        # Tính toán phổ từ tiết diện và kết quả
        xs_values = np.column_stack([self.fission_xs, self.scattering_xs, self.absorption_xs])
        
        # Vẽ tiết diện theo nhóm năng lượng
        x = np.arange(self.energy_groups)
        width = 0.25
        
        ax.bar(x - width, self.fission_xs, width, label='Tiết diện phân hạch')
        ax.bar(x, self.scattering_xs, width, label='Tiết diện tán xạ')
        ax.bar(x + width, self.absorption_xs, width, label='Tiết diện hấp thụ')
        
        ax.set_xlabel('Nhóm năng lượng')
        ax.set_ylabel('Tiết diện (cm⁻¹)')
        ax.set_title('Phân tích phổ năng lượng và tiết diện')
        ax.set_xticks(x)
        ax.set_xticklabels(group_names, rotation=45, ha='right')
        ax.legend()
        
        fig.tight_layout()
        return fig