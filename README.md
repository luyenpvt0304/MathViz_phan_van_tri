# 🎨 AI Trợ Giúp Học Tập Hình Học

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

**Repository:** https://github.com/luyenpvt0304/MathViz_phan_van_tri.git

## 🌐 Truy Cập Trực Tuyến

Bạn có thể truy cập ứng dụng trực tiếp trên **Streamlit Community Cloud** mà không cần cài đặt:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://leluyenpvt.streamlit.app)

**Link:** https://leluyenpvt.streamlit.app

> 💡 **Ưu điểm:** Truy cập ngay trên trình duyệt, không cần cài đặt Python hay bất kỳ dependency nào

## 📋 Thông Tin Dự Án

| Thông tin | Chi tiết |
|-----------|---------|
| **Tên dự án** | AI Trợ Giúp Học Tập Hình Học |
| **Trường** | Trường THCS Phan Văn Trị, Phường Hạnh Thông, Thành phố Hồ Chí Minh |
| **Giáo viên hướng dẫn** | Lê Thị Luyến |
| **Cuộc thi** | Cuộc thi Sáng tạo trẻ Quốc gia trong lĩnh vực Trí tuệ nhân tạo năm 2026 |

## 📖 Mô Tả Dự Án

**AI Trợ Giúp Học Tập Hình Học** là ứng dụng web tương tác hỗ trợ học sinh lớp 8 học hình học theo cách trực quan, hiện đại và dễ hiểu. 

Ứng dụng cho phép:
- 🎨 **Vẽ hình học trực quan** với Matplotlib, hỗ trợ các loại hình: Tứ giác, Hình thang cân, Hình bình hành, Hình chữ nhật, Hình thoi, Hình tam giác, Hình vuông
- 📊 **Tính toán tức thì** chu vi, diện tích khi thay đổi tham số
- 🤖 **Giải thích bằng AI** (Gemini API) với nội dung ngắn gọn, dễ hiểu bằng tiếng Việt
- 💾 **Giải thích tĩnh dự phòng** để sử dụng ngay cả khi chưa cấu hình API key

**Mục tiêu:** Biến lý thuyết sách giáo khoa thành trải nghiệm tương tác, giúp học sinh ghi nhớ công thức và tính chất hình học lâu hơn.

## ✨ Tính Năng Nổi Bật

- ✅ **Vẽ hình học trực quan** - Matplotlib tạo hình ảnh chất lượng cao
- ✅ **Thay đổi tham số bằng Slider** - Quan sát sự thay đổi hình dạo thời gian thực
- ✅ **Giải thích AI thông minh** - Gemini API cung cấp giải thích ngắn gọn tiếng Việt
- ✅ **Tính toán nhanh** - Tính chu vi, diện tích tự động khi thay đổi giá trị
- ✅ **Giao diện thân thiện** - Streamlit tạo trải nghiệm người dùng mượt mà
- ✅ **Hoàn toàn miễn phí** - Không cần tài khoản, không mất phí

## 🧰 Công Nghệ Sử Dụng

| Công nghệ | Mục đích |
|-----------|---------|
| **Streamlit** | Framework web ứng dụng Python |
| **Gemini API** | AI giải thích nội dung |
| **Matplotlib** | Vẽ hình học |
| **NumPy** | Tính toán toán học |
| **Plotly** | Biểu đồ tương tác |
| **Pandas** | Xử lý dữ liệu |

## 📌 Yêu Cầu Hệ Thống

- Python 3.9+
- pip (trình quản lý gói Python)
- Git (để clone repository)

## ⚙️ Cài Đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/luyenpvt0304/MathViz_phan_van_tri.git
cd MathViz_phan_van_tri
```

### Bước 2: Tạo môi trường ảo

```bash
python -m venv venv
```

### Bước 3: Kích hoạt môi trường ảo

**Trên Linux/macOS:**
```bash
source venv/bin/activate
```

**Trên Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Trên Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

### Bước 4: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Lấy Gemini API Key

Để sử dụng tính năng giải thích AI, bạn cần có Gemini API key (miễn phí):

1. Truy cập https://ai.google.dev
2. Đăng nhập bằng tài khoản Gmail
3. Chọn **"Get API Key"**
4. Tạo API key mới cho dự án
5. **Sao chép key** vào ứng dụng ở sidebar (mục "⚙️ CẤU HÌNH")

**Lưu ý:** API key sẽ được lưu trong session (không lưu trên máy chủ)

## 🚀 Hướng Dẫn Chạy Ứng Dụng

### Cách 1: Sử Dụng Trực Tuyến (Khuyên Dùng)

Truy cập trực tiếp tại: **https://leluyenpvt.streamlit.app**

✅ **Không cần cài đặt gì** - Chỉ cần trình duyệt và kết nối Internet

### Cách 2: Chạy Trên Máy Tính Cá Nhân

Nếu muốn chạy ứng dụng trên máy tính:

```bash
streamlit run streamlit_app.py
```

Ứng dụng sẽ mở tại: **http://localhost:8501**

> 💻 **Yêu cầu:** Đã hoàn thành bước Cài Đặt (xem phần trên)

## 🧑‍🎓 Cách Sử Dụng (3 Bước)

1. **Nhập API key** (tùy chọn)
   - Vào mục "⚙️ CẤU HÌNH" ở sidebar
   - Dán Gemini API key và bấm "✓ Kiểm tra kết nối API"
   - Nếu không có, ứng dụng vẫn hoạt động với giải thích tĩnh

2. **Chọn hình học**
   - Nhấp vào tab "🚀 BẮT ĐẦU HỌC"
   - Chọn loại hình muốn học (Tứ giác, Hình thang cân, Hình bình hành, v.v.)

3. **Tương tác và học**
   - Kéo slider để thay đổi kích thước/góc
   - Quan sát hình vẽ thay đổi tức thì
   - Đọc chu vi, diện tích và giải thích tự động

## 📂 Cấu Trúc Dự Án

```
MathViz_phan_van_tri/
├── streamlit_app.py          # Ứng dụng Streamlit chính
├── trang_chu.py              # Trang chủ
├── requirements.txt          # Dependencies
├── logo/                     # Logo ứng dụng
├── page_modules/             # Các module hình học
│   ├── tu_giac.py           # Tứ giác
│   ├── hinh_thang.py        # Hình thang cân
│   ├── hinh_binh_hanh.py    # Hình bình hành
│   ├── hinh_chu_nhat.py     # Hình chữ nhật
│   ├── hinh_thoi.py         # Hình thoi
│   ├── hinh_tam_giac.py     # Hình tam giác
│   └── hinh_vuong.py        # Hình vuông
└── utils/                    # Các hàm tiện ích
    ├── geometry_tools.py     # Công cụ hình học
    ├── ai_helper.py         # Tích hợp Gemini API
    └── explanations.py      # Giải thích tĩnh
```

## 🛠 Khắc Phục Sự Cố

| Vấn đề | Giải pháp |
|--------|----------|
| **Streamlit không chạy được** | Kiểm tra đã activate môi trường ảo và cài đủ dependencies |
| **Lỗi thiếu package (NumPy, Matplotlib)** | Chạy: `pip install --no-cache-dir -r requirements.txt` |
| **Gemini API không phản hồi** | Kiểm tra API key hợp lệ và kết nối Internet |
| **Slider không hoạt động** | Cập nhật Streamlit: `pip install --upgrade streamlit` |
| **Hình vẽ bị lỗi** | Kiểm tra Matplotlib được cài đúng: `pip install --upgrade matplotlib` |

## 📦 Triển Khai Trên Streamlit Community Cloud

Ứng dụng được tự động triển khai trên **Streamlit Community Cloud** từ nhánh `main` của GitHub repository.

### Cấu Hình Triển Khai

Streamlit Community Cloud sử dụng file `requirements.txt` để cài đặt dependencies:

```
streamlit>=1.28.0
google-generativeai
matplotlib
numpy
plotly
pandas
```

### Cách Triển Khai Của Bạn Lên Streamlit Cloud

1. **Fork hoặc clone repository** từ GitHub
2. **Cấu hình tại** https://share.streamlit.io/
3. **Kết nối tài khoản GitHub** của bạn
4. **Chọn repository** `MathViz_phan_van_tri`
5. **Chọn nhánh:** `main`
6. **Chọn file chính:** `streamlit_app.py`
7. Bấm **"Deploy"** - Ứng dụng sẽ live trong vài phút

### Lưu Ý Khi Triển Khai

- 🔒 **API Key:** Không bao giờ commit API key lên GitHub. Sử dụng Streamlit Secrets để quản lý
- 🔄 **Tự động cập nhật:** Mỗi lần push lên GitHub, ứng dụng sẽ tự động cập nhật
- ⚡ **Hiệu suất:** Streamlit Cloud có giới hạn tài nguyên, phù hợp cho ứng dụng nhẹ

## 📝 Hướng Dẫn Phát Triển Thêm

Để thêm hình học mới:

1. Tạo file trong thư mục `page_modules/`
2. Import các hàm từ `utils/geometry_tools.py`
3. Tạo hàm tính chu vi, diện tích
4. Vẽ hình bằng Matplotlib
5. Thêm giải thích trong `utils/explanations.py`
6. Push lên GitHub - ứng dụng trên Streamlit Cloud sẽ tự động cập nhật

## 📄 Giấy Phép

MIT License - Tự do sử dụng, sửa đổi, phân phối

## 👥 Thông Tin Tác Giả

- **Giáo viên hướng dẫn:** Lê Thị Luyến
- **Trường:** Trường THCS Phan Văn Trị
- **Địa chỉ:** Phường Hạnh Thông, Thành phố Hồ Chí Minh
- **Repository:** https://github.com/luyenpvt0304/MathViz_phan_van_tri.git

## 💬 Liên Hệ & Hỗ Trợ

- **Mở issue** trên [GitHub repository](https://github.com/luyenpvt0304/MathViz_phan_van_tri/issues)
- **Liên hệ email:** luyenpvt0304@gmail.com
- **Website trường:** https://thcsphanvantri.hcm.edu.vn/

## 🎯 Mục Tiêu Dự Án

Dự án được phát triển nhằm:
- ✅ Giúp học sinh lớp 8 hiểu rõ hơn về hình học
- ✅ Sử dụng công nghệ AI hỗ trợ giáo dục
- ✅ Tạo trải nghiệm học tập hiện đại và tương tác
- ✅ Tham gia **Cuộc thi Sáng tạo trẻ Quốc gia trong lĩnh vực Trí tuệ nhân tạo năm 2026**

---

**Made with ❤️ bởi Lê Thị Luyến và học sinh Trường THCS Phan Văn Trị**
