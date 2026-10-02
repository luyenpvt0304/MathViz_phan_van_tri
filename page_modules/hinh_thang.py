# -*- coding: utf-8 -*-
"""• Hình Thang - Hình Thang Tổng Quát & Hình Thang Cân"""

from __future__ import annotations

from typing import Dict, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation

Point = Tuple[float, float]


@st.cache_data(ttl=3600)
def get_trapezoid_data(base_long: float, base_short: float, leg_left: float, height: float, fixed_leg: str = "left") -> Dict:
    """
    Tính toán hình thang tổng quát từ các tham số.

    Hình thang ABCD với:
    - AB là đáy lớn (ngang dưới)
    - CD là đáy bé (ngang trên)
    - AD, BC là hai cạnh bên
    - fixed_leg: "left" hoặc "right" - cạnh nào được cố định
    """

    base_long = float(base_long)
    base_short = float(base_short)
    leg_left = float(leg_left)
    height = float(height)

    # Kiểm tra điều kiện
    if base_short >= base_long:
        base_short = base_long * 0.6

    if height <= 0:
        height = 2.0

    # Tọa độ các đỉnh
    a: Point = (0.0, 0.0)
    b: Point = (base_long, 0.0)

    # Tính toán offset dựa trên cạnh cố định
    if fixed_leg == "left":
        # leg_left cố định, tính leg_right
        offset_left = np.sqrt(max(0, leg_left**2 - height**2))
        offset_left = min(offset_left, (base_long - base_short) * 0.8)
    else:
        # leg_left là tham số input cho "cạnh phải", tính leg_left thực tế
        offset_right = np.sqrt(max(0, leg_left**2 - height**2))
        offset_right = min(offset_right, (base_long - base_short) * 0.8)
        offset_left = base_long - base_short - offset_right

    d: Point = (offset_left, height)
    c: Point = (offset_left + base_short, height)

    # Tính cạnh phải (leg_right) dựa trên tọa độ
    leg_right = np.sqrt((base_long - c[0])**2 + (0 - c[1])**2)

    # Tính diện tích và chu vi
    area = (base_long + base_short) * height / 2.0
    perimeter = base_long + base_short + leg_left + leg_right

    return {
        "points": (a, b, c, d),
        "area": float(area),
        "perimeter": float(perimeter),
        "base_long": float(base_long),
        "base_short": float(base_short),
        "height": float(height),
        "leg_left": float(leg_left),
        "leg_right": float(leg_right),
    }


@st.cache_data(ttl=3600)
def get_isosceles_trapezoid_data(base_long: float, base_short: float, leg: float) -> Dict:
    """Tính toán hình thang cân từ các tham số."""
    base_long = float(base_long)
    base_short = float(base_short)
    leg = float(leg)

    if base_short >= base_long:
        base_short = base_long * 0.6

    # Tính chiều cao từ cạnh bên
    offset = (base_long - base_short) / 2.0
    if leg**2 - offset**2 > 0:
        height = np.sqrt(leg**2 - offset**2)
    else:
        height = 2.0
        leg = np.sqrt(offset**2 + height**2)

    a: Point = (0.0, 0.0)
    b: Point = (base_long, 0.0)
    d: Point = (offset, height)
    c: Point = (offset + base_short, height)

    area = (base_long + base_short) * height / 2.0
    perimeter = base_long + base_short + 2 * leg

    return {
        "points": (a, b, c, d),
        "area": float(area),
        "perimeter": float(perimeter),
        "base_long": float(base_long),
        "base_short": float(base_short),
        "leg": float(leg),
        "leg_left": float(leg),
        "leg_right": float(leg),
        "height": float(height),
    }


def init_session_state() -> None:
    """Khởi tạo trạng thái của trang."""
    defaults = {
        "trapezoid_type": "isosceles",
        "base_long": 8,
        "base_short": 4,
        "leg": 4,
        "height": 3,
        "ai_text_trapezoid": "",
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


def render_drawing_section() -> None:
    """Phần vẽ hình thang với slider điều khiển."""
    st.subheader("▭ Vẽ Hình Thang")

    trapezoid_type = st.radio(
        "Chọn loại hình thang:",
        options=["isosceles", "general"],
        format_func=lambda x: "Hình Thang Cân" if x == "isosceles" else "Hình Thang Tổng Quát",
        horizontal=True,
    )
    st.session_state.trapezoid_type = trapezoid_type

    if trapezoid_type == "isosceles":
        with st.form("isosceles_trapezoid_form"):
            col1, col2, col3, col4 = st.columns([1, 1, 1, 0.9])
            with col1:
                base_long = st.slider(
                    "Đáy lớn (cm)",
                    min_value=3,
                    max_value=12,
                    value=int(st.session_state.base_long),
                )
            with col2:
                base_short = st.slider(
                    "Đáy bé (cm)",
                    min_value=1,
                    max_value=8,
                    value=int(st.session_state.base_short),
                )
            with col3:
                leg = st.slider(
                    "Cạnh bên (cm)",
                    min_value=2,
                    max_value=8,
                    value=int(st.session_state.leg),
                )
            with col4:
                st.write("")
                st.write("")
                redraw = st.form_submit_button("🔄 Vẽ lại", width='stretch')

        if redraw:
            st.session_state.base_long = base_long
            st.session_state.base_short = base_short
            st.session_state.leg = leg

        data = get_isosceles_trapezoid_data(
            float(st.session_state.base_long),
            float(st.session_state.base_short),
            float(st.session_state.leg),
        )

    else:
        if "leg_left" not in st.session_state:
            st.session_state.leg_left = 3
        if "height" not in st.session_state:
            st.session_state.height = 3
        if "fixed_leg" not in st.session_state:
            st.session_state.fixed_leg = "left"

        # Radio để chọn cạnh cố định
        fixed_leg = st.radio(
            "Cạnh cố định:",
            options=["left", "right"],
            format_func=lambda x: "Cạnh trái" if x == "left" else "Cạnh phải",
            horizontal=True,
            key="fixed_leg_radio",
        )
        st.session_state.fixed_leg = fixed_leg

        with st.form("general_trapezoid_form"):
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                base_long = st.slider(
                    "Đáy lớn (cm)",
                    min_value=3,
                    max_value=12,
                    value=int(st.session_state.base_long),
                )
            with col2:
                base_short = st.slider(
                    "Đáy bé (cm)",
                    min_value=1,
                    max_value=8,
                    value=int(st.session_state.base_short),
                )
            with col3:
                height = st.slider(
                    "Chiều cao (cm)",
                    min_value=1,
                    max_value=8,
                    value=int(st.session_state.height),
                )
            with col4:
                leg_label = "Cạnh trái (cm)" if fixed_leg == "left" else "Cạnh phải (cm)"
                leg = st.slider(
                    leg_label,
                    min_value=2,
                    max_value=8,
                    value=int(st.session_state.leg_left),
                )

            st.form_submit_button("🔄 Vẽ lại", width='stretch')

        st.session_state.base_long = base_long
        st.session_state.base_short = base_short
        st.session_state.height = height
        st.session_state.leg_left = leg

        data = get_trapezoid_data(
            float(st.session_state.base_long),
            float(st.session_state.base_short),
            float(st.session_state.leg_left),
            float(st.session_state.height),
            fixed_leg=st.session_state.fixed_leg,
        )

    points = data["points"]

    # Vẽ hình thang
    fig, ax = plt.subplots(figsize=(6, 4))
    trapezoid = patches.Polygon(points, closed=True, facecolor="lightyellow", edgecolor="orange", linewidth=2, alpha=0.6)
    ax.add_patch(trapezoid)

    # Đánh dấu các đỉnh
    labels = ["A", "B", "C", "D"]
    for point, label in zip(points, labels):
        ax.plot(point[0], point[1], "ro", markersize=8)
        ax.text(point[0] - 0.3, point[1] - 0.3, label, fontsize=11, weight="bold", color="darkorange")

    ax.set_xlim(-1, max(p[0] for p in points) + 1)
    ax.set_ylim(-1, max(p[1] for p in points) + 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Hình Thang", fontsize=14, weight="bold")
    st.pyplot(fig, width='stretch')
    plt.close(fig)

    st.markdown("### Thông tin hình:")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.write(f"Đáy lớn = {data['base_long']:.1f} cm")
        st.write(f"Đáy bé = {data['base_short']:.1f} cm")
    with info_col2:
        if 'leg_left' in data and 'leg_right' in data:
            st.write(f"Cạnh trái = {data['leg_left']:.2f} cm")
            st.write(f"Cạnh phải = {data['leg_right']:.2f} cm")
        elif 'leg' in data:
            st.write(f"Cạnh bên = {data['leg']:.2f} cm")
    with info_col3:
        st.write(f"Diện tích = {data['area']:.2f} cm²")
        st.write(f"Chu vi = {data['perimeter']:.2f} cm")


def render_info_section() -> None:
    """Phần giải thích định nghĩa, tính chất, công thức."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(
        "Hình thang là tứ giác có một cặp cạnh đối song song. "
        "Hai cạnh song song được gọi là hai đáy, hai cạnh còn lại gọi là cạnh bên."
    )

    st.markdown("#### Phân Loại")
    with st.expander("🔹 Hình Thang Cân", expanded=True):
        st.write("Hình thang cân có 2 cạnh bên bằng nhau.")

    with st.expander("🔹 Hình Thang Tổng Quát", expanded=False):
        st.write("Hình thang tổng quát có 2 cạnh bên không bằng nhau.")

    st.markdown("#### Tính Chất")
    properties = [
        "Một cặp cạnh đối song song",
        "Tổng hai góc kề một cạnh bên = 180°",
        "(Hình thang cân) Hai góc ở cùng một đáy bằng nhau",
        "(Hình thang cân) Hai đường chéo bằng nhau",
    ]
    for prop in properties:
        st.write(f"🔹 {prop}")

    st.markdown("#### Công Thức")
    st.write("Diện tích: S = (a + b) × h ÷ 2 (a, b là hai đáy, h là chiều cao)")

    if st.button("🤖 Giải Thích AI", width='stretch'):
        ai_properties = {
            "định_nghĩa": "tứ giác có một cặp cạnh đối song song",
            "cạnh_bên": "hai cạnh không song song",
            "hình_thang_cân": "hai cạnh bên bằng nhau",
            "diện_tích": "(a + b) × h ÷ 2",
        }

        try:
            ai_text = get_ai_explanation(
                "Hình thang",
                ai_properties
            )
            st.session_state.ai_text_trapezoid = ai_text
        except Exception:
            st.session_state.ai_text_trapezoid = "Không thể gọi AI"

    if st.session_state.ai_text_trapezoid:
        if st.session_state.ai_text_trapezoid == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_trapezoid == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_trapezoid)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Phân biệt hình thang cân và hình thangtổng quát bằng độ dài cạnh bên")
        st.write("- Khoảng cách giữa hai đáy bằng độ dài đoạn vuông góc giữa hai đáy")
        st.write("- Tính diện tích bằng công thức (a + b) × h ÷ 2")


def main() -> None:
    """Hàm chính chạy toàn bộ trang."""
    init_session_state()
    render_sidebar()

    st.title("• Hình Thang")
    st.caption("Khám phá định nghĩa, phân loại và tính chất của hình thang")

    render_drawing_section()
    st.divider()
    render_info_section()


if __name__ == "__main__":
    main()
