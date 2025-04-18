translations = {
    "en": {
        "app.title": "Nuclear Physics Simulation Dashboard",
        "app.description": "This dashboard provides interactive simulations of various physical processes related to nuclear reactions and nuclear explosions.",
        "app.page_title": "Nuclear Physics Simulation",
        "app.icon": "☢️",
        "app.menu.get_help": "https://github.com/luyen-tran/nuclear-simulation-tool/issues",
        "app.menu.report_bug": "https://github.com/luyen-tran/nuclear-simulation-tool/issues",
        "app.menu.about": "# Nuclear Physics Simulation\nThis is a software for nuclear physics simulations.",
        "nav.chain_reaction": "Critical Mass & Chain Reaction",
        "nav.neutron_transport": "Neutron Transport Equation",
        "nav.monte_carlo": "Monte Carlo Modeling",
        "nav.blast_wave": "Blast Wave Simulation",
        "nav.thermal_radiation": "Thermal Radiation Effects",
        "footer.text": "Nuclear Physics Simulation Dashboard",
        "footer.links": "Links",
        "footer.documentation": "Documentation",
        "footer.info": "Info",
        "footer.version": "Version: {version}",
        "footer.last_updated": "Last updated: {date}",
        "select.simulation": "Select Simulation",
        "language.selector": "Language / Ngôn ngữ",
        
        # Simulation categories
        "select.category": "Simulation Category",
        "category.theoretical": "Theoretical Models",
        "category.practical": "Practical Effects",
        
        # Theme settings
        "theme.light": "Light",
        "theme.dark": "Dark",
        "theme.system": "Use system theme",
        "theme.settings": "Theme Settings",
        "theme.selector": "Select Theme",
        "theme.apply_changes": "Click 'Apply New Theme' button above to apply the changes.",
        "theme.use_system": "The application will use your system theme.",
        
        # Chain reaction page
        "chain.header": "Critical Mass & Chain Reaction",
        "chain.enrichment": "U-235 Enrichment",
        "chain.geometry": "Geometry",
        "chain.geometry.sphere": "Sphere",
        "chain.geometry.cylinder": "Cylinder",
        "chain.geometry.slab": "Slab",
        "chain.neutrons": "Initial Neutrons",
        "chain.mass_ratio": "Mass Ratio (to Critical)",
        "chain.critical_mass": "Calculated critical mass: {mass:.2f} kg",
        "chain.button": "Run Chain Reaction Simulation",
        
        # Neutron transport page
        "transport.header": "Neutron Transport Equation Analysis",
        "transport.size": "System Size (cm)",
        "transport.resolution": "Spatial Resolution",
        "transport.scattering": "Scattering Cross-section (cm⁻¹)",
        "transport.absorption": "Absorption Cross-section (cm⁻¹)",
        "transport.fission": "Fission Cross-section (cm⁻¹)",
        "transport.button": "Solve Neutron Transport",
        "transport.button_label": "Neutron Transport Solution",
        
        # Monte Carlo page
        "monte.header": "Monte Carlo Modeling for Nuclear Reactions",
        "monte.radius": "System Radius (cm)",
        "monte.num_neutrons": "Number of Neutrons",
        "monte.fission": "MC: Fission Cross-section (cm⁻¹)",
        "monte.scattering": "MC: Scattering Cross-section (cm⁻¹)",
        "monte.absorption": "MC: Absorption Cross-section (cm⁻¹)",
        "monte.button": "Run Monte Carlo Simulation",
        "monte.fissions": "Fissions",
        "monte.absorptions": "Absorptions",
        "monte.escapes": "Escapes",
        "monte.advanced_options": "Advanced Options",
        "monte.average_fission_neutrons": "Average Neutrons per Fission",
        "monte.show_progress": "Show Progress Bar",
        "monte.simulate_fission_chain": "Simulate Fission Chain",
        "monte.execution_time": "Execution Time: {time:.2f} seconds",
        "monte.k_effective": "Effective Multiplication Factor (k-eff): {value:.4f} ± {error:.4f}",
        
        # Blast wave page
        "blast.header": "Sedov-Taylor Blast Wave Solution",
        "blast.yield": "Yield (kilotons)",
        "blast.distance": "Max Distance (m)",
        "blast.density": "Ambient Density (kg/m³)",
        "blast.time": "Time After Detonation (s)",
        "blast.radius": "Blast wave radius at {time} seconds: {radius:.2f} meters",
        "blast.button": "Simulate Blast Wave Propagation",
        "blast.chart_title": "Blast Wave Overpressure at t = {time} seconds",
        "blast.chart_title_animation": "Blast Wave Propagation Over Time",
        "blast.x_axis": "Distance from Ground Zero (m)",
        "blast.y_axis": "Overpressure (kPa)",
        "blast.play_button": "Play",
        "blast.shock_front": "Shock Front",
        "blast.damage_level_1": "Minor damage (window breakage)",
        "blast.damage_level_2": "Light structural damage (complete window breakage)",
        "blast.damage_level_3": "Moderate damage to reinforced structures",
        "blast.damage_level_4": "Most residential buildings collapse",
        "blast.damage_level_5": "Severe damage to reinforced concrete structures",
        "blast.damage_level_6": "Complete destruction of most structures",
        "blast.report_title": "Nuclear Blast Analysis Report",
        "blast.report_subtitle": "Sedov-Taylor Blast Wave Model Results",
        "blast.report_intro": "This report presents results from a Sedov-Taylor blast wave simulation used for educational purposes.",
        "blast.report_distance": "Effects at {distance} meters from ground zero:",
        "blast.report_pressure": "Peak overpressure: {pressure:.2f} kPa",
        "blast.report_wind": "Peak wind speed: {speed:.2f} m/s",
        "blast.report_arrival": "Arrival time of shock wave: {time:.2f} seconds",
        "blast.report_thermal": "Thermal radiation: {thermal:.2e} J/m²",
        "blast.report_radiation_initial": "Initial radiation: {radiation:.2e} Gy",
        "blast.report_radiation_fallout": "Fallout radiation (1 hour): {fallout:.2e} Gy",
        
        # Thermal radiation page
        "thermal.header": "Thermal and Radiative Impact Simulation",
        "thermal.yield": "Thermal: Yield (kilotons)",
        "thermal.distance": "Thermal: Max Distance (km)",
        "thermal.height": "Burst Height (m)",
        "thermal.energy_title": "Thermal Energy Density vs Distance",
        "thermal.energy_x_axis": "Distance from Ground Zero (km)",
        "thermal.energy_y_axis": "Thermal Energy Density (J/m²)",
        "thermal.burn_title": "Burn Probability vs Distance",
        "thermal.burn_x_axis": "Distance from Ground Zero (km)",
        "thermal.burn_y_axis": "Probability",
        "thermal.first_degree": "1st Degree Burns",
        "thermal.second_degree": "2nd Degree Burns",
        "thermal.third_degree": "3rd Degree Burns",
        "thermal.button": "Simulate Thermal Radiation Effects",
        
        # EMP effects page
        "nav.emp_effects": "EMP Effects",
        "emp.header": "Electromagnetic Pulse (EMP) Effects",
        "emp.yield": "EMP: Yield (kilotons)",
        "emp.distance": "EMP: Max Distance (km)",
        "emp.height": "Burst Height (km)",
        "emp.conductivity": "Ground Conductivity (S/m)",
        "emp.field_strength": "Field Strength",
        "emp.field_strength_title": "EMP Field Strength vs Distance",
        "emp.x_axis": "Distance from Ground Zero (km)",
        "emp.y_axis": "Electric Field Strength (V/m)",
        "emp.damage_title": "EMP Damage Probability vs Distance",
        "emp.probability": "Probability",
        "emp.electronic_damage": "Electronic Equipment Damage",
        "emp.power_grid_damage": "Power Grid Damage",
        "emp.communication_damage": "Communication Networks Damage",
        "emp.button": "Calculate EMP Effects",
        "emp.threshold_note": "Electronic equipment damage threshold: 20,000 V/m",
        "emp.threshold_label": "Damage Threshold",
        "emp.threshold_percentage": "Threshold {percentage}",
        "emp.field_strength_trace": "Field Strength",
        "emp.damage_probability_trace": "Damage Probability",
        "emp.induction_title": "EMP Induction Effects Information",
        "emp.damage_threshold_25": "25% probability of electronic equipment damage",
        "emp.damage_threshold_50": "50% probability of electronic equipment damage",
        "emp.damage_threshold_75": "75% probability of electronic equipment damage",
        "emp.damage_thresholds_note": "Damage thresholds: 25%, 50%, 75% probability of electronic equipment damage",
        "emp.induction_y_axis": "Induction Magnitude (V/m/s)",
        
        # Fallout page
        "nav.fallout": "Fallout Simulation",
        "fallout.header": "Nuclear Fallout Simulation",
        "fallout.yield": "Fallout: Yield (kilotons)",
        "fallout.height": "Burst Height (m)",
        "fallout.fission_fraction": "Fission Fraction",
        "fallout.wind_speed": "Wind Speed (km/h)",
        "fallout.wind_direction": "Wind Direction (degrees)",
        "fallout.time": "Time after detonation",
        "fallout.specific_distance": "Distance from Ground Zero (km)",
        "fallout.dose_rate": "Dose rate at {distance}km after {time} hours: {dose:.4e} rad/hour",
        "fallout.button": "Simulate Fallout Pattern",
        "fallout.pattern_title": "Fallout Pattern after {time} hours",
        "fallout.x_axis": "East-West Distance (km)",
        "fallout.y_axis": "North-South Distance (km)",
        "fallout.dose_rate_unit": "Dose Rate (rad/h)",
        "fallout.info_title": "Fallout Information",
        "fallout.info_note": "Notes about fallout model:",
        "fallout.info_decay": "- The model uses Way-Wigner law (t^-1.2) for radioactive decay",
        "fallout.info_ground": "- Ground bursts produce the most fallout by drawing soil into the fireball",
        "fallout.info_air": "- Air bursts (>2000m) produce very little fallout",
        "fallout.info_wind": "- Wind significantly affects fallout distribution",
        "fallout.info_dose": "- Dose rates above 100 rad/h are extremely dangerous, requiring immediate evacuation",
        
        # Weapon design page
        "nav.weapon_design": "Weapon Design Analysis",
        "weapon.header": "Nuclear Weapon Design Analysis",
        "weapon.type": "Weapon Type",
        "weapon.type_fission": "Fission (atomic)",
        "weapon.type_boosted": "Boosted Fission",
        "weapon.type_thermonuclear": "Thermonuclear (hydrogen)",
        "weapon.yield": "Design Yield (kilotons)",
        "weapon.characteristics": "Design Characteristics",
        "weapon.materials": "Required Materials",
        "weapon.material_type": "Material",
        "weapon.material_amount": "Amount",
        "weapon.parameters": "Design Parameters",
        "weapon.implosion_quality": "Implosion Quality",
        "weapon.neutron_initiator": "Neutron Initiator Efficiency",
        "weapon.tamper_effectiveness": "Tamper Effectiveness",
        "weapon.fission_efficiency": "Fission Core Efficiency",
        "weapon.tritium_amount": "Tritium-Deuterium Amount",
        "weapon.primary_yield": "Primary Stage Fraction",
        "weapon.coupling_efficiency": "Primary-Secondary Coupling",
        "weapon.secondary_burn": "Secondary Stage Burn Fraction",
        "weapon.efficiency": "Total Device Efficiency",
        "weapon.analyze_button": "Analyze Design",
        "weapon.analyzing": "Analyzing design...",
        "weapon.boost_factor": "Boost Factor",
        "weapon.primary_energy": "Primary Stage Energy",
        "weapon.secondary_energy": "Secondary Stage Energy",
        "weapon.material_aluminum": "Aluminum (reflector layer)",
        "weapon.material_conventional": "Conventional explosives",
        "weapon.material_beryllium": "Beryllium (neutron reflector)",
        "weapon.material_pu_primary": "Pu-239 (Primary stage)",
        "weapon.material_lithium": "Lithium-6 Deuteride",
        "weapon.material_u238": "U-238 (Tamper)",
        "weapon.material_tritium": "Tritium-Deuterium",
        
        # Flash effects page
        "nav.flash_effects": "Flash & Eye Effects",
        "flash.header": "Nuclear Flash Effects Simulation",
        "flash.yield": "Flash: Yield (kilotons)",
        "flash.distance": "Flash: Max Distance (km)",
        "flash.height": "Burst Height (m)",
        "flash.illuminance": "Illuminance",
        "flash.illuminance_title": "Peak Illuminance vs Distance",
        "flash.x_axis": "Distance from Ground Zero (km)",
        "flash.y_axis": "Illuminance (lux)",
        "flash.damage_title": "Eye Damage Probability vs Distance",
        "flash.probability": "Probability",
        "flash.temporary_blindness": "Temporary Flash Blindness",
        "flash.retinal_burn": "Retinal Burn",
        "flash.permanent_damage": "Permanent Eye Damage",
        "flash.time_of_day": "Time of Day",
        "flash.time_of_day_help": "Time of day affects pupil dilation and impact on eyes",
        "flash.day_time": "Daytime",
        "flash.twilight": "Twilight/Dawn",
        "flash.night_time": "Night",
        "common.calculating": "Calculating...",
        "flash.info_title": "Information about Flash Effects",
        "flash.condition": "Condition",
        "flash.effects_title": "Nuclear Flash Effects",
        "flash.temporary_blindness_info": "Temporary Blindness",
        "flash.temporary_blindness_desc": "Called \"flash blindness\", lasts from seconds to minutes",
        "flash.retinal_burn_info": "Retinal Burns",
        "flash.retinal_burn_desc": "Thermal damage occurs when retinal temperature increases by 10-20°C",
        "flash.permanent_damage_info": "Permanent Damage",
        "flash.permanent_damage_desc": "Can lead to permanent blindness if the macula is damaged",
        "flash.time_effect_title": "Effect of Time of Day",
        "flash.night_effect": "At night: Pupil dilation is 2.5 times larger, significantly increasing the risk of eye damage",
        "flash.visibility_note": "Nuclear flash can be visible from hundreds of km, even without other effects",
        "flash.peak_illuminance": "Peak Illuminance",
        "flash.temporary_blindness_threshold": "Temporary Blindness Threshold",
        "flash.retinal_burn_threshold": "Retinal Burn Threshold",
        
        # Các thành phần chung
        "conclusions.title": "Scientific Conclusions",
        
        # Chart components
        "chart.neutron_population": "Neutron Population over Time",
        "chart.time_seconds": "Time (seconds)",
        "chart.neutron_count": "Neutron Count",
        "chart.initial_count": "Initial Count",
        "chart.energy_released": "Energy Released over Time",
        "chart.energy_mev": "Energy (MeV)",
        "chart.energy_distribution": "Energy Distribution by Type",
        "chart.blast": "Blast/Pressure",
        "chart.thermal": "Thermal",
        "chart.instant_radiation": "Instant Radiation",
        "chart.delayed_radiation": "Delayed Radiation",
        "chart.fast_neutrons": "Fast Neutrons",
        "chart.damage_thresholds": "Damage Thresholds",
        "chart.window_breakage": "Window Breakage",
        "chart.moderate_damage": "Moderate Building Damage",
        "chart.severe_damage": "Most Houses Collapse",
        "chart.reinforced_damage": "Reinforced Concrete Damaged",
        "chart.neutron_flux": "Neutron Flux Distribution",
        "chart.position": "Position (cm)",
        "chart.flux": "Neutron Flux (arbitrary units)",
        "chart.neutron_flux_2d": "2D Neutron Flux Distribution",
        "chart.overpressure": "Overpressure",
        "chart.interaction_distribution": "Neutron Interaction Distribution",
        "chart.interaction_type": "Interaction Type",
        "chart.count": "Count",
        "chart.path_length_distribution": "Neutron Path Length Distribution",
        "chart.path_length": "Path Length (cm)",
        "chart.frequency": "Frequency",
        "chart.final_position": "Final Position Distribution",
        "chart.radial_position": "Radial Position (cm)",
        "chart.system_boundary": "System Boundary",
        "chart.neutron_generation": "Neutron Population by Generation",
        "chart.generation": "Generation",
        "chart.subcritical": "System is subcritical (k < 1)",
        "chart.supercritical": "System is supercritical (k > 1)",
        "chart.critical": "System is near critical (k ≈ 1)",
        "chart.detonation_center": "Detonation Center",
        "chart.wind_direction": "Wind Direction",
        
        # Help text translations
        "help.energy_kt": "Energy of explosion in kilotons",
        "help.weapon_yield": "Weapon design yield in kilotons",
        "help.max_distance_km": "Maximum distance from ground zero in kilometers",
        "help.max_distance_m": "Maximum distance from ground zero in meters",
        "help.burst_height_m": "Burst height in meters",
        "help.burst_height_km": "Burst height in kilometers",
        "help.density": "Ambient air density, default is 1.225 kg/m³ (air density at sea level)",
        "help.time_after_s": "Time after detonation in seconds",
        "help.time_after_h": "Time after detonation in hours",
        "help.system_radius": "Radius of the system in cm",
        "help.neutron_count": "Number of neutrons to simulate",
        "help.initial_distribution": "Initial spatial distribution of neutrons",
        "help.fission_xs": "Fission cross-section",
        "help.scattering_xs": "Scattering cross-section",
        "help.absorption_xs": "Absorption cross-section",
        "help.avg_neutrons": "Average number of neutrons produced by each fission reaction",
        "help.energy_groups": "Number of energy groups for multi-group calculations (1 = single group)",
        "help.max_generations": "Maximum number of generations for chain fission simulation",
        "help.show_progress": "Show progress bar during simulation",
        "help.simulate_chain": "Simulate fission chain reaction to calculate k-effective neutron multiplication factor",
        "help.multi_core": "Accelerate simulation by using multiple CPU cores",
        "help.system_size": "System size in cm",
        "help.spatial_resolution": "Spatial resolution",
        "help.enrichment": "Enrichment of uranium-235",
        "help.geometry": "Shape of fissionable material",
        "help.initial_neutrons": "Number of initial neutrons",
        "help.mass_ratio": "Ratio compared to critical mass",
        "help.fission_fraction": "Energy fraction from fission",
        "help.wind_speed": "Wind speed (km/h)",
        "help.wind_direction": "Wind direction in degrees (0=North, 90=East, 180=South, 270=West)",
        "help.specific_distance": "Specific distance from center to display dose rate",
        "help.conductivity": "Surface conductivity, in S/m (Siemens/meter)",
        "help.primary_fraction": "Energy fraction from primary stage",
        "help.tritium": "Amount in grams"
    },
    "vi": {
        "app.title": "Mô Phỏng Vật Lý Hạt Nhân",
        "app.description": "Bảng điều khiển này cung cấp các mô phỏng tương tác về các quá trình vật lý liên quan đến phản ứng hạt nhân và nổ hạt nhân.",
        "app.page_title": "Mô Phỏng Vật Lý Hạt Nhân",
        "app.icon": "☢️",
        "app.menu.get_help": "https://github.com/luyen-tran/nuclear-simulation-tool/issues",
        "app.menu.report_bug": "https://github.com/luyen-tran/nuclear-simulation-tool/issues",
        "app.menu.about": "# Mô Phỏng Vật Lý Hạt Nhân\nPhần mềm mô phỏng vật lý hạt nhân.",
        "nav.chain_reaction": "Khối Lượng Tới Hạn & Phản Ứng Dây Chuyền",
        "nav.neutron_transport": "Phương Trình Vận Chuyển Nơtron",
        "nav.monte_carlo": "Mô Hình Monte Carlo",
        "nav.blast_wave": "Mô Phỏng Sóng Xung Kích",
        "nav.thermal_radiation": "Hiệu Ứng Bức Xạ Nhiệt",
        "footer.text": "Bảng Điều Khiển Mô Phỏng Vật Lý Hạt Nhân",
        "footer.links": "Liên kết",
        "footer.documentation": "Tài liệu",
        "footer.info": "Thông tin",
        "footer.version": "Phiên bản: {version}",
        "footer.last_updated": "Cập nhật lần cuối: {date}",
        "select.simulation": "Chọn Mô Phỏng",
        "language.selector": "Ngôn ngữ / Language",
        
        # Simulation categories
        "select.category": "Phân Loại Mô Phỏng",
        "category.theoretical": "Mô Hình Lý Thuyết",
        "category.practical": "Hiệu Ứng Thực Tế",
        
        # Theme settings
        "theme.light": "Sáng",
        "theme.dark": "Tối",
        "theme.system": "Sử dụng giao diện hệ thống",
        "theme.settings": "Cài Đặt Giao Diện",
        "theme.selector": "Chọn Giao Diện",
        "theme.apply_changes": "Nhấp vào nút 'Áp dụng giao diện mới' ở trên để thực hiện thay đổi.",
        "theme.use_system": "Ứng dụng sẽ sử dụng giao diện của hệ thống.",
        
        # Chain reaction page
        "chain.header": "Khối Lượng Tới Hạn & Phản Ứng Dây Chuyền",
        "chain.enrichment": "Độ Làm Giàu U-235",
        "chain.geometry": "Hình Dạng",
        "chain.geometry.sphere": "Hình cầu",
        "chain.geometry.cylinder": "Hình trụ",
        "chain.geometry.slab": "Tấm phẳng",
        "chain.neutrons": "Số Nơtron Ban Đầu",
        "chain.mass_ratio": "Tỷ Lệ Khối Lượng (so với Tới Hạn)",
        "chain.critical_mass": "Khối lượng tới hạn tính toán: {mass:.2f} kg",
        "chain.button": "Chạy Mô Phỏng Phản Ứng Dây Chuyền",
        
        # Neutron transport page
        "transport.header": "Phân Tích Phương Trình Vận Chuyển Nơtron",
        "transport.size": "Kích Thước Hệ Thống (cm)",
        "transport.resolution": "Độ Phân Giải Không Gian",
        "transport.scattering": "Tiết Diện Tán Xạ (cm⁻¹)",
        "transport.absorption": "Tiết Diện Hấp Thụ (cm⁻¹)",
        "transport.fission": "Tiết Diện Phân Hạch (cm⁻¹)",
        "transport.button": "Giải Phương Trình Vận Chuyển Nơtron",
        "transport.button_label": "Giải Phương Trình Vận Chuyển Nơtron",
        
        # Monte Carlo page
        "monte.header": "Mô Hình Monte Carlo cho Phản Ứng Hạt Nhân",
        "monte.radius": "Bán Kính Hệ Thống (cm)",
        "monte.num_neutrons": "Số Lượng Nơtron",
        "monte.fission": "MC: Tiết Diện Phân Hạch (cm⁻¹)",
        "monte.scattering": "MC: Tiết Diện Tán Xạ (cm⁻¹)",
        "monte.absorption": "MC: Tiết Diện Hấp Thụ (cm⁻¹)",
        "monte.button": "Chạy Mô Phỏng Monte Carlo",
        "monte.fissions": "Phân Hạch",
        "monte.absorptions": "Hấp Thụ",
        "monte.escapes": "Thoát Ra Ngoài",
        "monte.advanced_options": "Tùy Chọn Nâng Cao",
        "monte.average_fission_neutrons": "Số nơtron trung bình mỗi phân hạch",
        "monte.show_progress": "Hiển thị thanh tiến trình",
        "monte.simulate_fission_chain": "Mô phỏng chuỗi phân hạch",
        "monte.execution_time": "Thời gian thực thi: {time:.2f} giây",
        "monte.k_effective": "Hệ số nhân hiệu dụng (k-eff): {value:.4f} ± {error:.4f}",
        
        # Blast wave page
        "blast.header": "Mô Hình Sóng Xung Kích Sedov-Taylor",
        "blast.yield": "Năng Lượng (kiloton)",
        "blast.distance": "Khoảng Cách Tối Đa (m)",
        "blast.density": "Mật Độ Môi Trường (kg/m³)",
        "blast.time": "Thời Gian Sau Vụ Nổ (giây)",
        "blast.radius": "Bán kính sóng xung kích tại thời điểm {time} giây: {radius:.2f} mét",
        "blast.button": "Mô Phỏng Lan Truyền Sóng Xung Kích",
        "blast.chart_title": "Áp Suất Tăng Của Sóng Xung Kích tại t = {time} giây",
        "blast.chart_title_animation": "Lan Truyền Sóng Xung Kích Theo Thời Gian",
        "blast.x_axis": "Khoảng Cách từ Tâm Nổ (m)",
        "blast.y_axis": "Áp Suất Tăng (kPa)",
        "blast.play_button": "Phát",
        "blast.shock_front": "Mặt Sóng Xung Kích",
        "blast.damage_level_1": "Thiệt hại nhẹ (kính cửa sổ vỡ)",
        "blast.damage_level_2": "Thiệt hại nhẹ đến công trình (kính cửa sổ vỡ hoàn toàn)",
        "blast.damage_level_3": "Thiệt hại trung bình đến công trình gia cố",
        "blast.damage_level_4": "Hầu hết các tòa nhà dân cư sụp đổ",
        "blast.damage_level_5": "Công trình bê tông cốt thép bị hư hại nghiêm trọng",
        "blast.damage_level_6": "Phá hủy hoàn toàn hầu hết các công trình",
        "blast.report_title": "Báo Cáo Phân Tích Vụ Nổ Hạt Nhân",
        "blast.report_subtitle": "Kết Quả Mô Hình Sóng Xung Kích Sedov-Taylor",
        "blast.report_intro": "Báo cáo này trình bày kết quả mô phỏng sóng xung kích Sedov-Taylor được sử dụng cho mục đích giáo dục.",
        "blast.report_distance": "Các hiệu ứng tại khoảng cách {distance} mét từ tâm vụ nổ:",
        "blast.report_pressure": "Áp suất đỉnh: {pressure:.2f} kPa",
        "blast.report_wind": "Tốc độ gió đỉnh: {speed:.2f} m/s",
        "blast.report_arrival": "Thời gian sóng xung kích tới: {time:.2f} giây",
        "blast.report_thermal": "Bức xạ nhiệt: {thermal:.2e} J/m²",
        "blast.report_radiation_initial": "Bức xạ ban đầu: {radiation:.2e} Gy",
        "blast.report_radiation_fallout": "Bức xạ phóng xạ rơi (1 giờ): {fallout:.2e} Gy",
        
        # Thermal radiation page
        "thermal.header": "Mô Phỏng Tác Động Nhiệt và Bức Xạ",
        "thermal.yield": "Nhiệt: Năng Lượng (kiloton)",
        "thermal.distance": "Nhiệt: Khoảng Cách Tối Đa (km)",
        "thermal.height": "Độ Cao Nổ (m)",
        "thermal.energy_title": "Mật Độ Năng Lượng Nhiệt theo Khoảng Cách",
        "thermal.energy_x_axis": "Khoảng Cách từ Tâm Nổ (km)",
        "thermal.energy_y_axis": "Mật Độ Năng Lượng Nhiệt (J/m²)",
        "thermal.burn_title": "Xác Suất Bỏng theo Khoảng Cách",
        "thermal.burn_x_axis": "Khoảng Cách từ Tâm Nổ (km)",
        "thermal.burn_y_axis": "Xác Suất",
        "thermal.first_degree": "Bỏng Độ 1",
        "thermal.second_degree": "Bỏng Độ 2",
        "thermal.third_degree": "Bỏng Độ 3",
        "thermal.button": "Mô phỏng hiệu ứng bức xạ nhiệt",
        
        # EMP effects page
        "nav.emp_effects": "Hiệu Ứng Xung Điện Từ",
        "emp.header": "Mô Phỏng Xung Điện Từ (EMP)",
        "emp.yield": "EMP: Năng Lượng (kiloton)",
        "emp.distance": "EMP: Khoảng Cách Tối Đa (km)",
        "emp.height": "Độ Cao Nổ (km)",
        "emp.conductivity": "Độ Dẫn Điện Mặt Đất (S/m)",
        "emp.field_strength": "Cường Độ Điện Trường",
        "emp.field_strength_title": "Cường Độ Điện Trường EMP theo Khoảng Cách",
        "emp.x_axis": "Khoảng Cách từ Tâm Nổ (km)",
        "emp.y_axis": "Cường Độ Điện Trường (V/m)",
        "emp.damage_title": "Xác Suất Hư Hỏng do EMP theo Khoảng Cách",
        "emp.probability": "Xác Suất",
        "emp.electronic_damage": "Hư Hỏng Thiết Bị Điện Tử",
        "emp.power_grid_damage": "Hư Hỏng Lưới Điện",
        "emp.communication_damage": "Hư Hỏng Mạng Thông Tin",
        "emp.button": "Tính Toán Hiệu Ứng EMP",
        "emp.threshold_note": "Ngưỡng hư hỏng thiết bị điện tử: 20.000 V/m",
        "emp.threshold_label": "Ngưỡng hư hỏng",
        "emp.threshold_percentage": "Ngưỡng {percentage}",
        "emp.field_strength_trace": "Cường độ điện trường",
        "emp.damage_probability_trace": "Xác suất hư hỏng",
        "emp.induction_title": "Thông Tin về Hiệu Ứng Cảm Ứng EMP",
        "emp.damage_threshold_25": "25% xác suất hư hỏng thiết bị điện tử",
        "emp.damage_threshold_50": "50% xác suất hư hỏng thiết bị điện tử",
        "emp.damage_threshold_75": "75% xác suất hư hỏng thiết bị điện tử",
        "emp.damage_thresholds_note": "Các ngưỡng hư hỏng: 25%, 50%, 75% xác suất hư hỏng thiết bị điện tử",
        "emp.induction_y_axis": "Cường Độ Cảm Ứng (V/m/s)",
        
        # Fallout page
        "nav.fallout": "Mô Phỏng Phóng Xạ Rơi",
        "fallout.header": "Mô Phỏng Phóng Xạ Rơi Hạt Nhân",
        "fallout.yield": "Phóng Xạ: Năng Lượng (kiloton)",
        "fallout.height": "Độ Cao Nổ (m)",
        "fallout.fission_fraction": "Tỷ Lệ Phân Hạch",
        "fallout.wind_speed": "Tốc Độ Gió (km/h)",
        "fallout.wind_direction": "Hướng Gió (độ)",
        "fallout.time": "Thời gian sau vụ nổ",
        "fallout.specific_distance": "Khoảng Cách từ Tâm Nổ (km)",
        "fallout.dose_rate": "Liều lượng tại {distance} km sau {time} giờ: {dose:.4e} rad/giờ",
        "fallout.button": "Mô Phỏng Phân Bố Phóng Xạ Rơi",
        "fallout.pattern_title": "Phân Bố Phóng Xạ Rơi sau {time} giờ",
        "fallout.x_axis": "Khoảng Cách Đông-Tây (km)",
        "fallout.y_axis": "Khoảng Cách Bắc-Nam (km)",
        "fallout.dose_rate_unit": "Liều Lượng (rad/h)",
        "fallout.info_title": "Thông tin về phóng xạ rơi",
        "fallout.info_note": "Lưu ý về mô hình phóng xạ rơi:",
        "fallout.info_decay": "- Mô hình sử dụng định luật Way-Wigner (t^-1.2) cho sự phân rã phóng xạ",
        "fallout.info_ground": "- Vụ nổ mặt đất tạo ra phóng xạ rơi nhiều nhất do cuốn đất vào quả cầu lửa",
        "fallout.info_air": "- Vụ nổ trên không (>2.000 m) tạo ra phóng xạ rơi rất ít",
        "fallout.info_wind": "- Gió ảnh hưởng đáng kể đến sự phân bố phóng xạ rơi",
        "fallout.info_dose": "- Liều lượng trên 100 rad/h cực kỳ nguy hiểm, cần sơ tán ngay lập tức",
        
        # Weapon design page
        "nav.weapon_design": "Phân Tích Thiết Kế Vũ Khí",
        "weapon.header": "Phân Tích Thiết Kế Vũ Khí Hạt Nhân",
        "weapon.type": "Loại Vũ Khí",
        "weapon.type_fission": "Phân Hạch (nguyên tử)",
        "weapon.type_boosted": "Phân Hạch Tăng Cường",
        "weapon.type_thermonuclear": "Nhiệt Hạch (hydro)",
        "weapon.yield": "Năng Lượng Thiết Kế (kiloton)",
        "weapon.characteristics": "Đặc Điểm Thiết Kế",
        "weapon.materials": "Vật Liệu Cần Thiết",
        "weapon.material_type": "Vật Liệu",
        "weapon.material_amount": "Số Lượng",
        "weapon.parameters": "Tham Số Thiết Kế",
        "weapon.implosion_quality": "Chất Lượng Bộ Nén",
        "weapon.neutron_initiator": "Hiệu Suất Bộ Khơi Mào Nơtron",
        "weapon.tamper_effectiveness": "Hiệu Quả Lớp Vỏ Đệm",
        "weapon.fission_efficiency": "Hiệu Suất Lõi Phân Hạch",
        "weapon.tritium_amount": "Lượng Tritium-Deuterium",
        "weapon.primary_yield": "Tỷ Lệ Giai Đoạn Sơ Cấp",
        "weapon.coupling_efficiency": "Hiệu Quả Ghép Nối Sơ Cấp-Thứ Cấp",
        "weapon.secondary_burn": "Tỷ Lệ Cháy Giai Đoạn Thứ Cấp",
        "weapon.efficiency": "Hiệu Suất Tổng Thể",
        "weapon.analyze_button": "Phân tích thiết kế",
        "weapon.analyzing": "Đang phân tích thiết kế...",
        "weapon.boost_factor": "Hệ số tăng cường",
        "weapon.primary_energy": "Năng lượng giai đoạn sơ cấp",
        "weapon.secondary_energy": "Năng lượng giai đoạn thứ cấp",
        "weapon.material_aluminum": "Nhôm (lớp phản xạ)",
        "weapon.material_conventional": "Thuốc nổ thông thường",
        "weapon.material_beryllium": "Berili (phản xạ nơtron)",
        "weapon.material_pu_primary": "Pu-239 (Giai đoạn sơ cấp)",
        "weapon.material_lithium": "Lithi-6 Deuteride",
        "weapon.material_u238": "U-238 (Vỏ bọc)",
        "weapon.material_tritium": "Tritium-Deuterium",
        
        # Flash effects page
        "nav.flash_effects": "Hiệu Ứng Ánh Chớp & Mắt",
        "flash.header": "Mô Phỏng Hiệu Ứng Ánh Chớp Hạt Nhân",
        "flash.yield": "Ánh Chớp: Năng Lượng (kiloton)",
        "flash.distance": "Ánh Chớp: Khoảng Cách Tối Đa (km)",
        "flash.height": "Độ Cao Nổ (m)",
        "flash.illuminance": "Độ Sáng",
        "flash.illuminance_title": "Độ Sáng Đỉnh theo Khoảng Cách",
        "flash.x_axis": "Khoảng Cách từ Tâm Nổ (km)",
        "flash.y_axis": "Độ Sáng (lux)",
        "flash.damage_title": "Xác Suất Tổn Thương Mắt theo Khoảng Cách",
        "flash.probability": "Xác Suất",
        "flash.temporary_blindness": "Mù Tạm Thời do Ánh Chớp",
        "flash.retinal_burn": "Bỏng Võng Mạc",
        "flash.permanent_damage": "Tổn Thương Mắt Vĩnh Viễn",
        "flash.time_of_day": "Thời điểm trong ngày",
        "flash.time_of_day_help": "Thời điểm trong ngày ảnh hưởng đến độ giãn đồng tử và tác động đến mắt",
        "flash.day_time": "Ban ngày",
        "flash.twilight": "Hoàng hôn/Bình minh",
        "flash.night_time": "Ban đêm",
        "common.calculating": "Đang tính toán...",
        "flash.info_title": "Thông tin về hiệu ứng ánh chớp",
        "flash.condition": "Điều kiện",
        "flash.effects_title": "Hiệu Ứng ánh chớp hạt nhân",
        "flash.temporary_blindness_info": "Mù tạm thời",
        "flash.temporary_blindness_desc": "Gọi là \"mù do ánh chớp\", kéo dài từ vài giây đến vài phút",
        "flash.retinal_burn_info": "Bỏng võng mạc",
        "flash.retinal_burn_desc": "Tổn thương nhiệt xảy ra khi nhiệt độ võng mạc tăng 10-20°C",
        "flash.permanent_damage_info": "Tổn thương vĩnh viễn",
        "flash.permanent_damage_desc": "Có thể dẫn đến mù vĩnh viễn nếu vùng hoàng điểm bị tổn thương",
        "flash.time_effect_title": "Ảnh hưởng của thời điểm trong ngày",
        "flash.night_effect": "Ban đêm: Đồng tử giãn lớn hơn gấp 2,5 lần, làm tăng đáng kể nguy cơ tổn thương mắt",
        "flash.visibility_note": "Ánh chớp hạt nhân có thể nhìn thấy từ hàng trăm km, ngay cả khi không có hiệu ứng khác",
        "flash.peak_illuminance": "Độ sáng đỉnh",
        "flash.temporary_blindness_threshold": "Ngưỡng mù tạm thời",
        "flash.retinal_burn_threshold": "Ngưỡng bỏng võng mạc",
        
        # Các thành phần chung
        "conclusions.title": "Kết Luận Khoa Học",
        
        # Chart components
        "chart.neutron_population": "Số Lượng Nơtron theo Thời gian",
        "chart.time_seconds": "Thời gian (giây)",
        "chart.neutron_count": "Số lượng Nơtron",
        "chart.initial_count": "Số lượng Ban đầu",
        "chart.energy_released": "Năng lượng Giải phóng theo Thời gian",
        "chart.energy_mev": "Năng lượng (MeV)",
        "chart.energy_distribution": "Phân bố Năng lượng theo Loại",
        "chart.blast": "Sóng Xung Kích/Áp suất",
        "chart.thermal": "Nhiệt",
        "chart.instant_radiation": "Bức xạ Tức thời",
        "chart.delayed_radiation": "Bức xạ Chậm",
        "chart.fast_neutrons": "Nơtron Nhanh",
        "chart.damage_thresholds": "Ngưỡng Thiệt hại",
        "chart.window_breakage": "Cửa kính vỡ",
        "chart.moderate_damage": "Thiệt hại công trình trung bình",
        "chart.severe_damage": "Đa số nhà sập đổ",
        "chart.reinforced_damage": "Bê tông cốt thép hư hại",
        "chart.neutron_flux": "Phân bố thông lượng nơtron",
        "chart.position": "Vị trí (cm)",
        "chart.flux": "Thông lượng nơtron (đơn vị tương đối)",
        "chart.neutron_flux_2d": "Phân bố thông lượng nơtron 2D",
        "chart.overpressure": "Áp suất tăng",
        "chart.interaction_distribution": "Phân bố tương tác Nơtron",
        "chart.interaction_type": "Loại tương tác",
        "chart.count": "Số lượng",
        "chart.path_length_distribution": "Phân bố độ dài đường đi Nơtron",
        "chart.path_length": "Độ dài đường đi (cm)",
        "chart.frequency": "Tần suất",
        "chart.final_position": "Phân bố vị trí cuối cùng",
        "chart.radial_position": "Vị trí bán kính (cm)",
        "chart.system_boundary": "Ranh giới hệ thống",
        "chart.neutron_generation": "Số lượng Nơtron theo thế hệ",
        "chart.generation": "Thế hệ",
        "chart.subcritical": "Hệ thống dưới tới hạn (k < 1)",
        "chart.supercritical": "Hệ thống siêu tới hạn (k > 1)",
        "chart.critical": "Hệ thống gần tới hạn (k ≈ 1)",
        "chart.detonation_center": "Tâm vụ nổ",
        "chart.wind_direction": "Hướng gió",
        
        # Help text translations
        "help.energy_kt": "Năng lượng vụ nổ tính bằng kiloton",
        "help.weapon_yield": "Năng lượng thiết kế vũ khí tính bằng kiloton",
        "help.max_distance_km": "Khoảng cách tối đa từ tâm nổ tính bằng kilômét",
        "help.max_distance_m": "Khoảng cách tối đa từ tâm nổ tính bằng mét",
        "help.burst_height_m": "Độ cao nổ tính bằng mét",
        "help.burst_height_km": "Độ cao nổ tính bằng kilômét",
        "help.density": "Mật độ không khí môi trường, mặc định là 1,225 kg/m³ (mật độ không khí ở mực nước biển)",
        "help.time_after_s": "Thời gian sau vụ nổ tính bằng giây",
        "help.time_after_h": "Thời gian sau vụ nổ tính bằng giờ",
        "help.system_radius": "Bán kính của hệ thống tính bằng centimét",
        "help.neutron_count": "Số lượng nơtron dùng để mô phỏng",
        "help.initial_distribution": "Phân bố không gian ban đầu của nơtron",
        "help.fission_xs": "Tiết diện phân hạch",
        "help.scattering_xs": "Tiết diện tán xạ",
        "help.absorption_xs": "Tiết diện hấp thụ",
        "help.avg_neutrons": "Số nơtron trung bình sinh ra từ mỗi phản ứng phân hạch",
        "help.energy_groups": "Số nhóm năng lượng cho tính toán đa nhóm (1 = một nhóm)",
        "help.max_generations": "Số thế hệ tối đa cho mô phỏng chuỗi phân hạch",
        "help.show_progress": "Hiển thị thanh tiến trình trong quá trình mô phỏng",
        "help.simulate_chain": "Mô phỏng chuỗi phản ứng phân hạch để tính hệ số nhân nơtron k-hiệu dụng",
        "help.multi_core": "Tăng tốc mô phỏng bằng cách sử dụng nhiều nhân CPU",
        "help.system_size": "Kích thước hệ thống tính bằng centimét",
        "help.spatial_resolution": "Độ phân giải không gian",
        "help.enrichment": "Độ làm giàu của uranium-235",
        "help.geometry": "Hình dạng của vật liệu phân hạch",
        "help.initial_neutrons": "Số lượng nơtron ban đầu",
        "help.mass_ratio": "Tỷ lệ so với khối lượng tới hạn",
        "help.fission_fraction": "Tỷ lệ năng lượng từ phân hạch",
        "help.wind_speed": "Tốc độ gió (km/h)",
        "help.wind_direction": "Hướng gió tính theo độ (0=Bắc, 90=Đông, 180=Nam, 270=Tây)",
        "help.specific_distance": "Khoảng cách cụ thể từ tâm để hiển thị liều lượng",
        "help.conductivity": "Độ dẫn điện của bề mặt, đơn vị S/m (Siemens/mét)",
        "help.primary_fraction": "Tỷ lệ năng lượng từ giai đoạn sơ cấp",
        "help.tritium": "Khối lượng tính bằng gam"
    }
}