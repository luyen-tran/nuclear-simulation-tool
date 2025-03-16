import streamlit as st
from ui.dashboard import run_dashboard
import sys
import os

# Đảm bảo dark mode được áp dụng ngay từ đầu
if len(sys.argv) > 1 and sys.argv[1] == "run":
    # Đây là lần chạy đầu tiên, kiểm tra tham số URL theme
    # Streamlit không cho phép thiết lập theme trước khi chạy, 
    # nhưng bằng cách này chúng ta có thể chuẩn bị một số thứ
    os.environ["STREAMLIT_THEME"] = "custom"

if __name__ == "__main__":
    run_dashboard()