# -*- coding: utf-8 -*-
"""▭ Hình Chữ Nhật"""

from __future__ import annotations

from typing import Dict, Tuple
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation

Point = Tuple[float, float]


@st.cache_data(ttl=3600)
def get_rectangle_data(ab: float, ad: float) -> Dict[str, object]:
    """Tính các đỉnh và đại lượng cơ bản của hình chữ nhật ABCD."""
    a: Point = (0.0, float(ad))
    b: Point = (float(ab), float(ad))
    c: Point = (float(ab), 0.0)
    d: Point = (0.0, 0.0)
    o: Point = (float(ab) / 2.0, float(ad) / 2.0)

    diagonal = math.hypot(ab, ad)
    return {
        "points": (a, b, c, d),
        "center": o,
        "area": float(ab * ad),
        "perimeter": float(2 * (ab + ad)),
        "diagonal": float(diagonal),
        "half_diagonal": float(diagonal / 2.0),
    }


@st.cache_data(ttl=3600)
def get_ai_explanation_cached(
    shape_name: str,
    properties_items: Tuple[Tuple[str, str], ...],
) -> str:
    """Cache giải thích AI để tránh gọi API lặp lại."""
    return get_ai_explanation(shape_name, dict(properties_items))


def init_session_state() -> None:
    """Khởi tạo trạng thái của trang."""
    defaults = {
        "rectangle_ab": 5,
        "rectangle_ad": 3,
        "ai_text_rectangle": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "api_key" not in st.session_state:
        try:
            st.session_state.api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            st.session_state.api_key = ""


def render_sidebar() -> None:
    """Hiển thị sidebar với cấu hình API."""
    with st.sidebar:
        st.markdown("### 🔑 API Gemini")
        api_key = st.text_input(
            "API key (tùy chọn)",
            value=str(st.session_state.api_key),
            type="password",
            help="Có thể để trống nếu chỉ dùng giải thích tĩnh.",
        )
        st.session_state.api_key = api_key.strip()


def render_drawing_section() -> Dict[str, object]:
    """Phần vẽ hình chữ nhật với slider điều khiển."""
    st.subheader("▭ Vẽ Hình Chữ Nhật")

    with st.form("rectangle_form"):
        col1, col2, col3 = st.columns([1, 1, 0.9])
        with col1:
            ab = st.slider(
                "Chiều dài AB (cm)",
                min_value=1,
                max_value=10,
                value=int(st.session_state.rectangle_ab),
            )
        with col2:
            ad = st.slider(
                "Chiều rộng AD (cm)",
                min_value=1,
                max_value=10,
                value=int(st.session_state.rectangle_ad),
            )
        with col3:
            st.write("")
            st.write("")
            redraw = st.form_submit_button("🔄 Vẽ lại", use_container_width=True)

    if redraw:
        st.session_state.rectangle_ab = ab
        st.session_state.rectangle_ad = ad
    else:
        ab = st.session_state.rectangle_ab
        ad = st.session_state.rectangle_ad

    data = get_rectangle_data(float(ab), float(ad))
    points = data["points"]

    # Vẽ hình chữ nhật
    fig, ax = plt.subplots(figsize=(6, 4))
    rect = Polygon(points, closed=True, facecolor="lightgreen", edgecolor="darkgreen", linewidth=2, alpha=0.6)
    ax.add_patch(rect)

    # Đánh dấu các đỉnh
    for i, (point, label) in enumerate(zip(points, ["A", "B", "C", "D"])):
        ax.plot(point[0], point[1], "ro", markersize=8)
        ax.text(point[0] - 0.3, point[1] + 0.2, label, fontsize=11, weight="bold", color="darkgreen")

    ax.set_xlim(-1, float(ab) + 1)
    ax.set_ylim(-1, float(ad) + 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Hình Chữ Nhật ABCD", fontsize=14, weight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("### Thông tin hình:")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.write(f"AB = {ab:.0f} cm")
        st.write(f"AD = {ad:.0f} cm")
    with info_col2:
        st.write(f"Diện tích = {data['area']:.2f} cm²")
        st.write(f"Chu vi = {data['perimeter']:.2f} cm")
        st.write(f"Đường chéo = {data['diagonal']:.2f} cm")

    return data


def render_info_section(data: Dict[str, object]) -> None:
    """Phần giải thích định nghĩa, tính chất, công thức."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(
        "Hình chữ nhật ABCD là tứ giác có bốn góc vuông (90°). "
        "Nó có hai cặp cạnh đối song song và bằng nhau."
    )

    st.markdown("#### Tính Chất")
    properties = [
        "Có bốn góc vuông (90°)",
        "Cạnh đối bằng nhau: AB = CD, AD = BC",
        "Hai đường chéo bằng nhau: AC = BD",
        "Hai đường chéo cắt nhau tại trung điểm",
        "Là trường hợp đặc biệt của hình bình hành",
    ]
    for prop in properties:
        st.write(f"🔹 {prop}")

    st.markdown("#### Công Thức")
    ab = float(st.session_state.rectangle_ab)
    ad = float(st.session_state.rectangle_ad)
    st.write(f"Diện tích: S = a × b = {ab:.0f} × {ad:.0f} = {data['area']:.2f} cm²")
    st.write(f"Chu vi: P = 2(a + b) = 2({ab:.0f} + {ad:.0f}) = {data['perimeter']:.2f} cm")
    st.write(f"Đường chéo: d = √(a² + b²) = √({ab:.0f}² + {ad:.0f}²) = {data['diagonal']:.2f} cm")

    if st.button("🤖 Giải Thích AI", use_container_width=True):
        ai_properties = {
            "định_nghĩa": "hình bình hành có bốn góc vuông",
            "cạnh_đối": "song song và bằng nhau",
            "đường_chéo": "bằng nhau",
            "AB": f"{st.session_state.rectangle_ab} cm",
            "AD": f"{st.session_state.rectangle_ad} cm",
        }

        try:
            ai_text = get_ai_explanation_cached(
                "Hình chữ nhật",
                tuple(sorted((str(k), str(v)) for k, v in ai_properties.items())),
            )
            st.session_state.ai_text_rectangle = ai_text
        except Exception:
            st.session_state.ai_text_rectangle = "Không thể gọi AI"

    if st.session_state.ai_text_rectangle:
        if st.session_state.ai_text_rectangle == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_rectangle == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_rectangle)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Hình chữ nhật là hình bình hành với tất cả các góc bằng 90°")
        st.write("- Tính đường chéo bằng định lý Pitago")
        st.write("- Kéo slider để thay đổi kích thước và quan sát sự thay đổi")


def main() -> None:
    """Hàm chính chạy toàn bộ trang."""
    init_session_state()
    render_sidebar()

    st.title("▭ Hình Chữ Nhật")
    st.caption("Khám phá tính chất và công thức tính diện tích, chu vi")

    left_col, right_col = st.columns([3, 2])

    with left_col:
        data = render_drawing_section()

    with right_col:
        render_info_section(data)


if __name__ == "__main__":
    main()
