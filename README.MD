# 🚀 Công Cụ Mô Phỏng Nguyên Tử / Nuclear Simulation Tool

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-blue.svg" alt="Phiên bản"/>
  <img src="https://img.shields.io/badge/Python-3.7+-green.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="Giấy phép"/>
</p>

## 📋 Mục lục
- [Tổng Quan / Overview](#tổng-quan--overview)
- [Tính Năng Chính / Key Features](#tính-năng-chính--key-features)
- [Cài Đặt / Installation](#cài-đặt--installation)
- [Cách Sử Dụng / Usage](#cách-sử-dụng--usage)
- [Cấu Trúc Dự Án / Project Structure](#cấu-trúc-dự-án--project-structure)
- [Yêu Cầu Hệ Thống / System Requirements](#yêu-cầu-hệ-thống--system-requirements)
- [Liên Hệ / Contact](#liên-hệ--contact)

## 🔍 Tổng Quan / Overview

### 🇻🇳 Tiếng Việt
Công cụ mô phỏng hạt nhân là một ứng dụng web tương tác được xây dựng bằng Streamlit / Python để mô phỏng và trực quan hóa các hiện tượng vật lý liên quan đến năng lượng hạt nhân. Dự án nhằm mục đích giáo dục, cung cấp mô phỏng trực quan về phản ứng dây chuyền, sóng xung kích, bức xạ nhiệt, mưa phóng xạ và các hiệu ứng EMP.

### 🇬🇧 English
The Nuclear Simulation Tool is an interactive web application built with Streamlit / Python to simulate and visualize physical phenomena related to nuclear energy. The project aims for educational purposes, providing visual simulations of chain reactions, blast waves, thermal radiation, fallout, and EMP effects.

---

## ✨ Tính Năng Chính / Key Features

### 🇻🇳 Tiếng Việt
- 💥 Mô phỏng phản ứng dây chuyền hạt nhân
- 🌊 Phân tích sóng xung kích từ vụ nổ hạt nhân
- 🔥 Mô phỏng bức xạ nhiệt và tác động
- ☢️ Mô hình hóa và phân tích mưa phóng xạ
- ⚡ Mô phỏng hiệu ứng xung điện từ (EMP)
- 🎲 Mô phỏng Monte Carlo cho vận chuyển neutron
- 🌐 Hỗ trợ đa ngôn ngữ
- 🌓 Giao diện thân thiện với chế độ sáng/tối

### 🇬🇧 English
- 💥 Nuclear chain reaction simulation
- 🌊 Nuclear blast wave analysis
- 🔥 Thermal radiation simulation and effects
- ☢️ Fallout modeling and analysis
- ⚡ Electromagnetic pulse (EMP) effect simulation
- 🎲 Monte Carlo simulation for neutron transport
- 🌐 Multi-language support
- 🌓 User-friendly interface with light/dark modes

---

## 💻 Cài Đặt / Installation

### 🇻🇳 Tiếng Việt
```bash
# Clone repo
git clone https://github.com/luyen-tran/nuclear-simulation-tool.git
cd nuclear-simulation-tool

# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
## Windows
venv\Scripts\activate
## macOS/Linux
source venv/bin/activate

# Cài đặt các gói phụ thuộc
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run main.py
```

### 🇬🇧 English
```bash
# Clone the repository
git clone https://github.com/luyen-tran/nuclear-simulation-tool.git
cd nuclear-simulation-tool

# Create virtual environment
python -m venv venv

# Activate virtual environment
## Windows
venv\Scripts\activate
## macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

---

## 📝 Cách Sử Dụng / Usage

### 🇻🇳 Tiếng Việt
Sau khi khởi chạy ứng dụng, bạn có thể chọn các mô-đun mô phỏng khác nhau từ menu bên trái. Mỗi mô-đun cho phép bạn điều chỉnh các tham số đầu vào và chạy mô phỏng để xem kết quả.

**Ví dụ để mô phỏng phản ứng dây chuyền:**
1. Chọn "Phản ứng dây chuyền" từ thanh điều hướng
2. Điều chỉnh các tham số như độ giàu, hình dạng, khối lượng
3. Nhấn nút "Chạy mô phỏng" để xem kết quả

### 🇬🇧 English
After launching the application, you can select different simulation modules from the left menu. Each module allows you to adjust input parameters and run simulations to view results.

**Example to simulate a chain reaction:**
1. Select "Chain Reaction" from the navigation bar
2. Adjust parameters like enrichment, geometry, mass
3. Click the "Run Simulation" button to view results

---

## 📁 Cấu Trúc Dự Án / Project Structure
```
    ├── main.py # Điểm vào ứng dụng / Main entry point
    ├── requirements.txt # Các phụ thuộc / Dependencies
    ├── models/ # Các mô hình toán học / Mathematical models
    │   ├── blast_wave.py # Mô hình sóng xung kích / Blast wave model
    │   ├── chain_reaction.py # Mô hình phản ứng dây chuyền / Chain reaction model
    │   ├── emp_effects.py # Mô hình hiệu ứng EMP / EMP effects model
    │   ├── fallout.py # Mô hình mưa phóng xạ / Fallout model
    │   ├── monte_carlo.py # Mô phỏng Monte Carlo / Monte Carlo simulation
    │   ├── neutron_transport.py # Vận chuyển neutron / Neutron transport
    │   └── thermal_radiation.py # Bức xạ nhiệt / Thermal radiation
    └── ui/ # Giao diện người dùng / User interface
        ├── components/ # Các thành phần UI / UI components
        ├── pages/ # Các trang / Pages
        ├── conclusions.py # Kết luận khoa học / Scientific conclusions
        ├── dashboard.py # Bảng điều khiển chính / Main dashboard
        ├── theme_manager.py # Quản lý giao diện / Theme manager
        └── translator.py # Hệ thống đa ngôn ngữ / Translator system
```

---

## 🔧 Yêu Cầu Hệ Thống / System Requirements

### 🇻🇳 Tiếng Việt
- Python 3.7+
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Matplotlib >= 3.5.0
- Pandas >= 1.3.0
- Streamlit >= 1.10.0
- Plotly >= 5.7.0
- Các gói phụ thuộc khác được liệt kê trong requirements.txt

### 🇬🇧 English
- Python 3.7+
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Matplotlib >= 3.5.0
- Pandas >= 1.3.0
- Streamlit >= 1.10.0
- Plotly >= 5.7.0
- Other dependencies listed in requirements.txt

---

## 📞 Liên Hệ / Contact

### 🇻🇳 Tiếng Việt
- Luyện Trần - [@luyen-tran](https://github.com/luyen-tran) - minhluyen.tran0702@gmail.com
- Link dự án: [https://github.com/luyen-tran/nuclear-simulation-tool](https://github.com/luyen-tran/nuclear-simulation-tool)

### 🇬🇧 English
- Luyen Tran - [@luyen-tran](https://github.com/luyen-tran) - minhluyen.tran0702@gmail.com
- Project Link: [https://github.com/luyen-tran/nuclear-simulation-tool](https://github.com/luyen-tran/nuclear-simulation-tool)
