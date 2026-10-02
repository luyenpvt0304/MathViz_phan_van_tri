# -*- coding: utf-8 -*-
"""◊ Hình Thoi"""

from __future__ import annotations

from typing import Dict, Tuple
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation

Point = Tuple[float, float]


@st.cache_data(ttl=3600)
def get_rhombus_data(side: float, angle_deg: float) -> Dict[str, float]:
    """Tính các đỉnh và đại lượng cơ bản của hình thoi."""
    angle_rad = float(np.deg2rad(angle_deg))
    side = float(side)

    a: Point = (0.0, 0.0)
    b: Point = (side, 0.0)
    d: Point = (side * np.cos(angle_rad), side * np.sin(angle_rad))
    c: Point = (b[0] + d[0], b[1] + d[1])

    area = side * side * np.sin(angle_rad)
    perimeter = 4 * side

    return {
        "points": (a, b, c, d),
        "area": float(area),
        "perimeter": float(perimeter),
        "side": float(side),
        "angle": float(angle_deg),
    }


def init_session_state() -> None:
    """Khởi tạo trạng thái của trang."""
    defaults = {
        "rhombus_side": 4,
        "rhombus_angle": 60,
        "ai_text_rhombus": "",
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
    """Phần vẽ hình thoi với slider điều khiển."""
    st.subheader("◊ Vẽ Hình Thoi")

    with st.form("rhombus_form"):
        col1, col2, col3 = st.columns([1, 1, 0.9])
        with col1:
            side = st.slider(
                "Cạnh (cm)",
                min_value=1,
                max_value=8,
                value=int(st.session_state.rhombus_side),
            )
        with col2:
            angle = st.slider(
                "Góc A (°)",
                min_value=30,
                max_value=150,
                value=int(st.session_state.rhombus_angle),
            )
        with col3:
            st.write("")
            st.write("")
            redraw = st.form_submit_button("🔄 Vẽ lại", use_container_width=True)

    if redraw:
        st.session_state.rhombus_side = side
        st.session_state.rhombus_angle = angle
    else:
        side = st.session_state.rhombus_side
        angle = st.session_state.rhombus_angle

    data = get_rhombus_data(float(side), float(angle))
    points = data["points"]

    # Vẽ hình thoi
    fig, ax = plt.subplots(figsize=(6, 5))
    rhombus = Polygon(points, closed=True, facecolor="lightcoral", edgecolor="darkred", linewidth=2, alpha=0.6)
    ax.add_patch(rhombus)

    # Đánh dấu các đỉnh
    labels = ["A", "B", "C", "D"]
    for point, label in zip(points, labels):
        ax.plot(point[0], point[1], "ro", markersize=8)
        ax.text(point[0] - 0.3, point[1] - 0.3, label, fontsize=11, weight="bold", color="darkred")

    # Vẽ đường chéo
    ax.plot([points[0][0], points[2][0]], [points[0][1], points[2][1]], "b--", linewidth=1, alpha=0.5)
    ax.plot([points[1][0], points[3][0]], [points[1][1], points[3][1]], "b--", linewidth=1, alpha=0.5)

    ax.set_xlim(-2, 7)
    ax.set_ylim(-2, 7)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Hình Thoi ABCD", fontsize=14, weight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("### Thông tin hình:")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.write(f"Cạnh = {side:.1f} cm")
        st.write(f"Góc A = {angle:.0f}°")
    with info_col2:
        st.write(f"Diện tích = {data['area']:.2f} cm²")
        st.write(f"Chu vi = {data['perimeter']:.2f} cm")

    return data


def render_info_section(data: Dict[str, float]) -> None:
    """Phần giải thích định nghĩa, tính chất, công thức."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(
        "Hình thoi là hình bình hành có bốn cạnh bằng nhau. "
        "Nó cũng là một tứ giác có tất cả các cạnh bằng nhau."
    )

    st.markdown("#### Tính Chất")
    properties = [
        "Bốn cạnh bằng nhau",
        "Cạnh đối song song",
        "Góc đối bằng nhau",
        "Hai đường chéo vuông góc với nhau",
        "Hai đường chéo cắt nhau tại trung điểm",
        "Đường chéo chia hình thoi thành 4 tam giác bằng nhau",
    ]
    for prop in properties:
        st.write(f"🔹 {prop}")

    st.markdown("#### Công Thức")
    side = float(st.session_state.rhombus_side)
    st.write(f"Diện tích: S = a² × sin(A) = {side:.0f}² × sin({st.session_state.rhombus_angle}°) = {data['area']:.2f} cm²")
    st.write(f"Chu vi: P = 4a = 4 × {side:.0f} = {data['perimeter']:.2f} cm")

    if st.button("🤖 Giải Thích AI", use_container_width=True):
        ai_properties = {
            "định_nghĩa": "hình bình hành có bốn cạnh bằng nhau",
            "đường_chéo": "vuông góc với nhau tại trung điểm",
            "cạnh": f"{st.session_state.rhombus_side} cm",
            "góc": f"{st.session_state.rhombus_angle}°",
        }

        try:
            ai_text = get_ai_explanation(
                "Hình thoi",
                ai_properties
            )
            st.session_state.ai_text_rhombus = ai_text
        except Exception:
            st.session_state.ai_text_rhombus = "Không thể gọi AI"

    if st.session_state.ai_text_rhombus:
        if st.session_state.ai_text_rhombus == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_rhombus == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_rhombus)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Hình thoi là hình bình hành có tất cả các cạnh bằng nhau")
        st.write("- Hai đường chéo vuông góc chia hình thoi thành 4 tam giác đều")
        st.write("- Kéo slider để thay đổi kích thước và góc")


def main() -> None:
    """Hàm chính chạy toàn bộ trang."""
    init_session_state()
    render_sidebar()

    st.title("◊ Hình Thoi")
    st.caption("Khám phá tính chất và công thức tính diện tích hình thoi")

    left_col, right_col = st.columns([3, 2])

    with left_col:
        data = render_drawing_section()

    with right_col:
        render_info_section(data)


if __name__ == "__main__":
    main()
