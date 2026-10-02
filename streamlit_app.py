"""🏠 Trang Chủ"""

from __future__ import annotations

import sys

import streamlit as st

from utils.ai_helper import test_api_connection

# Cấu hình trang theo yêu cầu đề bài.
st.set_page_config(
    page_title="Trang Chủ",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_state() -> None:
    """Khởi tạo các biến cần thiết trong session state."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "api_status" not in st.session_state:
        st.session_state.api_status = ""


def render_sidebar() -> None:
    """Hiển thị thanh bên: cấu hình, hướng dẫn và thông tin dự án."""
    with st.sidebar:
        st.header("⚙️ CẤU HÌNH")

        # Lưu API key vào session_state để các trang khác có thể dùng lại.
        api_key = st.text_input(
            "Nhập Gemini API Key (từ ai.google.dev)",
            value=st.session_state.api_key,
            type="password",
            placeholder="AIza...",
        )
        st.session_state.api_key = api_key.strip()

        if st.button("✓ Kiểm tra kết nối API", use_container_width=True):
            if not st.session_state.api_key:
                st.session_state.api_status = "❌ API lỗi"
            else:
                ok = test_api_connection(st.session_state.api_key)
                st.session_state.api_status = "✅ API sẵn sàng" if ok else "❌ API lỗi"

        if st.session_state.api_status:
            if "✅" in st.session_state.api_status:
                st.success(st.session_state.api_status)
            else:
                st.error(st.session_state.api_status)

        st.divider()
        st.header("📚 HƯỚNG DẪN")

        with st.expander("Cách lấy Gemini API key (5 bước)", expanded=False):
            st.markdown(
                "\n".join(
                    [
                        "1. Truy cập: https://ai.google.dev",
                        "2. Đăng nhập tài khoản Gmail",
                        "3. Chọn mục Get API Key",
                        "4. Tạo API key mới cho dự án",
                        "5. Sao chép key và dán vào ô cấu hình",
                    ]
                )
            )

        with st.expander("Cách sử dụng app (3 bước)", expanded=False):
            st.markdown(
                "\n".join(
                    [
                        "1. Nhập API key và bấm kiểm tra kết nối",
                        "2. Chọn hình học muốn học ở tab BẮT ĐẦU HỌC",
                        "3. Thay đổi tham số, quan sát hình vẽ và đọc giải thích",
                    ]
                )
            )

        st.divider()
        st.header("ℹ️ THÔNG TIN")
        st.write("Phiên bản: v1.0")
        st.write("Made by: Tên bạn")
        st.write("GitHub: https://tieuphungiter.github.io/AI-Geometry-Learning")
        st.caption(f"Python: {sys.version.split()[0]}")


def render_intro_tab() -> None:
    """Tab giới thiệu tổng quan dự án."""
    st.subheader("📖 GIỚI THIỆU")

    col_text, col_icon = st.columns([2, 1])
    with col_text:
        st.markdown(
            "Ứng dụng này được thiết kế để hỗ trợ học sinh lớp 8 học hình học theo cách trực quan và dễ hiểu. "
            "Bạn có thể thay đổi kích thước hình, quan sát sự thay đổi của chu vi và diện tích theo thời gian thực."
        )
        st.markdown(
            "Bên cạnh phần vẽ hình bằng Matplotlib, ứng dụng tích hợp Gemini API để tạo giải thích ngắn gọn bằng tiếng Việt. "
            "Nếu chưa có API key, bạn vẫn có thể học với phần giải thích tĩnh đã chuẩn bị sẵn."
        )
        st.markdown(
            "Mục tiêu của dự án là biến lý thuyết trong sách giáo khoa thành trải nghiệm tương tác, "
            "giúp bạn ghi nhớ công thức và tính chất hình học lâu hơn."
        )

        st.markdown("### Tính năng nổi bật")
        st.markdown("✅ Vẽ hình trực quan (Matplotlib)")
        st.markdown("✅ Giải thích AI (Gemini)")
        st.markdown("✅ Tính chu vi, diện tích")
        st.markdown("✅ Hoàn toàn miễn phí")

    with col_icon:
        st.info("🎨 Học hình học bằng trực quan + AI")
        st.markdown(
            """
            ### Biểu tượng dự án
            - 📐 Hình học trực quan
            - 🤖 Hỗ trợ AI
            - 🚀 Học nhanh hơn
            """
        )


def render_start_tab() -> None:
    """Tab điều hướng sang các trang học theo từng hình."""
    st.subheader("🚀 BẮT ĐẦU HỌC")
    st.write("Chọn hình bạn muốn học:")

    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/1_Tu_Giac.py", label="1️⃣ Tứ Giác", icon="📐")
        st.page_link("pages/2_Hinh_Thang_Can.py", label="2️⃣ Hình Thang Cân", icon="📏")
        st.page_link("pages/3_Hinh_Binh_Hanh.py", label="3️⃣ Hình Bình Hành", icon="🔷")

    with col2:
        st.page_link("pages/4_Hinh_Chu_Nhat.py", label="4️⃣ Hình Chữ Nhật", icon="⬜")
        st.page_link("pages/5_Hinh_Thoi.py", label="5️⃣ Hình Thoi", icon="💎")

    st.caption("Nếu một trang chưa được tạo, bạn hãy tạo file tương ứng trong thư mục pages.")


def render_faq_tab() -> None:
    """Tab câu hỏi thường gặp cho người dùng mới."""
    st.subheader("❓ CÂU HỎI THƯỜNG GẶP")

    with st.expander("Tôi không có Gemini API key?"):
        st.write("Không sao, app vẫn hoạt động với giải thích tĩnh")

    with st.expander("Có mất tiền không?"):
        st.write("Không, Gemini API free")

    with st.expander("Giải thích AI có chính xác không?"):
        st.write("Chỉ để hỗ trợ, không thay thế sách giáo khoa")


def render_footer() -> None:
    """Hiển thị footer cuối trang."""
    st.divider()
    st.markdown("Made with ❤️ by Tên bạn | Dự án cuộc thi AI")

    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.markdown("GitHub repo: https://github.com/your-username/ai-learning-geometry")
    with footer_col2:
        st.markdown("Blog: https://thcsphanvantri.hcm.edu.vn/")
    with footer_col3:
        st.markdown("Email: luyenpvt0304@gmail.com")


def main() -> None:
    """Hàm chạy chính của trang chủ."""
    init_session_state()
    render_sidebar()

    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image("logo/logo.jpg", use_container_width=True)
    with col_title:
        st.markdown("<div style='font-size: 120px !important; font-weight: 900 !important; margin: 0 !important; padding-top: 10px !important; line-height: 1.2 !important;'>🎨 AI Trợ Giúp Học Tập Hình Học</div>", unsafe_allow_html=True)
        st.caption("Khám phá hình học lớp 8 một cách dễ hiểu & thực tế")
        st.write("Sử dụng AI (Gemini) để giải thích tính chất hình học, trực quan hóa hình vẽ")

    tab_intro, tab_start, tab_faq = st.tabs(
        ["📖 GIỚI THIỆU", "🚀 BẮT ĐẦU HỌC", "❓ CÂU HỎI THƯỜNG GẶP"]
    )

    with tab_intro:
        render_intro_tab()

    with tab_start:
        render_start_tab()

    with tab_faq:
        render_faq_tab()

    render_footer()


if __name__ == "__main__":
    main()
