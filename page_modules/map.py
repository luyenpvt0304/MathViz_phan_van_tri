# -*- coding: utf-8 -*-
"""Sơ đồ tư duy tương tác: Các tứ giác đặc biệt."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon
import streamlit as st

Point = Tuple[float, float]


@dataclass(frozen=True)
class ShapeNode:
    title: str
    center: Point
    color: str
    properties: Tuple[str, ...]


NODES: Dict[str, ShapeNode] = {
    "Tứ giác": ShapeNode(
        "TỨ GIÁC", (5.0, 8.8), "#E8EAF6",
        ("Gồm 4 cạnh, 4 đỉnh", "Tổng các góc bằng 360°"),
    ),
    "Hình thang": ShapeNode(
        "HÌNH THANG", (5.0, 7.0), "#FFF3E0",
        ("Có một cặp cạnh đối song song", "Ví dụ: AB // CD"),
    ),
    "Hình thang cân": ShapeNode(
        "HÌNH THANG CÂN", (2.0, 5.1), "#E3F2FD",
        ("Hai góc kề một đáy bằng nhau", "Hai đường chéo bằng nhau"),
    ),
    "Hình thang vuông": ShapeNode(
        "HÌNH THANG VUÔNG", (5.0, 5.1), "#F3E5F5",
        ("Có một góc vuông", "Có hai góc vuông"),
    ),
    "Hình bình hành": ShapeNode(
        "HÌNH BÌNH HÀNH", (8.0, 5.1), "#E8F5E9",
        ("Các cạnh đối song song, bằng nhau", "Các góc đối bằng nhau", "Đường chéo cắt nhau tại trung điểm"),
    ),
    "Hình chữ nhật": ShapeNode(
        "HÌNH CHỮ NHẬT", (2.7, 2.8), "#E0F7FA",
        ("Bốn góc vuông", "Hai đường chéo bằng nhau", "Đường chéo cắt nhau tại trung điểm"),
    ),
    "Hình thoi": ShapeNode(
        "HÌNH THOI", (7.3, 2.8), "#FFF8E1",
        ("Bốn cạnh bằng nhau", "Đường chéo vuông góc", "Đường chéo là phân giác các góc"),
    ),
    "Hình vuông": ShapeNode(
        "HÌNH VUÔNG", (5.0, 0.8), "#FFEBEE",
        ("Bốn cạnh bằng nhau", "Bốn góc vuông", "Đường chéo bằng nhau và vuông góc"),
    ),
}

# (nút nguồn, nút đích, điều kiện chuyển)
EDGES: List[Tuple[str, str, str]] = [
    ("Tứ giác", "Hình thang", "Có một cặp cạnh đối song song"),
    ("Tứ giác", "Hình bình hành", "Hai cặp cạnh đối song song"),
    ("Hình thang", "Hình thang cân", "Hai góc kề một đáy bằng nhau\nhoặc hai đường chéo bằng nhau"),
    ("Hình thang", "Hình thang vuông", "Có một góc vuông"),
    ("Hình thang", "Hình bình hành", "Hai cạnh bên song song\nhoặc một cặp cạnh đối song song và bằng nhau"),
    ("Hình thang cân", "Hình chữ nhật", "Có một góc vuông"),
    ("Hình thang vuông", "Hình chữ nhật", "Cặp cạnh bên song song"),
    ("Hình bình hành", "Hình chữ nhật", "Có một góc vuông\nhoặc hai đường chéo bằng nhau"),
    ("Hình bình hành", "Hình thoi", "Hai cạnh kề bằng nhau\nhoặc hai đường chéo vuông góc\nhoặc một đường chéo là phân giác một góc"),
    ("Hình chữ nhật", "Hình vuông", "Hai cạnh kề bằng nhau\nhoặc đường chéo vuông góc\nhoặc một đường chéo là phân giác một góc"),
    ("Hình thoi", "Hình vuông", "Có một góc vuông\nhoặc hai đường chéo bằng nhau"),
]


def draw_shape_icon(ax, name: str, center: Point, scale: float = 0.34) -> None:
    """Vẽ biểu tượng hình học nhỏ bên trong mỗi nút."""
    x, y = center
    if name == "Tứ giác":
        pts = [(x-0.8*scale,y-0.4*scale),(x-0.45*scale,y+0.65*scale),(x+0.65*scale,y+0.45*scale),(x+0.75*scale,y-0.55*scale)]
    elif name in {"Hình thang", "Hình thang cân", "Hình thang vuông"}:
        left_top = -0.55 if name != "Hình thang vuông" else -0.8
        pts = [(x-0.8*scale,y-0.5*scale),(x+0.8*scale,y-0.5*scale),(x+0.5*scale,y+0.5*scale),(x+left_top*scale,y+0.5*scale)]
    elif name == "Hình bình hành":
        pts = [(x-0.8*scale,y-0.5*scale),(x+0.55*scale,y-0.5*scale),(x+0.8*scale,y+0.5*scale),(x-0.55*scale,y+0.5*scale)]
    elif name == "Hình chữ nhật":
        pts = [(x-0.8*scale,y-0.5*scale),(x+0.8*scale,y-0.5*scale),(x+0.8*scale,y+0.5*scale),(x-0.8*scale,y+0.5*scale)]
    elif name == "Hình thoi":
        pts = [(x-0.9*scale,y),(x,y-0.6*scale),(x+0.9*scale,y),(x,y+0.6*scale)]
    else:
        pts = [(x-0.6*scale,y-0.6*scale),(x+0.6*scale,y-0.6*scale),(x+0.6*scale,y+0.6*scale),(x-0.6*scale,y+0.6*scale)]
    ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor="#263B80", linewidth=1.4))


def draw_node(ax, name: str, selected: str) -> None:
    node = NODES[name]
    x, y = node.center
    width, height = 2.35, 1.05
    border = "#D32F2F" if name == selected else "#334E9E"
    line_width = 2.8 if name == selected else 1.5
    box = FancyBboxPatch(
        (x-width/2, y-height/2), width, height,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor=node.color, edgecolor=border, linewidth=line_width, zorder=3,
    )
    ax.add_patch(box)
    draw_shape_icon(ax, name, (x-0.78, y), 0.45)
    ax.text(x+0.15, y, node.title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#172B4D", zorder=4)


def draw_edge(ax, source: str, target: str, label: str, show_labels: bool) -> None:
    x1, y1 = NODES[source].center
    x2, y2 = NODES[target].center
    arrow = FancyArrowPatch(
        (x1, y1-0.56), (x2, y2+0.56),
        arrowstyle="-|>", mutation_scale=13,
        linewidth=1.25, color="#455A64",
        connectionstyle="arc3,rad=0.04", zorder=1,
    )
    ax.add_patch(arrow)
    if show_labels:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my, label, ha="center", va="center", fontsize=6.8,
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#B0BEC5", alpha=0.95), zorder=5)


def create_mind_map(selected: str, show_labels: bool):
    fig, ax = plt.subplots(figsize=(14, 11))
    for source, target, label in EDGES:
        draw_edge(ax, source, target, label, show_labels)
    for name in NODES:
        draw_node(ax, name, selected)

    ax.set_xlim(0.2, 9.8)
    ax.set_ylim(-0.1, 9.6)
    ax.axis("off")
    ax.set_title("SƠ ĐỒ TƯ DUY CÁC TỨ GIÁC ĐẶC BIỆT", fontsize=18, fontweight="bold", color="#17367D", pad=18)
    fig.tight_layout()
    return fig


def render_details(selected: str) -> None:
    node = NODES[selected]
    st.subheader(f"📘 {node.title.title()}")
    st.markdown("#### Tính chất chính")
    for item in node.properties:
        st.write(f"🔹 {item}")

    incoming = [(s, text) for s, t, text in EDGES if t == selected]
    outgoing = [(t, text) for s, t, text in EDGES if s == selected]

    if incoming:
        st.markdown("#### Dấu hiệu nhận biết từ hình khác")
        for source, condition in incoming:
            st.write(f"**{NODES[source].title.title()} → {node.title.title()}:** {condition}")
    if outgoing:
        st.markdown("#### Có thể suy ra hình đặc biệt hơn")
        for target, condition in outgoing:
            st.write(f"**{node.title.title()} → {NODES[target].title.title()}:** {condition}")


def main() -> None:
    st.set_page_config(page_title="Sơ đồ tư duy hình học", page_icon="🧠", layout="wide")
    st.title("🧠 Sơ đồ tư duy Toán hình")
    st.caption("Hệ thống hóa mối quan hệ, tính chất và dấu hiệu nhận biết các tứ giác đặc biệt")

    with st.sidebar:
        st.header("Tùy chọn hiển thị")
        selected = st.selectbox("Chọn hình cần học", list(NODES.keys()), index=7)
        show_labels = st.checkbox("Hiện điều kiện trên các mũi tên", value=True)
        st.info("Mũi tên chỉ hướng từ khái niệm tổng quát đến trường hợp đặc biệt hơn.")

    left, right = st.columns([3.4, 1.6])
    with left:
        fig = create_mind_map(selected, show_labels)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with right:
        render_details(selected)

    st.markdown("### Cách ghi nhớ nhanh")
    cols = st.columns(3)
    with cols[0]:
        st.success("**Hình chữ nhật**\n\nHình bình hành + một góc vuông")
    with cols[1]:
        st.warning("**Hình thoi**\n\nHình bình hành + hai cạnh kề bằng nhau")
    with cols[2]:
        st.error("**Hình vuông**\n\nVừa là hình chữ nhật, vừa là hình thoi")


if __name__ == "__main__":
    main()
