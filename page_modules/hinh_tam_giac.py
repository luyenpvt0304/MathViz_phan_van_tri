# -*- coding: utf-8 -*-
"""▲ Hình Tam Giác"""

from __future__ import annotations

from typing import Dict, Tuple
import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import streamlit as st

from utils.ai_helper import get_explanation as get_ai_explanation

Point = Tuple[float, float]


def get_midpoint(p1: Point, p2: Point) -> Point:
    """Tính trung điểm của 2 điểm."""
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def get_median_line(vertex: Point, opposite_midpoint: Point) -> Tuple[Point, Point]:
    """Trả về đường trung tuyến từ đỉnh đến trung điểm cạnh đối diện."""
    return (vertex, opposite_midpoint)


def get_angle_bisector(vertex: Point, p1: Point, p2: Point, length: float = 3) -> Tuple[Point, Point]:
    """Trả về đường phân giác từ đỉnh (chia góc thành 2 phần bằng nhau)."""
    # Vector từ đỉnh đến 2 điểm
    v1 = np.array([p1[0] - vertex[0], p1[1] - vertex[1]])
    v2 = np.array([p2[0] - vertex[0], p2[1] - vertex[1]])

    # Normalize vectors
    v1_norm = v1 / (np.linalg.norm(v1) + 1e-10)
    v2_norm = v2 / (np.linalg.norm(v2) + 1e-10)

    # Bisector direction
    bisector = v1_norm + v2_norm
    bisector = bisector / (np.linalg.norm(bisector) + 1e-10)

    # End point
    end_point = (vertex[0] + bisector[0] * length, vertex[1] + bisector[1] * length)
    return (vertex, end_point)


def get_perpendicular_bisector(p1: Point, p2: Point, length: float = 2) -> Tuple[Point, Point]:
    """Trả về đường trung trực (vuông góc với cạnh tại trung điểm)."""
    midpoint = get_midpoint(p1, p2)

    # Vector cạnh
    edge = np.array([p2[0] - p1[0], p2[1] - p1[1]])

    # Vector vuông góc (quay 90 độ)
    perpendicular = np.array([-edge[1], edge[0]])
    perpendicular = perpendicular / (np.linalg.norm(perpendicular) + 1e-10)

    # 2 điểm trên đường trung trực
    p_start = (midpoint[0] - perpendicular[0] * length, midpoint[1] - perpendicular[1] * length)
    p_end = (midpoint[0] + perpendicular[0] * length, midpoint[1] + perpendicular[1] * length)

    return (p_start, p_end)


def get_incenter(a_pt: Point, b_pt: Point, c_pt: Point, side_a: float, side_b: float, side_c: float) -> Point:
    """Tính tâm đường tròn nội tiếp (incenter) - giao điểm 3 đường phân giác."""
    perimeter = side_a + side_b + side_c
    if perimeter == 0:
        return ((a_pt[0] + b_pt[0] + c_pt[0]) / 3, (a_pt[1] + b_pt[1] + c_pt[1]) / 3)

    # I = (a*A + b*B + c*C) / (a+b+c)
    ix = (side_a * a_pt[0] + side_b * b_pt[0] + side_c * c_pt[0]) / perimeter
    iy = (side_a * a_pt[1] + side_b * b_pt[1] + side_c * c_pt[1]) / perimeter

    return (ix, iy)


def get_circumcenter(a_pt: Point, b_pt: Point, c_pt: Point) -> Point:
    """Tính tâm đường tròn ngoại tiếp (circumcenter) - giao điểm 3 đường trung trực."""
    ax, ay = a_pt
    bx, by = b_pt
    cx, cy = c_pt

    # Sử dụng công thức từ hình học
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

    if abs(d) < 1e-10:
        # Tam giác suy biến, trả về trọng tâm
        return ((ax + bx + cx) / 3, (ay + by + cy) / 3)

    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d

    return (ux, uy)


def get_inradius(area: float, side_a: float, side_b: float, side_c: float) -> float:
    """Tính bán kính đường tròn nội tiếp."""
    s = (side_a + side_b + side_c) / 2
    if s == 0:
        return 0
    return area / s


def get_circumradius(area: float, side_a: float, side_b: float, side_c: float) -> float:
    """Tính bán kính đường tròn ngoại tiếp."""
    if area == 0:
        return 0
    return (side_a * side_b * side_c) / (4 * area)


@st.cache_data(ttl=3600)
def get_triangle_data(side_a: float, side_b: float, angle_c_deg: float) -> Dict[str, float]:
    """Tính các đại lượng cơ bản của hình tam giác."""
    angle_c_rad = np.deg2rad(angle_c_deg)
    side_a = float(side_a)
    side_b = float(side_b)

    # Tính cạnh c từ định lý cosin
    side_c = math.sqrt(side_a**2 + side_b**2 - 2*side_a*side_b*np.cos(angle_c_rad))

    # Tính diện tích
    area = 0.5 * side_a * side_b * np.sin(angle_c_rad)

    # Tính chu vi
    perimeter = side_a + side_b + side_c

    # Tính chiều cao từ cạnh c
    height = 2 * area / side_c if side_c > 0 else 0

    return {
        "side_a": float(side_a),
        "side_b": float(side_b),
        "side_c": float(side_c),
        "angle_c": float(angle_c_deg),
        "area": float(area),
        "perimeter": float(perimeter),
        "height": float(height),
    }


def init_session_state() -> None:
    """Khởi tạo trạng thái của trang."""
    defaults = {
        "triangle_a": 5,
        "triangle_b": 4,
        "triangle_angle": 60,
        "ai_text_triangle": "",
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
    """Phần vẽ hình tam giác với slider điều khiển."""
    st.subheader("▲ Vẽ Hình Tam Giác")

    # Radio button chọn loại đường
    special_line = st.radio(
        "Hiển thị đường đặc biệt:",
        options=["none", "median", "angle_bisector", "perpendicular_bisector"],
        format_func=lambda x: {
            "none": "Không",
            "median": "Đường trung tuyến",
            "angle_bisector": "Đường phân giác",
            "perpendicular_bisector": "Đường trung trực",
        }.get(x, x),
        horizontal=True,
    )

    with st.form("triangle_form"):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 0.9])
        with col1:
            a = st.slider(
                "Cạnh a (cm)",
                min_value=2,
                max_value=8,
                value=int(st.session_state.triangle_a),
            )
        with col2:
            b = st.slider(
                "Cạnh b (cm)",
                min_value=2,
                max_value=8,
                value=int(st.session_state.triangle_b),
            )
        with col3:
            angle = st.slider(
                "Góc C (°)",
                min_value=30,
                max_value=150,
                value=int(st.session_state.triangle_angle),
            )
        with col4:
            st.write("")
            st.write("")
            redraw = st.form_submit_button("🔄 Vẽ lại", width='stretch')

    if redraw:
        st.session_state.triangle_a = a
        st.session_state.triangle_b = b
        st.session_state.triangle_angle = angle
    else:
        a = st.session_state.triangle_a
        b = st.session_state.triangle_b
        angle = st.session_state.triangle_angle

    data = get_triangle_data(float(a), float(b), float(angle))

    # Tính tọa độ các đỉnh
    c_point = (float(b), 0)
    angle_rad = np.deg2rad(angle)
    a_point = (float(a) * np.cos(angle_rad), float(a) * np.sin(angle_rad))
    b_point = (0, 0)

    points = [b_point, c_point, a_point]

    # Vẽ hình tam giác
    fig, ax = plt.subplots(figsize=(6, 4))
    triangle = patches.Polygon(points, closed=True, facecolor="lightyellow", edgecolor="orange", linewidth=2, alpha=0.6)
    ax.add_patch(triangle)

    # Đánh dấu các đỉnh
    labels = ["B", "C", "A"]
    for point, label in zip(points, labels):
        ax.plot(point[0], point[1], "ro", markersize=8)
        ax.text(point[0] - 0.3, point[1] - 0.3, label, fontsize=11, weight="bold", color="darkorange")

    # Vẽ chiều cao
    foot_of_height = (a_point[0], 0)
    ax.plot([a_point[0], foot_of_height[0]], [a_point[1], foot_of_height[1]], "g--", linewidth=1, alpha=0.5, label="Chiều cao")

    # Vẽ các đường đặc biệt
    if special_line == "median":
        # Đường trung tuyến từ mỗi đỉnh
        mid_bc = get_midpoint(b_point, c_point)
        mid_ac = get_midpoint(a_point, c_point)
        mid_ab = get_midpoint(a_point, b_point)

        ax.plot([a_point[0], mid_bc[0]], [a_point[1], mid_bc[1]], "b-", linewidth=1.5, alpha=0.7, label="Trung tuyến")
        ax.plot([b_point[0], mid_ac[0]], [b_point[1], mid_ac[1]], "b-", linewidth=1.5, alpha=0.7)
        ax.plot([c_point[0], mid_ab[0]], [c_point[1], mid_ab[1]], "b-", linewidth=1.5, alpha=0.7)

    elif special_line == "angle_bisector":
        # Đường phân giác từ mỗi đỉnh
        bisec_a = get_angle_bisector(a_point, b_point, c_point, length=3)
        bisec_b = get_angle_bisector(b_point, a_point, c_point, length=3)
        bisec_c = get_angle_bisector(c_point, a_point, b_point, length=3)

        ax.plot([bisec_a[0][0], bisec_a[1][0]], [bisec_a[0][1], bisec_a[1][1]], "r-", linewidth=1.5, alpha=0.7, label="Phân giác")
        ax.plot([bisec_b[0][0], bisec_b[1][0]], [bisec_b[0][1], bisec_b[1][1]], "r-", linewidth=1.5, alpha=0.7)
        ax.plot([bisec_c[0][0], bisec_c[1][0]], [bisec_c[0][1], bisec_c[1][1]], "r-", linewidth=1.5, alpha=0.7)

        # Vẽ tâm đường tròn nội tiếp
        incenter = get_incenter(a_point, b_point, c_point, data['side_a'], data['side_b'], data['side_c'])
        inradius = get_inradius(data['area'], data['side_a'], data['side_b'], data['side_c'])

        ax.plot(incenter[0], incenter[1], "r*", markersize=15, label="Tâm nội tiếp")
        circle_in = patches.Circle(incenter, inradius, fill=False, edgecolor="red", linewidth=1, alpha=0.5, linestyle="--")
        ax.add_patch(circle_in)

    elif special_line == "perpendicular_bisector":
        # Đường trung trực của mỗi cạnh
        perp_bc = get_perpendicular_bisector(b_point, c_point, length=1.5)
        perp_ac = get_perpendicular_bisector(a_point, c_point, length=1.5)
        perp_ab = get_perpendicular_bisector(a_point, b_point, length=1.5)

        ax.plot([perp_bc[0][0], perp_bc[1][0]], [perp_bc[0][1], perp_bc[1][1]], "m-", linewidth=1.5, alpha=0.7, label="Trung trực")
        ax.plot([perp_ac[0][0], perp_ac[1][0]], [perp_ac[0][1], perp_ac[1][1]], "m-", linewidth=1.5, alpha=0.7)
        ax.plot([perp_ab[0][0], perp_ab[1][0]], [perp_ab[0][1], perp_ab[1][1]], "m-", linewidth=1.5, alpha=0.7)

        # Vẽ tâm đường tròn ngoại tiếp
        circumcenter = get_circumcenter(a_point, b_point, c_point)
        circumradius = get_circumradius(data['area'], data['side_a'], data['side_b'], data['side_c'])

        ax.plot(circumcenter[0], circumcenter[1], "m*", markersize=15, label="Tâm ngoại tiếp")
        circle_out = patches.Circle(circumcenter, circumradius, fill=False, edgecolor="magenta", linewidth=1, alpha=0.5, linestyle="--")
        ax.add_patch(circle_out)

    x_min = min(p[0] for p in points) - 1
    x_max = max(p[0] for p in points) + 1
    y_min = min(p[1] for p in points) - 1
    y_max = max(p[1] for p in points) + 1

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title("Hình Tam Giác ABC", fontsize=14, weight="bold")
    st.pyplot(fig, width='stretch')
    plt.close(fig)

    st.markdown("### Thông tin hình:")
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.write(f"Cạnh a = {data['side_a']:.1f} cm")
        st.write(f"Cạnh b = {data['side_b']:.1f} cm")
        st.write(f"Cạnh c = {data['side_c']:.2f} cm")
    with info_col2:
        st.write(f"Góc C = {angle:.0f}°")
        st.write(f"Diện tích = {data['area']:.2f} cm²")
        st.write(f"Chu vi = {data['perimeter']:.2f} cm")

    return data


def render_info_section(data: Dict[str, float]) -> None:
    """Phần giải thích định nghĩa, tính chất, công thức."""
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(
        "Hình tam giác là một đa giác có ba cạnh và ba góc. "
        "Ba cạnh được nối với nhau tại ba đỉnh."
    )

    st.markdown("#### Phân Loại")
    with st.expander("🔹 Theo Cạnh", expanded=True):
        st.write("- Tam giác đều: ba cạnh bằng nhau, ba góc = 60°")
        st.write("- Tam giác cân: hai cạnh bằng nhau")
        st.write("- Tam giác thường: ba cạnh khác nhau")

    with st.expander("🔹 Theo Góc", expanded=False):
        st.write("- Tam giác nhọn: ba góc < 90°")
        st.write("- Tam giác vuông: một góc = 90°")
        st.write("- Tam giác tù: một góc > 90°")

    st.markdown("#### Tính Chất")
    properties = [
        "Tổng ba góc = 180°",
        "Hiệu của hai cạnh bất kỳ < cạnh thứ ba",
        "Đường cao từ một đỉnh vuông góc với cạnh đối diện",
        "Ba đường trung tuyến cắt nhau tại trọng tâm",
        "Ba đường cao cắt nhau tại trực tâm",
    ]
    for prop in properties:
        st.write(f"🔹 {prop}")

    st.markdown("#### Đường Đặc Biệt")
    special_lines = [
        "**Đường trung tuyến**: Nối từ đỉnh đến trung điểm cạnh đối diện. Ba đường trung tuyến gặp nhau tại trọng tâm.",
        "**Đường phân giác**: Chia góc của đỉnh thành hai phần bằng nhau.",
        "**Đường trung trực**: Vuông góc với cạnh tại trung điểm.",
    ]
    for line in special_lines:
        st.write(f"🔹 {line}")

    st.markdown("#### Các Tâm Đặc Biệt")
    special_centers = [
        "**Tâm nội tiếp (I)**: Giao điểm của ba đường phân giác. Là tâm của đường tròn nội tiếp (tiếp xúc với 3 cạnh).",
        "**Tâm ngoại tiếp (O)**: Giao điểm của ba đường trung trực. Là tâm của đường tròn ngoại tiếp (đi qua 3 đỉnh).",
        "**Trọng tâm (G)**: Giao điểm của ba đường trung tuyến. Chia mỗi đường trung tuyến theo tỉ lệ 2:1.",
    ]
    for center in special_centers:
        st.write(f"🔹 {center}")

    st.markdown("#### Công Thức")
    st.write(f"Diện tích: S = (1/2) × a × b × sin(C) = (1/2) × {data['side_a']:.0f} × {data['side_b']:.0f} × sin({data['angle_c']:.0f}°) = {data['area']:.2f} cm²")
    st.write(f"Chu vi: P = a + b + c = {data['side_a']:.0f} + {data['side_b']:.0f} + {data['side_c']:.2f} = {data['perimeter']:.2f} cm")

    if st.button("🤖 Giải Thích AI", width='stretch'):
        ai_properties = {
            "định_nghĩa": "hình có ba cạnh và ba góc",
            "tổng_góc": "180°",
            "công_thức_diện_tích": "(1/2) × a × b × sin(C)",
            "cạnh_a": f"{data['side_a']:.0f} cm",
            "cạnh_b": f"{data['side_b']:.0f} cm",
        }

        try:
            ai_text = get_ai_explanation(
                "Hình tam giác",
                ai_properties
            )
            st.session_state.ai_text_triangle = ai_text
        except Exception:
            st.session_state.ai_text_triangle = "Không thể gọi AI"

    if st.session_state.ai_text_triangle:
        if st.session_state.ai_text_triangle == "Cần API key":
            st.warning("Cần API key")
        elif st.session_state.ai_text_triangle == "Không thể gọi AI":
            st.error("Không thể gọi AI")
        else:
            st.success(st.session_state.ai_text_triangle)

    with st.expander("💡 Mẹo học tập"):
        st.write("- Tổng ba góc của bất kỳ tam giác nào đều = 180°")
        st.write("- Tính diện tích bằng công thức (1/2) × cơ sở × chiều cao")
        st.write("- Kéo slider để thay đổi kích thước cạnh và góc")


def main() -> None:
    """Hàm chính chạy toàn bộ trang."""
    init_session_state()
    render_sidebar()

    st.title("▲ Hình Tam Giác")
    st.caption("Khám phá tính chất và công thức tính diện tích hình tam giác")

    left_col, right_col = st.columns([3, 2])

    with left_col:
        data = render_drawing_section()

    with right_col:
        render_info_section(data)


if __name__ == "__main__":
    main()
