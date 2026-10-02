# -*- coding: utf-8 -*-
"""■ Hình Vuông"""

from __future__ import annotations

from typing import Dict, Tuple
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as RectPatch
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation

Point = Tuple[float, float]


@st.cache_data(ttl=3600)
def get_square_data(side: float) -> Dict[str, float]:
    """Tính các đại lượng cơ bản của hình vuông."""
    side = float(side)
    diagonal = side * math.sqrt(2)
    area = side * side
    perimeter = 4 * side

    return {
        "side": float(side),
        "diagonal": float(diagonal),
        "area": float(area),
        "perimeter": float(perimeter),
    }


def init_session_state() -> None:
    """Khởi tạo trạng thái của trang."""
    defaults = {
        "square_side": 4,
        "ai_text_square": "",
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


def render_drawing_section() -> Dict[str, float]:
    """Phần vẽ hình vuông với slider điều khiển."""
    st.subheader("■ Vẽ Hình Vuông")

    with st.form("square_form"):
        col1, col2 = st.columns([1, 0.9])
        with col1:
            side = st.slider(
                "Cạnh (cm)",
                min_value=1,
                max_value=10,
                value=int(st.session_state.square_side),
            )
        with col2:
            st.write("")
            st.write("")
            redraw = st.form_submit_button("🔄 Vẽ lại", use_container_width=True)

    if redraw:
        st.session_state.square_side = side
    else:
        side = st.session_state.square_side

    data = get_square_data(float(side))

    # Vẽ hình vuông
    fig, ax = plt.subplots(figsize=(6, 4))
    square = RectPatch((0, 0), side, side, facecolor="lightsteelblue", edgecolor="darkblue", linewidth=2, alpha=0.6)
    ax.add_patch(square)

    # Đánh dấu các đỉnh
    points = [(0, 0), (side, 0), (side, side), (0, side)]
    labels = ["A", "B", "C", "D"]
    for point, label in zip(points, labels):
        ax.plot(point[0], point[1], "ro", markersize=8)
        offset = -0.4 if label in ["A", "B"] else 0.2
        ax.text(point[0] - 0.3, point[1] + offset, label, fontsize=11, weight="bold", color="darkblue")

    # Vẽ đường chéo
    ax.plot([0, side], [0, side], "b--", linewidth=1, alpha=0.5)
    ax.plot([side, 0], [0, side], "b--", linewidth=1, alpha=0.5)

    ax.set_xlim(-1, side + 1)
    ax.set_ylim(-1, side + 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Hình Vuông ABCD", fontsize=14, weight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("### Thông tin hình:")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.write(f"Cạnh = {side:.1f} cm")
        st.write(f"Diện tích = {data['area']:.2f} cm²")
    with info_col2:
        st.write(f"Chu vi = {data['perimeter']:.2f} cm")
        st.write(f"Đường chéo = {data['diagonal']:.2f} cm")

    return data


def render_info_section(data: Dict[str, float]) -> None:
    """Phần giải thích định nghĩa, tính chất, công thức."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(
        "Hình vuông là tứ giác có bốn góc vuông và bốn cạnh bằng nhau."
        "Nó cũng là hình thoi có bốn góc vuông."
    )

    st.markdown("#### Tính Chất")
    properties = [
        "Bốn cạnh bằng nhau",
        "Bốn góc vuông (90°)",
        "Hai đường chéo bằng nhau",
        "Hai đường chéo vuông góc với nhau",
        "Hai đường chéo cắt nhau tại trung điểm của mỗi đường",
        "Là trường hợp đặc biệt của cả hình chữ nhật và hình thoi",
    ]
    for prop in properties:
        st.write(f"🔹 {prop}")

    st.markdown("#### Công Thức")
    side = float(st.session_state.square_side)
    st.write(f"Diện tích: S = a² = {side:.0f}² = {data['area']:.2f} cm²")
    st.write(f"Chu vi: P = 4a = 4 × {side:.0f} = {data['perimeter']:.2f} cm")
    st.write(f"Đường chéo: d = a√2 = {side:.0f}√2 = {data['diagonal']:.2f} cm")

    if st.button("🤖 Giải Thích AI", use_container_width=True):
        ai_properties = {
            "định_nghĩa": "hình chữ nhật có bốn cạnh bằng nhau",
            "đặc_điểm": "bốn góc vuông, hai đường chéo vuông góc",
            "cạnh": f"{st.session_state.square_side} cm",
            "diện_tích": f"{data['area']:.2f} cm²",
        }

        try:
            ai_text = get_ai_explanation(
                "Hình vuông",
                ai_properties
            )
            st.session_state.ai_text_square = ai_text
        except Exception:
            st.session_state.ai_text_square = "Không thể gọi AI"

    if st.session_state.ai_text_square:
        if st.session_state.ai_text_square == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_square == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_square)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Hình vuông là hình chữ nhật có tất cả các cạnh bằng nhau")
        st.write("- Hình vuông cũng là hình thoi có bốn góc vuông")
        st.write("- Hai đường chéo của hình vuông chia nó thành 4 tam giác đều")


def main() -> None:
    """Hàm chính chạy toàn bộ trang."""
    init_session_state()
    render_sidebar()

    st.title("■ Hình Vuông")
    st.caption("Khám phá tính chất và công thức tính diện tích hình vuông")

    left_col, right_col = st.columns([3, 2])

    with left_col:
        data = render_drawing_section()

    with right_col:
        render_info_section(data)


if __name__ == "__main__":
    main()
