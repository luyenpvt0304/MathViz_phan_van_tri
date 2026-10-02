# -*- coding: utf-8 -*-
"""🔷 Hình Bình Hành"""

from __future__ import annotations

from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation
from utils.explanations import get_definition, get_properties
from utils.geometry_tools import (
    calculate_area_polygon,
    calculate_distance,
    calculate_perimeter,
    draw_parallelogram,
)

Point = Tuple[float, float]


@st.cache_data(ttl=3600)
def get_parallelogram_data(ab: float, ad: float, angle_deg: float) -> Dict[str, float | Tuple[Point, ...]]:
    """Tính và cache toàn bộ dữ liệu của hình bình hành từ 3 tham số đầu vào."""
    angle_rad = float(np.deg2rad(angle_deg))

    a: Point = (0.0, 0.0)
    b: Point = (float(ab), 0.0)
    d: Point = (float(ad * np.cos(angle_rad)), float(ad * np.sin(angle_rad)))
    c: Point = (b[0] + d[0], b[1] + d[1])

    points: Tuple[Point, ...] = (a, b, c, d)

    bc = calculate_distance(b, c)
    cd = calculate_distance(c, d)
    area = calculate_area_polygon(points)
    perimeter = calculate_perimeter(points)
    height = float(ad * np.sin(angle_rad))

    return {
        "points": points,
        "bc": float(bc),
        "cd": float(cd),
        "area": float(area),
        "perimeter": float(perimeter),
        "height": float(height),
    }


@st.cache_data(ttl=3600)
def get_ai_explanation_cached(shape_name: str, properties_items: Tuple[Tuple[str, str], ...]) -> str:
    """Cache phần giải thích AI để tránh gọi API lặp lại nhiều lần."""
    properties = dict(properties_items)
    return get_ai_explanation(shape_name, properties)


def init_session_state() -> None:
    """Khởi tạo session state cho tham số hình và API key."""
    if "ab" not in st.session_state:
        st.session_state.ab = 5

    if "ad" not in st.session_state:
        st.session_state.ad = 3

    if "angle_a" not in st.session_state:
        st.session_state.angle_a = 60

    if "ai_text_parallelogram" not in st.session_state:
        st.session_state.ai_text_parallelogram = ""

    if "api_key" not in st.session_state:
        try:
            st.session_state.api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            st.session_state.api_key = ""


def render_sidebar_key_input() -> None:
    """Cho phép nhập API key ở sidebar để dùng cho nút giải thích AI."""
    with st.sidebar:
        st.markdown("### 🔑 API Gemini")
        api_key = st.text_input(
            "API key (tùy chọn)",
            value=str(st.session_state.api_key),
            type="password",
            help="Có thể để trống nếu chỉ dùng giải thích tĩnh.",
        )
        st.session_state.api_key = api_key.strip()


def render_left_column() -> Dict[str, float | Tuple[Point, ...]]:
    """Cột trái: nhập tham số, vẽ hình, hiển thị thông tin tính toán."""
    st.subheader("▭ Vẽ Hình Bình Hành")

    # Form ngang gồm 3 slider và 1 nút vẽ lại.
    with st.form("parallelogram_form"):
        slider_col_1, slider_col_2, slider_col_3, button_col = st.columns([1, 1, 1, 0.9])

        with slider_col_1:
            ab = st.slider("Cạnh AB (cm)", min_value=1, max_value=10, value=int(st.session_state.ab))

        with slider_col_2:
            ad = st.slider("Cạnh AD (cm)", min_value=1, max_value=10, value=int(st.session_state.ad))

        with slider_col_3:
            angle_a = st.slider(
                "Góc A (°)",
                min_value=30,
                max_value=150,
                value=int(st.session_state.angle_a),
            )

        with button_col:
            st.write("")
            st.write("")
            redraw_clicked = st.form_submit_button("🔄 Vẽ lại", use_container_width=True)

    # Lưu tham số vào session state để giữ trạng thái giữa các lần rerun.
    if redraw_clicked:
        st.session_state.ab = ab
        st.session_state.ad = ad
        st.session_state.angle_a = angle_a
    else:
        ab = int(st.session_state.ab)
        ad = int(st.session_state.ad)
        angle_a = int(st.session_state.angle_a)

    data = get_parallelogram_data(float(ab), float(ad), float(angle_a))
    points = data["points"]

    # Tạo hình matplotlib và vẽ bằng hàm trong utils.
    fig, ax = plt.subplots(figsize=(6, 4))
    draw_parallelogram(fig, ax, points, title="Hình Bình Hành ABCD")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("### Thông tin hình:")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.write(f"AB = {ab:.0f} cm")
        st.write(f"AD = {ad:.0f} cm")
        st.write(f"∠ A = {angle_a:.0f}°")
        st.write(f"BC = {data['bc']:.2f} cm (= AD)")
    with info_col2:
        st.write(f"CD = {data['cd']:.2f} cm (= AB)")
        st.write(f"Diện tích = {data['area']:.2f} cm²")
        st.write(f"Chu vi = {data['perimeter']:.2f} cm")

    return data


def render_right_column(data: Dict[str, float | Tuple[Point, ...]]) -> None:
    """Cột phải: Định nghĩa, tính chất, công thức, AI và mẹo học tập."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(get_definition("Hình bình hành"))

    st.markdown("#### Tính Chất")
    properties = get_properties("Hình bình hành")
    for prop in properties:
        st.write(f"🔹 {prop}")

    st.markdown("#### Công Thức")
    ab = float(st.session_state.ab)
    ad = float(st.session_state.ad)
    h = float(data["height"])
    area = float(data["area"])
    perimeter = float(data["perimeter"])

    st.write(f"Diện tích: S = a × h = {ab:.0f} × {h:.2f} = {area:.2f} cm²")
    st.write(f"Chu vi: P = 2(a + b) = 2({ab:.0f} + {ad:.0f}) = {perimeter:.2f} cm")

    if st.button("🤖 Giải Thích AI", use_container_width=True):
        ai_properties = {
            "cạnh_đối": "song song và bằng nhau",
            "góc_đối": "bằng nhau",
            "AB": f"{st.session_state.ab} cm",
            "AD": f"{st.session_state.ad} cm",
            "góc_A": f"{st.session_state.angle_a}°",
        }

        try:
            ai_text = get_ai_explanation_cached(
                "Hình bình hành",
                tuple(sorted((str(k), str(v)) for k, v in ai_properties.items())),
            )
            st.session_state.ai_text_parallelogram = ai_text
        except Exception:
            st.session_state.ai_text_parallelogram = "Không thể gọi AI"

    # Hiển thị kết quả AI sau khi bấm nút.
    if st.session_state.ai_text_parallelogram:
        if st.session_state.ai_text_parallelogram == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_parallelogram == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_parallelogram)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Kéo slider để thay đổi kích thước")
        st.write("- Quan sát: Cạnh đối luôn bằng nhau")
        st.write("- Thử thay đổi góc A xem chuyện gì xảy ra")


def main() -> None:
    """Hàm chính chạy toàn bộ trang học hình bình hành."""
    init_session_state()
    render_sidebar_key_input()

    st.title("Hình Bình Hành")
    st.caption("Khám phá trực quan và hiểu bản chất hình học qua AI")

    left_col, right_col = st.columns([3, 2])

    with left_col:
        data = render_left_column()

    with right_col:
        render_right_column(data)


if __name__ == "__main__":
    main()
