# -*- coding: utf-8 -*-
"""🏠 Trang Chủ"""

from __future__ import annotations

import sys

import streamlit as st

from utils.ai_helper import test_api_connection

# Import page modules for routing
from page_modules import tu_giac as one_tu_giac
from page_modules import hinh_thang as two_hinh_thang
from page_modules import hinh_binh_hanh as three_hinh_binh_hanh
from page_modules import hinh_chu_nhat as four_hinh_chu_nhat
from page_modules import hinh_thoi as five_hinh_thoi
from page_modules import hinh_vuong as six_hinh_vuong
from page_modules import hinh_tam_giac as seven_hinh_tam_giac
from page_modules import map as eight_map

# Cấu hình trang theo yêu cầu đề bài.
st.set_page_config(
    page_title="Trang Chủ",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS tùy chỉnh đơn giản cho giao diện responsive
st.markdown("""
<style>
    /* Title chính: áp cả cho thẻ con (span/div) bên trong h1 để không bị rule khác ghi đè */
    .main-title, .main-title * {
        font-size: 3rem !important;      /* <-- CHỈNH CỠ CHỮ TITLE Ở ĐÂY */
        line-height: 1.1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    h1 { margin: 0 !important; padding: 0 !important; line-height: 1.1 !important; }
    h2 { font-size: 1.8rem !important; margin-bottom: 0.3rem !important; }
    h3 { font-size: 1.4rem !important; margin-bottom: 0.2rem !important; }
    h4 { font-size: 1.1rem !important; }
    body { font-size: 1rem !important; }
    p { font-size: 1rem !important; }
    [data-testid="stHeading"] { margin-bottom: 0.5rem !important; }
    @media (max-width: 768px) {
        .main-title, .main-title * { font-size: 2.2rem !important; }
        h2 { font-size: 1.4rem !important; }
        h3 { font-size: 1.1rem !important; }
    }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    [data-testid="metric-container"] { padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)


def init_session_state() -> None:
    """Khởi tạo các biến cần thiết trong session state."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "api_status" not in st.session_state:
        st.session_state.api_status = ""

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    if "qa_questions" not in st.session_state:
        st.session_state.qa_questions = None

    if "qa_answers" not in st.session_state:
        st.session_state.qa_answers = {}



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
        st.write("Made by: LuyenPVT")
        st.write("GitHub: https://github.com/luyenpvt0304/MathViz_phan_van_tri")
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

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1️⃣ Tứ Giác", use_container_width=True):
            st.session_state.current_page = "tu_giac"
            st.rerun()
        if st.button("4️⃣ Hình Chữ Nhật", use_container_width=True):
            st.session_state.current_page = "hinh_chu_nhat"
            st.rerun()
        if st.button("6️⃣ Hình Vuông", use_container_width=True):
            st.session_state.current_page = "hinh_vuong"
            st.rerun()

    with col2:
        if st.button("2️⃣ Hình Thang", use_container_width=True):
            st.session_state.current_page = "hinh_thang"
            st.rerun()
        if st.button("5️⃣ Hình Thoi", use_container_width=True):
            st.session_state.current_page = "hinh_thoi"
            st.rerun()
        if st.button("📊 Sơ Đồ Tư Duy", use_container_width=True):
            st.session_state.current_page = "map"
            st.rerun()

    with col3:
        if st.button("3️⃣ Hình Bình Hành", use_container_width=True):
            st.session_state.current_page = "hinh_binh_hanh"
            st.rerun()
        if st.button("7️⃣ Hình Tam Giác", use_container_width=True):
            st.session_state.current_page = "hinh_tam_giac"
            st.rerun()
        st.write("")


def generate_qa_questions() -> str | None:
    """Tạo 5 câu hỏi trắc nghiệm ngẫu nhiên về hình học từ Gemini API."""
    from utils.ai_helper import _safe_generate

    if not st.session_state.api_key:
        return None

    prompt = """Hãy tạo 5 câu hỏi trắc nghiệm ngẫu nhiên về hình học lớp 8 (tứ giác, hình thang, hình bình hành, hình chữ nhật, hình vuông, hình thoi, tam giác).

Định dạng JSON:
{
  "questions": [
    {
      "id": 1,
      "question": "Câu hỏi?",
      "options": ["A) Đáp án 1", "B) Đáp án 2", "C) Đáp án 3", "D) Đáp án 4"],
      "correct_answer": "A",
      "explanation": "Giải thích đáp án."
    },
    ...
  ]
}

Yêu cầu:
- Mỗi câu hỏi có 4 đáp án
- Câu hỏi phải liên quan đến định nghĩa, tính chất, công thức
- Giải thích chi tiết
- Tiếng Việt
- Trả về JSON hợp lệ"""

    ai_text = _safe_generate(prompt, st.session_state.api_key)
    return ai_text


def get_default_qa_questions() -> list:
    """Trả về 5 câu hỏi trắc nghiệm mặc định khi API không khả dụng."""
    import json
    default_qa = {
        "questions": [
            {
                "id": 1,
                "question": "Tổng các góc trong của một tứ giác bằng bao nhiêu?",
                "options": ["A) 180°", "B) 270°", "C) 360°", "D) 450°"],
                "correct_answer": "C",
                "explanation": "Theo định lý, tổng các góc trong của một tứ giác luôn bằng 360°."
            },
            {
                "id": 2,
                "question": "Hình bình hành có bao nhiêu tính chất về góc?",
                "options": ["A) Hai góc đối bằng nhau", "B) Tất cả góc bằng nhau", "C) Hai góc kề bù nhau", "D) Cả A và C"],
                "correct_answer": "D",
                "explanation": "Hình bình hành có: góc đối bằng nhau (A đúng) và hai góc kề bù nhau (C đúng)."
            },
            {
                "id": 3,
                "question": "Hình chữ nhật khác hình vuông ở điểm nào?",
                "options": ["A) Hình chữ nhật có 4 góc vuông", "B) Hình chữ nhật có cạnh không bằng nhau", "C) Hình vuông là hình chữ nhật đặc biệt", "D) Hình chữ nhật có 2 đường chéo"],
                "correct_answer": "B",
                "explanation": "Hình chữ nhật có chiều dài ≠ chiều rộng, trong khi hình vuông có 4 cạnh bằng nhau."
            },
            {
                "id": 4,
                "question": "Đường chéo của hình thoi có tính chất gì?",
                "options": ["A) Song song với nhau", "B) Vuông góc với nhau", "C) Bằng nhau", "D) Song song và bằng nhau"],
                "correct_answer": "B",
                "explanation": "Hai đường chéo của hình thoi vuông góc với nhau và cắt nhau tại trung điểm."
            },
            {
                "id": 5,
                "question": "Hình thang cân có tính chất nào dưới đây?",
                "options": ["A) Hai đáy bằng nhau", "B) Hai cạnh bên bằng nhau", "C) Tất cả cạnh bằng nhau", "D) Hai đường chéo không bằng nhau"],
                "correct_answer": "B",
                "explanation": "Hình thang cân có hai cạnh bên bằng nhau, hai đáy song song nhưng không bằng nhau."
            }
        ]
    }
    return default_qa["questions"]


def render_qa_tab() -> None:
    """Tab hệ thống Q&A với câu hỏi ngẫu nhiên được tạo bởi AI."""
    st.subheader("🎯 HỆ THỐNG Q&A")
    st.write("Kiểm tra kiến thức hình học của bạn với các câu hỏi trắc nghiệm do AI tạo")

    col_button1, col_button2 = st.columns(2)
    with col_button1:
        if st.button("🔄 Tạo bộ câu hỏi mới", use_container_width=True):
            if not st.session_state.api_key:
                st.warning("⚠️ Cần cấu hình API key trong mục CẤU HÌNH để sử dụng tính năng này")
            else:
                with st.spinner("Đang tạo câu hỏi từ AI (có thể mất vài giây)..."):
                    qa_json = generate_qa_questions()
                    if qa_json:
                        try:
                            import json
                            # Xóa markdown formatting nếu có
                            qa_json_clean = qa_json.replace("```json", "").replace("```", "").strip()
                            qa_data = json.loads(qa_json_clean)
                            st.session_state.qa_questions = qa_data.get("questions", [])
                            st.session_state.qa_answers = {}
                            st.session_state.show_results = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Lỗi khi xử lý câu hỏi: {str(e)[:100]}\n\nVui lòng thử lại.")
                    else:
                        st.error(
                            "❌ **API đang bận hoặc không khả dụng**\n\n"
                            "Gemini API đang trải qua tải cao. Bạn có thể:\n"
                            "- Thử lại sau vài phút\n"
                            "- Hoặc sử dụng bộ câu hỏi có sẵn"
                        )
                        col_retry1, col_retry2 = st.columns(2)
                        with col_retry1:
                            if st.button("🔁 Thử lại", use_container_width=True):
                                st.rerun()
                        with col_retry2:
                            if st.button("📝 Dùng câu hỏi có sẵn", use_container_width=True):
                                st.session_state.qa_questions = get_default_qa_questions()
                                st.session_state.qa_answers = {}
                                st.session_state.show_results = False
                                st.rerun()

    with col_button2:
        if st.button("✅ Kiểm tra đáp án", use_container_width=True, disabled=not st.session_state.qa_questions):
            if st.session_state.qa_questions:
                st.session_state.show_results = True
                st.rerun()

    if st.session_state.qa_questions:
        st.divider()
        if "show_results" not in st.session_state:
            st.session_state.show_results = False

        for q in st.session_state.qa_questions:
            st.markdown(f"### Câu {q['id']}: {q['question']}")

            selected = st.radio(
                "Chọn đáp án:",
                options=q["options"],
                key=f"q_{q['id']}",
                label_visibility="collapsed"
            )

            if selected:
                st.session_state.qa_answers[q["id"]] = selected[0]

            if st.session_state.show_results:
                correct = f"{q['correct_answer']})"
                is_correct = selected and selected.startswith(q['correct_answer'])

                if is_correct:
                    st.success(f"✅ Đúng! {q['explanation']}")
                else:
                    st.error(f"❌ Sai! Đáp án đúng là: {correct}\n\n{q['explanation']}")

            st.divider()

        if st.session_state.show_results:
            correct_count = sum(
                1 for q in st.session_state.qa_questions
                if st.session_state.qa_answers.get(q["id"], "").startswith(q["correct_answer"])
            )
            st.metric("Kết quả", f"{correct_count}/5 câu đúng")


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
    st.markdown("Made with ❤️ by LuyenPVT | Dự án cuộc thi AI")

    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.markdown("GitHub repo: https://github.com/luyenpvt0304/MathViz_phan_van_tri")
    with footer_col2:
        st.markdown("Blog: https://thcsphanvantri.hcm.edu.vn/")
    with footer_col3:
        st.markdown("Email: luyenpvt0304@gmail.com")


def main() -> None:
    """Hàm chạy chính của trang chủ."""
    init_session_state()

    if st.session_state.current_page == "home":
        render_sidebar()

        col_logo, col_title = st.columns([1, 4], gap="small")
        with col_logo:
            st.image("logo/logo.jpg", width=160)
        with col_title:
            st.markdown("<h1 class='main-title' style='font-weight: 500 !important; color: #ff4444; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>🎨 AI Trợ Giúp Học Tập Hình Học</h1>", unsafe_allow_html=True)
            st.caption("Khám phá hình học lớp 8 một cách dễ hiểu & thực tế")
            st.markdown("Sử dụng AI (Gemini) để giải thích tính chất hình học, trực quan hóa hình vẽ")

        tab_intro, tab_start, tab_qa, tab_faq = st.tabs(
            ["📖 GIỚI THIỆU", "🚀 BẮT ĐẦU HỌC", "🎯 Q&A", "❓ CÂU HỎI THƯỜNG GẶP"]
        )

        with tab_intro:
            render_intro_tab()

        with tab_start:
            render_start_tab()

        with tab_qa:
            render_qa_tab()

        with tab_faq:
            render_faq_tab()

        render_footer()

    elif st.session_state.current_page == "tu_giac":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        one_tu_giac.main()

    elif st.session_state.current_page == "hinh_thang":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        two_hinh_thang.main()

    elif st.session_state.current_page == "hinh_binh_hanh":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        three_hinh_binh_hanh.main()

    elif st.session_state.current_page == "hinh_chu_nhat":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        four_hinh_chu_nhat.main()

    elif st.session_state.current_page == "hinh_thoi":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        five_hinh_thoi.main()

    elif st.session_state.current_page == "hinh_vuong":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        six_hinh_vuong.main()

    elif st.session_state.current_page == "hinh_tam_giac":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        seven_hinh_tam_giac.main()

    elif st.session_state.current_page == "map":
        if st.button("← Quay lại Trang Chủ"):
            st.session_state.current_page = "home"
            st.rerun()
        eight_map.main()


if __name__ == "__main__":
    main()
