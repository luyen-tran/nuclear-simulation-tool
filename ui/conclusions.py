"""
Tệp chứa kết luận khoa học cho các mô hình
"""

conclusions = {
    "en": {
        "chain_reaction": """
        ### Scientific Conclusions on Nuclear Chain Reactions
        
        The chain reaction simulation demonstrates several key principles of nuclear fission:
        
        1. **Critical Mass Dependency**: The simulation shows how the chain reaction behavior dramatically changes around the critical mass threshold. Below this threshold, the reaction dies out; above it, exponential growth occurs.
        
        2. **Enrichment Effects**: Higher uranium enrichment reduces critical mass requirements significantly, explaining why weapons-grade uranium requires much higher enrichment than reactor fuel.
        
        3. **Neutron Population Dynamics**: The exponential growth of neutron population in supercritical assemblies follows well-established mathematical models, with doubling times that depend on reactivity.
        
        4. **Energy Release Characteristics**: The rapid energy release in supercritical assemblies shows why uncontrolled chain reactions can lead to explosive yield in milliseconds to microseconds.
        
        This simulation provides educational value in understanding nuclear weapon physics while avoiding details that would enable actual weapon development.
        """,
        
        "neutron_transport": """
        ### Scientific Conclusions on Neutron Transport
        
        The neutron transport simulation reveals important aspects of how neutrons move and interact within fissile materials:
        
        1. **Spatial Distribution Effects**: The simulation demonstrates how neutron flux varies spatially within a system, with higher concentrations in central regions and gradual decreases toward boundaries.
        
        2. **Cross-Section Sensitivity**: Results show high sensitivity to changes in cross-sections (especially fission and absorption), illustrating why precise nuclear data is critical for accurate modeling.
        
        3. **Geometry Impact**: Different geometries create distinctive neutron distribution patterns that affect criticality and overall system behavior.
        
        4. **Leakage Phenomena**: The simulation captures neutron leakage at boundaries, a crucial factor in determining whether a system can sustain a chain reaction.
        
        These principles are fundamental to nuclear reactor design, criticality safety, and understanding weapon physics.
        """,
        
        "monte_carlo": """
        ### Scientific Conclusions on Monte Carlo Neutron Modeling
        
        The Monte Carlo simulation provides probabilistic insights into neutron behavior:
        
        1. **Statistical Nature of Nuclear Reactions**: The simulation demonstrates the inherently probabilistic nature of neutron interactions, showing why statistical approaches are necessary for accurate modeling.
        
        2. **Cross-Section Effects**: Results show how different cross-sections influence neutron population behavior, including scattering, absorption, and fission.
        
        3. **Fission Chain Analysis**: Generation-to-generation analysis provides clear pictures of multiplication factors and criticality conditions.
        
        4. **Path Length Distributions**: Simulation reveals characteristic path length distributions dependent on material properties, critical for shielding and criticality calculations.
        
        5. **System Size Effects**: Results illustrate how finite geometry affects neutron escape probabilities and system criticality.
        
        The Monte Carlo approach represents the gold standard in nuclear system modeling when high accuracy is required.
        """,
        
        "blast_wave": """
        ### Scientific Conclusions on Blast Wave Effects
        
        The Sedov-Taylor blast wave model illustrates several important physical principles:
        
        1. **Energy-Distance Scaling**: The simulation confirms that overpressure decreases with distance according to established scaling laws, with initial scaling approximately proportional to r^-3 and transitioning to r^-1 for the shock front.
        
        2. **Temporal Evolution**: Results show how the blast wave evolves and attenuates over time, with initial rapid expansion followed by decreasing propagation speeds.
        
        3. **Energy Dependence**: The simulation illustrates the relationship between explosion energy and damage radius, approximating the cube root scaling law.
        
        4. **Atmospheric Effects**: The model shows how environmental density affects blast wave propagation, explaining why altitude and weather conditions influence nuclear blast effects.
        
        5. **Structural Damage Correlation**: The relationship between overpressure levels and structural damage is clearly displayed, providing context for understanding historical nuclear test data.
        
        These principles help understand both nuclear weapon impacts and large conventional explosions.
        """,
        
        "thermal_radiation": """
        ### Scientific Conclusions on Thermal Radiation Effects
        
        The thermal radiation simulation highlights several key phenomena:
        
        1. **Energy Distribution**: Approximately 35% of nuclear explosion energy is released as thermal radiation, creating significant thermal effects at large distances.
        
        2. **Inverse Square Law**: Thermal energy density follows the inverse square law with distance, modulated by atmospheric attenuation factors.
        
        3. **Pulse Characteristics**: The thermal pulse from a nuclear explosion has characteristic time profiles depending on yield, with larger yields producing longer pulses.
        
        4. **Material Response**: Different materials exhibit different ignition thresholds and burning behaviors when exposed to thermal radiation, explaining burn damage patterns following historical nuclear events.
        
        5. **Biological Effects**: The simulation shows how thermal exposure correlates with different burn degrees, explaining medical observations from historical nuclear explosions.
        
        6. **Atmospheric Effects**: Atmospheric conditions significantly modulate thermal radiation transmission, with foggy or cloudy conditions reducing thermal effects.
        
        Understanding these effects is crucial for both historical analysis and civil defense planning.
        """,
        
        "emp_effects": """
        ### Scientific Conclusions on EMP Effects
        
        The Electromagnetic Pulse (EMP) simulation reveals several important aspects of nuclear EMP:
        
        1. **High-Altitude Amplification**: The simulation confirms how high-altitude nuclear detonations create significantly stronger and wider EMP effects through interaction with Earth's magnetic field.
        
        2. **Spectral Characteristics**: Nuclear EMP comprises short-duration E1, intermediate E2, and longer-lasting E3 components, each affecting different types of infrastructure.
        
        3. **Technology Vulnerability**: Modern electronics with microprocessors and integrated circuits exhibit extreme vulnerability compared to older vacuum tube technology, explaining why EMP is a greater concern today than in the early nuclear era.
        
        4. **Protection Methods**: The simulation demonstrates the effectiveness of Faraday cages and other shielding methods in mitigating EMP effects.
        
        5. **Critical Infrastructure Issues**: Power grids and communication networks exhibit particular vulnerability due to their extensive conductive networks that can act as antennas for EMP.
        
        Understanding EMP effects is critical for protecting critical infrastructure, military operations, and disaster preparedness.
        """,
        
        "fallout": """
        ### Scientific Conclusions on Nuclear Fallout
        
        The fallout simulation illustrates several key principles of nuclear fallout:
        
        1. **Height Dependency**: Surface or near-surface bursts produce significantly more fallout than airburst detonations, due to the entrainment of soil into the fireball.
        
        2. **Weather Effects**: Wind patterns strongly influence fallout distribution, creating asymmetric contamination patterns downwind from ground zero.
        
        3. **Decay Characteristics**: The t^-1.2 decay law (Way-Wigner relationship) accurately predicts overall radiation decrease over time, although specific isotopes have different half-lives.
        
        4. **Hotspot Formation**: The simulation shows how terrain features and weather conditions can create concentrated fallout "hotspots" far from the detonation point.
        
        5. **Dose Rate Distribution**: Radiation levels from fallout follow complex patterns based on time, distance, and weather conditions, explaining why fallout monitoring requires sophisticated measurement networks.
        
        6. **Long-Term Effects**: While the strongest radiation occurs in the first few days, some areas may remain contaminated for years or decades due to long-lived isotopes.
        
        This understanding is critical for civil defense planning, post-nuclear event management, and historical analysis.
        """,
        
        "weapon_design": """
        ### Scientific Conclusions on Nuclear Weapon Physics
        
        The weapon physics simulation illustrates several fundamental principles:
        
        1. **Efficiency Limitations**: The simulation shows why nuclear weapons typically achieve only a fraction of their theoretical yield, with various design factors affecting efficiency.
        
        2. **Boosting Effects**: Fusion boosting significantly improves fission weapon efficiency without requiring a full two-stage thermonuclear design.
        
        3. **Staging Principles**: The Teller-Ulam two-stage design enables yield ratios far beyond what is achievable with pure fission devices, explaining the developmental pathway of thermonuclear weapons.
        
        4. **Material Requirements**: The simulation shows how different designs require different amounts and types of nuclear material, explaining historical development challenges.
        
        5. **Size-Yield Relationship**: The relationship between weapon size, mass, and yield helps explain the historical miniaturization of nuclear weapons.
        
        This simulation provides educational value in understanding nuclear weapon physics while avoiding details that would enable actual weapon development.
        """,
        
        "flash_effects": """
        ### Scientific Conclusions on Nuclear Flash Effects
        
        The nuclear flash simulation highlights several important phenomena:
        
        1. **Intensity Scale**: The simulation illustrates the unprecedented intensity of nuclear light, many orders of magnitude brighter than any natural light source, explaining why eye injuries occurred at great distances in historical tests.
        
        2. **Pulse Characteristics**: Nuclear light has temporal characteristics with an extremely bright initial peak followed by longer-lasting thermal radiation.
        
        3. **Eye Injury Mechanisms**: Different eye injury mechanisms (flash blindness, retinal burns, corneal damage) depend on intensity, spectral distribution, and viewing orientation.
        
        4. **Distance Dependence**: The simulation shows how light effects follow inverse square relationship with distance, modulated by atmospheric attenuation.
        
        5. **Time-of-Day Factor**: Pupil dilation at night significantly increases vulnerability to flash effects, explaining historical observations of greater eye injury ranges at night.
        
        Understanding these effects remains important for historical analysis and medical preparedness.
        """
    },
    "vi": {
        "chain_reaction": """
        ### Kết Luận Khoa Học về Phản Ứng Dây Chuyền Hạt Nhân
        
        Mô phỏng phản ứng dây chuyền minh họa các nguyên tắc cơ bản của phân hạch hạt nhân:
        
        1. **Sự Phụ Thuộc Khối Lượng Tới Hạn**: Mô phỏng cho thấy hành vi phản ứng dây chuyền thay đổi mạnh mẽ xung quanh ngưỡng khối lượng tới hạn. Dưới ngưỡng này, phản ứng tắt dần; trên ngưỡng này, sự tăng trưởng theo hàm mũ xảy ra.
        
        2. **Ảnh Hưởng của Độ Giàu**: Độ giàu uranium cao hơn làm giảm đáng kể yêu cầu khối lượng tới hạn, giải thích tại sao uranium cấp vũ khí yêu cầu độ giàu cao hơn nhiều so với nhiên liệu cho lò phản ứng.
        
        3. **Động Lực Quần Thể Neutron**: Sự tăng trưởng theo hàm mũ của quần thể neutron trong các hệ siêu tới hạn tuân theo các mô hình toán học đã được thiết lập, với thời gian nhân đôi phụ thuộc vào tính phản ứng.
        
        4. **Đặc Điểm Giải Phóng Năng Lượng**: Sự giải phóng năng lượng nhanh chóng trong các hệ siêu tới hạn cho thấy tại sao phản ứng dây chuyền không kiểm soát có thể dẫn đến năng suất nổ trong khoảng thời gian mili giây đến micro giây.
        
        Mô phỏng này cung cấp giá trị giáo dục trong việc hiểu vật lý vũ khí hạt nhân trong khi tránh các chi tiết có thể hỗ trợ phát triển vũ khí thực tế.
        """,
        
        "neutron_transport": """
        ### Kết Luận Khoa Học về Vận Chuyển Neutron
        
        Mô phỏng vận chuyển neutron tiết lộ các khía cạnh quan trọng về cách neutron di chuyển và tương tác trong vật liệu phân hạch:
        
        1. **Ảnh Hưởng Phân Bố Không Gian**: Mô phỏng minh họa cách dòng neutron thay đổi theo không gian trong một hệ thống, với nồng độ cao hơn ở vùng trung tâm và giảm dần về phía biên.
        
        2. **Độ Nhạy Tiết Diện**: Kết quả cho thấy độ nhạy cao đối với thay đổi trong tiết diện (đặc biệt là phân hạch và hấp thụ), minh họa tại sao dữ liệu hạt nhân chính xác là quan trọng cho việc mô hình hóa chính xác.
        
        3. **Tác Động Hình Học**: Các hình dạng khác nhau tạo ra các mẫu phân bố neutron đặc trưng ảnh hưởng đến tính tới hạn và hành vi tổng thể của hệ thống.
        
        4. **Hiện Tượng Rò Rỉ**: Mô phỏng nắm bắt được hiện tượng rò rỉ neutron tại biên, một yếu tố quan trọng trong việc xác định liệu một hệ thống có thể duy trì phản ứng dây chuyền hay không.
        
        Những nguyên tắc này là nền tảng cho thiết kế lò phản ứng hạt nhân, an toàn tới hạn, và hiểu biết về vật lý vũ khí.
        """,
        
        "monte_carlo": """
        ### Kết Luận Khoa Học về Mô Hình Monte Carlo cho Neutron
        
        Mô phỏng Monte Carlo cung cấp hiểu biết xác suất về hành vi neutron:
        
        1. **Bản Chất Thống Kê của Phản Ứng Hạt Nhân**: Mô phỏng minh họa bản chất vốn có tính xác suất của tương tác neutron, cho thấy tại sao phương pháp thống kê là cần thiết cho việc mô hình hóa chính xác.
        
        2. **Tác Động Tiết Diện**: Kết quả cho thấy cách các tiết diện khác nhau ảnh hưởng đến hành vi quần thể neutron, bao gồm quá trình tán xạ, hấp thụ và phân hạch.
        
        3. **Phân Tích Chuỗi Phân Hạch**: Phân tích từ thế hệ này đến thế hệ khác cung cấp hình ảnh rõ ràng về các yếu tố nhân và điều kiện tới hạn.
        
        4. **Phân Bố Độ Dài Đường Đi**: Mô phỏng tiết lộ phân bố độ dài đường đi đặc trưng phụ thuộc vào thuộc tính vật liệu, quan trọng cho tính toán che chắn và tới hạn.
        
        5. **Ảnh Hưởng Kích Thước Hệ Thống**: Kết quả minh họa cách hình học hữu hạn ảnh hưởng đến xác suất thoát neutron và tính tới hạn của hệ thống.
        
        Phương pháp Monte Carlo đại diện cho tiêu chuẩn vàng trong mô hình hóa hệ thống hạt nhân khi yêu cầu độ chính xác cao.
        """,
        
        "blast_wave": """
        ### Kết Luận Khoa Học về Ảnh Hưởng Sóng Xung Kích
        
        Mô hình sóng xung kích Sedov-Taylor minh họa một số nguyên tắc vật lý quan trọng:
        
        1. **Tỷ Lệ Năng Lượng-Khoảng Cách**: Mô phỏng xác nhận rằng áp suất tăng giảm theo khoảng cách theo các quy luật tỷ lệ đã được thiết lập, với tỷ lệ ban đầu xấp xỉ tỷ lệ thuận với r^-3 và chuyển sang r^-1 đối với mặt sóng xung kích.
        
        2. **Tiến Triển Thời Gian**: Kết quả cho thấy cách sóng xung kích tiến triển và suy yếu theo thời gian, với sự giãn nở ban đầu nhanh chóng tiếp theo là sự giảm dần tốc độ lan truyền.
        
        3. **Phụ Thuộc Năng Lượng**: Mô phỏng minh họa mối quan hệ giữa năng lượng nổ và bán kính thiệt hại, xấp xỉ theo quy luật tỷ lệ căn bậc ba.
        
        4. **Ảnh Hưởng Khí Quyển**: Mô hình cho thấy mật độ môi trường ảnh hưởng đến sự lan truyền của sóng xung kích, giải thích tại sao độ cao và điều kiện thời tiết ảnh hưởng đến hiệu ứng nổ hạt nhân.
        
        5. **Tương Quan Thiệt Hại Cấu Trúc**: Mối quan hệ giữa mức áp suất tăng và thiệt hại cấu trúc được hiển thị rõ ràng, cung cấp bối cảnh để hiểu dữ liệu thử nghiệm hạt nhân lịch sử.
        
        Những nguyên tắc này giúp hiểu cả tác động của vũ khí hạt nhân và các vụ nổ thông thường lớn.
        """,
        
        "thermal_radiation": """
        ### Kết Luận Khoa Học về Ảnh Hưởng Bức Xạ Nhiệt
        
        Mô phỏng bức xạ nhiệt làm nổi bật một số hiện tượng chính:
        
        1. **Phân Bố Năng Lượng**: Khoảng 35% năng lượng nổ hạt nhân được giải phóng dưới dạng bức xạ nhiệt, tạo ra các hiệu ứng nhiệt đáng kể ở khoảng cách lớn.
        
        2. **Định Luật Nghịch Đảo Bình Phương**: Mật độ năng lượng nhiệt tuân theo định luật nghịch đảo bình phương với khoảng cách, được điều chỉnh bởi các yếu tố giảm dần của khí quyển.
        
        3. **Đặc Điểm Xung**: Xung nhiệt từ vụ nổ hạt nhân có các đặc điểm thời gian đặc trưng tùy thuộc vào năng lượng, với năng lượng lớn hơn tạo ra xung dài hơn.
        
        4. **Phản Ứng Vật Liệu**: Các vật liệu khác nhau thể hiện ngưỡng bắt cháy và hành vi cháy khác nhau khi tiếp xúc với bức xạ nhiệt, giải thích mẫu thiệt hại do cháy sau các sự kiện hạt nhân lịch sử.
        
        5. **Ảnh Hưởng Sinh Học**: Mô phỏng cho thấy cách tiếp xúc nhiệt tương quan với các mức độ bỏng khác nhau, giải thích các quan sát y tế từ các vụ nổ hạt nhân lịch sử.
        
        6. **Tác Động Khí Quyển**: Điều kiện khí quyển điều chỉnh đáng kể sự truyền bức xạ nhiệt, với điều kiện sương mù hoặc nhiều mây làm giảm hiệu ứng nhiệt.
        
        Hiểu biết về những hiệu ứng này là rất quan trọng cho cả phân tích lịch sử và lập kế hoạch phòng thủ dân sự.
        """,
        
        "emp_effects": """
        ### Kết Luận Khoa Học về Hiệu Ứng EMP
        
        Mô phỏng Xung Điện Từ (EMP) tiết lộ một số khía cạnh quan trọng của EMP hạt nhân:
        
        1. **Khuếch Đại Độ Cao**: Mô phỏng xác nhận cách các vụ nổ hạt nhân ở độ cao tạo ra hiệu ứng EMP mạnh hơn và rộng hơn đáng kể thông qua tương tác với từ trường Trái đất.
        
        2. **Đặc Điểm Phổ**: EMP hạt nhân bao gồm thành phần E1 kéo dài ngắn, E2 trung gian và E3 kéo dài hơn, mỗi thành phần ảnh hưởng đến các loại cơ sở hạ tầng khác nhau.
        
        3. **Tính Dễ Bị Tổn Thương của Công Nghệ**: Thiết bị điện tử hiện đại với vi xử lý và mạch tích hợp thể hiện tính dễ bị tổn thương cực đoan so với công nghệ đèn chân không cũ hơn, giải thích tại sao EMP là mối quan tâm lớn hơn ngày nay so với thời kỳ đầu hạt nhân.
        
        4. **Phương Pháp Bảo Vệ**: Mô phỏng chứng minh hiệu quả của lồng Faraday và các phương pháp che chắn khác trong việc giảm thiểu tác động EMP.
        
        5. **Vấn Đề Cơ Sở Hạ Tầng Quan Trọng**: Lưới điện và mạng thông tin liên lạc thể hiện tính dễ bị tổn thương đặc biệt do mạng lưới dẫn điện rộng lớn của chúng có thể hoạt động như ăng-ten cho EMP.
        
        Hiểu biết về hiệu ứng EMP là rất quan trọng cho việc bảo vệ cơ sở hạ tầng quan trọng, hoạt động quân sự và chuẩn bị cho thảm họa.
        """,
        
        "fallout": """
        ### Kết Luận Khoa Học về Mưa Phóng Xạ Hạt Nhân
        
        Mô phỏng mưa phóng xạ minh họa một số nguyên tắc chính của mưa phóng xạ hạt nhân:
        
        1. **Phụ Thuộc Độ Cao**: Vụ nổ trên mặt đất hoặc gần mặt đất tạo ra mưa phóng xạ nhiều hơn đáng kể so với vụ nổ trên không, do sự hút đất vào quả cầu lửa.
        
        2. **Tác Động Thời Tiết**: Mô hình gió ảnh hưởng mạnh đến phân bố mưa phóng xạ, tạo ra các mẫu ô nhiễm không đối xứng xuôi theo gió từ điểm nổ.
        
        3. **Đặc Điểm Phân Rã**: Định luật phân rã t^-1.2 (mối quan hệ Way-Wigner) dự đoán chính xác sự giảm bức xạ tổng thể theo thời gian, mặc dù các đồng vị cụ thể có thời gian bán rã khác nhau.
        
        4. **Hình Thành Điểm Nóng**: Mô phỏng cho thấy cách đặc điểm địa hình và điều kiện thời tiết có thể tạo ra các "điểm nóng" mưa phóng xạ tập trung xa từ điểm nổ.
        
        5. **Phân Bố Tốc Độ Liều Lượng**: Mức bức xạ từ mưa phóng xạ tuân theo các mẫu phức tạp dựa trên thời gian, khoảng cách và điều kiện thời tiết, giải thích tại sao việc giám sát mưa phóng xạ đòi hỏi mạng lưới đo lường tinh vi.
        
        6. **Hiệu Ứng Dài Hạn**: Mặc dù bức xạ mạnh nhất xảy ra trong vài ngày đầu, một số khu vực có thể vẫn bị ô nhiễm trong nhiều năm hoặc thập kỷ do các đồng vị sống lâu.
        
        Hiểu biết này rất quan trọng cho lập kế hoạch phòng thủ dân sự, quản lý sự kiện hậu hạt nhân và phân tích lịch sử.
        """,
        
        "weapon_design": """
        ### Kết Luận Khoa Học về Vật Lý Vũ Khí Hạt Nhân
        
        Mô phỏng vật lý vũ khí minh họa một số nguyên tắc cơ bản:
        
        1. **Giới Hạn Hiệu Suất**: Mô phỏng cho thấy tại sao vũ khí hạt nhân thường chỉ đạt được một phần năng suất lý thuyết của chúng, với các yếu tố thiết kế khác nhau ảnh hưởng đến hiệu suất.
        
        2. **Hiệu Ứng Tăng Cường**: Tăng cường nhiệt hạch cải thiện đáng kể hiệu suất vũ khí phân hạch mà không cần thiết kế nhiệt hạch hai giai đoạn đầy đủ.
        
        3. **Nguyên Tắc Giai Đoạn**: Thiết kế Teller-Ulam hai giai đoạn cho phép tỷ lệ năng suất vượt xa những gì có thể thực hiện được với các thiết bị phân hạch thuần túy, giải thích con đường phát triển của vũ khí nhiệt hạch.
        
        4. **Yêu Cầu Vật Liệu**: Mô phỏng cho thấy cách các thiết kế khác nhau yêu cầu số lượng và loại vật liệu hạt nhân khác nhau, giải thích những thách thức phát triển lịch sử.
        
        5. **Mối Quan Hệ Kích Thước-Năng Suất**: Mối quan hệ giữa kích thước vũ khí, khối lượng và năng suất giúp giải thích sự thu nhỏ lịch sử của vũ khí hạt nhân.
        
        Mô phỏng này cung cấp giá trị giáo dục trong việc hiểu vật lý vũ khí hạt nhân trong khi tránh các chi tiết có thể hỗ trợ phát triển vũ khí thực tế.
        """,
        
        "flash_effects": """
        ### Kết Luận Khoa Học về Hiệu Ứng Ánh Sáng Hạt Nhân
        
        Mô phỏng ánh sáng hạt nhân làm nổi bật một số hiện tượng quan trọng:
        
        1. **Quy Mô Cường Độ**: Mô phỏng minh họa cường độ chưa từng có của ánh sáng hạt nhân, sáng hơn nhiều bậc so với bất kỳ nguồn sáng tự nhiên nào, giải thích tại sao thương tích ở mắt xảy ra ở khoảng cách lớn trong các thử nghiệm lịch sử.
        
        2. **Đặc Điểm Xung**: Ánh sáng hạt nhân có đặc điểm thời gian với một đỉnh ban đầu cực kỳ sáng tiếp theo là bức xạ nhiệt kéo dài hơn.
        
        3. **Cơ Chế Tổn Thương Mắt**: Các cơ chế tổn thương mắt khác nhau (mù tạm thời do ánh sáng, bỏng võng mạc, tổn thương giác mạc) phụ thuộc vào cường độ, phân bố phổ và hướng nhìn.
        
        4. **Phụ Thuộc Khoảng Cách**: Mô phỏng cho thấy cách hiệu ứng ánh sáng tuân theo mối quan hệ nghịch đảo bình phương với khoảng cách, được điều chỉnh bởi sự giảm dần của khí quyển.
        
        5. **Yếu Tố Thời Gian Trong Ngày**: Giãn đồng tử vào ban đêm làm tăng đáng kể tính dễ bị tổn thương với hiệu ứng ánh sáng, giải thích các quan sát lịch sử về phạm vi tổn thương mắt lớn hơn vào ban đêm.
        
        Hiểu biết về những hiệu ứng này vẫn quan trọng cho phân tích lịch sử và chuẩn bị y tế.
        """
    },
    "metadata": {
        "chain_reaction": {
            "references": [
                "Glasstone, S., & Dolan, P. J. (1977). The Effects of Nuclear Weapons (3rd ed.). U.S. Department of Defense.",
                "Kessler, G. (2011). Proliferation-Proof Uranium/Plutonium Fuel Cycles. KIT Scientific Publishing.",
                "Reed, B. C. (2014). The Physics of the Manhattan Project (2nd ed.). Springer."
            ]
        },
        "blast_wave": {
            "references": [
                "Brode, H. L. (1968). Review of Nuclear Weapons Effects. Annual Review of Nuclear Science, 18(1), 153-202.",
                "Needham, C. E. (2010). Blast Waves (Shock Wave and High Pressure Phenomena). Springer.",
                "Glasstone, S., & Dolan, P. J. (1977). The Effects of Nuclear Weapons (3rd ed.). U.S. Department of Defense."
            ]
        }
    }
}

def get_conclusions(model_name, lang="en"):
    """
    Trả về kết luận khoa học cho một mô hình cụ thể
    
    Parameters:
    -----------
    model_name : str
        Tên của mô hình (ví dụ: "chain_reaction", "blast_wave", etc.)
    lang : str
        Mã ngôn ngữ ("en" hoặc "vi")
    
    Returns:
    --------
    str
        Kết luận khoa học được định dạng Markdown
    """
    if lang == "metadata":
        if model_name in conclusions["metadata"]:
            return conclusions["metadata"][model_name]
        return {}
        
    if model_name in conclusions.get(lang, {}):
        return conclusions[lang][model_name]
    
    # Nếu không tìm thấy kết luận, trả về thông báo mặc định
    default_conclusions = {
        "en": "Scientific conclusions for this model are not available yet.",
        "vi": "Các kết luận khoa học cho mô hình này chưa có sẵn."
    }
    
    return default_conclusions.get(lang, default_conclusions["en"]) 