# -*- coding: utf-8 -*-
"""📐 Tứ Giác"""

from __future__ import annotations

from typing import Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation
from utils.explanations import get_definition, get_properties

Point = Tuple[float, float]


def init_session_state() -> None:
    """Khởi tạo session state cho trang học tứ giác."""
    if "quadrilateral_type" not in st.session_state:
        st.session_state.quadrilateral_type = "convex"

    if "api_key" not in st.session_state:
        try:
            st.session_state.api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            st.session_state.api_key = ""

    if "ai_text_quadrilateral" not in st.session_state:
        st.session_state.ai_text_quadrilateral = ""


def render_sidebar_key_input() -> None:
    """Cho phép nhập API key ở sidebar."""
    with st.sidebar:
        st.markdown("### 🔑 API Gemini")
        api_key = st.text_input(
            "API key (tùy chọn)",
            value=str(st.session_state.api_key),
            type="password",
            help="Có thể để trống nếu chỉ dùng giải thích tĩnh.",
        )
        st.session_state.api_key = api_key.strip()


def draw_convex_quadrilateral() -> None:
    """Vẽ tứ giác lồi ABCD."""
    fig, ax = plt.subplots(figsize=(6, 4))

    points = np.array([[1, 1], [5, 0.5], [5.5, 3], [1.5, 3.5]])
    polygon = patches.Polygon(points, closed=True, fill=True, facecolor="lightblue",
                             edgecolor="darkblue", linewidth=2, alpha=0.6)
    ax.add_patch(polygon)

    labels = ["A", "B", "C", "D"]
    for i, (point, label) in enumerate(zip(points, labels)):
        ax.plot(point[0], point[1], "ro", markersize=8)
        offset = 0.3
        ax.text(point[0] - offset, point[1] - offset, label, fontsize=12, weight="bold", color="darkred")

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Tứ Giác Lồi ABCD", fontsize=14, weight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def draw_concave_quadrilateral() -> None:
    """Vẽ tứ giác lõm MNPQ."""
    fig, ax = plt.subplots(figsize=(6, 4))

    points = np.array([[1, 2], [3, 0.5], [2.5, 2.5], [3.5, 3]])
    polygon = patches.Polygon(points, closed=True, fill=True, facecolor="magenta",
                             edgecolor="purple", linewidth=2, alpha=0.6)
    ax.add_patch(polygon)

    labels = ["M", "N", "P", "Q"]
    for i, (point, label) in enumerate(zip(points, labels)):
        ax.plot(point[0], point[1], "ro", markersize=8)
        offset = 0.25
        ax.text(point[0] - offset, point[1] - offset, label, fontsize=12, weight="bold", color="purple")

    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.5, 4)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Tứ Giác Lõm MNPQ", fontsize=14, weight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_left_column() -> None:
    """Cột trái: vẽ các loại tứ giác."""
    st.subheader("▭ Các Loại Tứ Giác")

    quad_type = st.radio(
        "Chọn loại tứ giác:",
        options=["convex", "concave"],
        format_func=lambda x: "Tứ Giác Lồi" if x == "convex" else "Tứ Giác Lõm",
        horizontal=True
    )
    st.session_state.quadrilateral_type = quad_type

    if quad_type == "convex":
        draw_convex_quadrilateral()
        st.markdown("### Thông tin hình:")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.write("✓ Tứ giác lồi")
            st.write("✓ Tất cả góc < 180°")
        with info_col2:
            st.write("✓ Luôn nằm trong nửa mặt phẳng")
            st.write("✓ Tổng 4 góc = 360°")
    else:
        draw_concave_quadrilateral()
        st.markdown("### Thông tin hình:")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.write("✓ Tứ giác lõm")
            st.write("✓ Có 1 góc > 180°")
        with info_col2:
            st.write("✓ Không luôn nằm trong nửa mặt phẳng")
            st.write("✓ Tổng 4 góc = 360°")


def render_right_column() -> None:
    """Cột phải: Định nghĩa, tính chất, và thông tin."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa Tứ Giác")
    st.info(
        "Tứ giác ABCD là hình gồm bốn đoạn thẳng AB, BC, CD, DA, "
        "trong đó không có hai đoạn thẳng nào nằm trên cùng một đường thẳng."
    )

    st.markdown("#### Phân Loại")
    with st.expander("🔹 Tứ Giác Lồi", expanded=True):
        st.write(
            "Tứ giác lồi là tứ giác luôn nằm trong một nửa mặt phẳng có bờ là "
            "đường thẳng chứa bất kỳ cạnh nào của tứ giác."
        )

    with st.expander("🔹 Tứ Giác Lõm", expanded=False):
        st.write(
            "Tứ giác lõm là tứ giác không thỏa điều kiện của tứ giác lồi, "
            "tức là có ít nhất một góc lớn hơn 180°."
        )

    st.markdown("#### Tính Chất")
    st.write("🔸 **Định lý:** Tổng các góc trong của một tứ giác bằng **360°**")
    st.write("🔸 Góc kề bù với một góc của tứ giác gọi là **góc ngoài**")
    st.write("🔸 Tổng các góc ngoài của một tứ giác bằng **360°**")

    if st.button("🤖 Giải Thích AI", use_container_width=True):
        ai_properties = {
            "định_nghĩa": "bốn đoạn thẳng nối 4 điểm phân biệt",
            "loại_lồi": "luôn nằm trong nửa mặt phẳng",
            "loại_lõm": "có góc lớn hơn 180°",
            "tổng_góc": "360°",
        }

        try:
            ai_text = get_ai_explanation(
                "Tứ giác",
                ai_properties
            )
            st.session_state.ai_text_quadrilateral = ai_text
        except Exception:
            st.session_state.ai_text_quadrilateral = "Không thể gọi AI"

    if st.session_state.ai_text_quadrilateral:
        if st.session_state.ai_text_quadrilateral == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_quadrilateral == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_quadrilateral)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Vẽ một tứ giác bất kỳ và đo các góc để kiểm chứng định lý")
        st.write("- Phân biệt tứ giác lồi và lõm bằng cách nhìn hình")
        st.write("- Tứ giác lồi là trường hợp đặc biệt của tứ giác nói chung")


def main() -> None:
    """Hàm chính chạy toàn bộ trang học tứ giác."""
    init_session_state()
    render_sidebar_key_input()

    st.title("📐 Tứ Giác")
    st.caption("Khám phá định nghĩa, phân loại và tính chất của tứ giác")

    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_left_column()

    with right_col:
        render_right_column()


if __name__ == "__main__":
    main()
