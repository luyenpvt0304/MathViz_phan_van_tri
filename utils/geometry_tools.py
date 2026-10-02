# -*- coding: utf-8 -*-
"""Các công cụ vẽ hình và tính toán hình học cho dự án lớp 8."""

from __future__ import annotations

from typing import List, Sequence, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

Point = Tuple[float, float]


def _to_point(point: Sequence[float]) -> Point:
    """Chuyển dữ liệu điểm bất kỳ thành tuple (x, y) kiểu float."""
    if len(point) != 2:
        raise ValueError("Mỗi điểm phải có đúng 2 giá trị (x, y).")

    return float(point[0]), float(point[1])


def _validate_points(points: Sequence[Sequence[float]]) -> List[Point]:
    """Kiểm tra danh sách 4 điểm A, B, C, D hợp lệ."""
    if len(points) != 4:
        raise ValueError("Cần đúng 4 điểm theo thứ tự A, B, C, D.")

    parsed_points = [_to_point(point) for point in points]

    # Tránh trường hợp trùng điểm hoàn toàn vì gây sai số khi tính góc/cạnh.
    if len(set(parsed_points)) < 4:
        raise ValueError("Bốn điểm phải khác nhau.")

    return parsed_points


def _draw_shape(
    fig: plt.Figure,
    ax: plt.Axes,
    points: Sequence[Sequence[float]],
    title: str,
) -> plt.Figure:
    """Vẽ một tứ giác bất kỳ gồm cạnh, điểm, nhãn và độ dài cạnh."""
    valid_points = _validate_points(points)
    labels = ["A", "B", "C", "D"]

    # Dùng Polygon để thể hiện rõ biên của hình.
    polygon = patches.Polygon(
        valid_points,
        closed=True,
        fill=False,
        edgecolor="black",
        linewidth=2,
    )
    ax.add_patch(polygon)

    x_coords = [point[0] for point in valid_points]
    y_coords = [point[1] for point in valid_points]
    centroid_x = float(np.mean(x_coords))
    centroid_y = float(np.mean(y_coords))
    span = max(max(x_coords) - min(x_coords), max(y_coords) - min(y_coords))
    label_offset = max(0.15, 0.04 * span)

    for i in range(4):
        p1 = valid_points[i]
        p2 = valid_points[(i + 1) % 4]

        # Vẽ cạnh.
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=2)

        # Hiển thị độ dài cạnh tại trung điểm.
        length = calculate_distance(p1, p2)
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        edge_norm = float(np.hypot(dx, dy))

        if edge_norm > 0:
            normal_x = -dy / edge_norm
            normal_y = dx / edge_norm

            to_centroid_x = centroid_x - mid_x
            to_centroid_y = centroid_y - mid_y
            if normal_x * to_centroid_x + normal_y * to_centroid_y > 0:
                normal_x = -normal_x
                normal_y = -normal_y
        else:
            normal_x, normal_y = 0.0, 1.0

        label_x = mid_x + normal_x * label_offset
        label_y = mid_y + normal_y * label_offset

        ax.text(
            label_x,
            label_y,
            f"{length:.2f}",
            color="blue",
            fontsize=10,
            ha="center",
            va="center",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.75, "pad": 1.2},
            zorder=6,
        )

    # Vẽ 4 điểm màu đỏ và gắn nhãn A, B, C, D.
    ax.scatter(x_coords, y_coords, color="red", s=40, zorder=5)

    for label, (x, y) in zip(labels, valid_points):
        ax.text(x + 0.08, y + 0.08, label, color="darkred", fontsize=11, weight="bold")

    ax.set_title(title)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.4)

    # Tự động căn khung nhìn theo dữ liệu.
    margin = 1.0
    ax.set_xlim(min(x_coords) - margin, max(x_coords) + margin)
    ax.set_ylim(min(y_coords) - margin, max(y_coords) + margin)

    return fig


def draw_parallelogram(
    fig: plt.Figure,
    ax: plt.Axes,
    points: Sequence[Sequence[float]],
    title: str = "Hình Bình Hành",
) -> plt.Figure:
    """Vẽ hình bình hành từ 4 điểm A, B, C, D."""
    return _draw_shape(fig, ax, points, title)


def draw_trapezoid(
    fig: plt.Figure,
    ax: plt.Axes,
    points: Sequence[Sequence[float]],
    title: str = "Hình Thang Cân",
) -> plt.Figure:
    """Vẽ hình thang cân từ 4 điểm A, B, C, D."""
    return _draw_shape(fig, ax, points, title)


def draw_rectangle(
    fig: plt.Figure,
    ax: plt.Axes,
    points: Sequence[Sequence[float]],
    title: str = "Hình Chữ Nhật",
) -> plt.Figure:
    """Vẽ hình chữ nhật từ 4 điểm A, B, C, D."""
    return _draw_shape(fig, ax, points, title)


def draw_rhombus(
    fig: plt.Figure,
    ax: plt.Axes,
    points: Sequence[Sequence[float]],
    title: str = "Hình Thoi",
) -> plt.Figure:
    """Vẽ hình thoi từ 4 điểm A, B, C, D."""
    return _draw_shape(fig, ax, points, title)


def draw_quadrilateral(
    fig: plt.Figure,
    ax: plt.Axes,
    points: Sequence[Sequence[float]],
    title: str = "Tứ Giác",
) -> plt.Figure:
    """Vẽ tứ giác bất kỳ từ 4 điểm A, B, C, D."""
    return _draw_shape(fig, ax, points, title)


def calculate_distance(p1: Sequence[float], p2: Sequence[float]) -> float:
    """Tính khoảng cách giữa hai điểm p1 và p2."""
    try:
        point_1 = _to_point(p1)
        point_2 = _to_point(p2)
        return float(np.hypot(point_2[0] - point_1[0], point_2[1] - point_1[1]))
    except (TypeError, ValueError, ZeroDivisionError):
        return float("nan")


def calculate_perimeter(points: Sequence[Sequence[float]]) -> float:
    """Tính chu vi tứ giác bằng tổng độ dài 4 cạnh."""
    try:
        valid_points = _validate_points(points)
        perimeter = 0.0
        for i in range(4):
            perimeter += calculate_distance(valid_points[i], valid_points[(i + 1) % 4])

        if np.isnan(perimeter):
            raise ValueError("Dữ liệu đầu vào không hợp lệ.")

        return float(perimeter)
    except (TypeError, ValueError, ZeroDivisionError):
        return float("nan")


def calculate_area_polygon(points: Sequence[Sequence[float]]) -> float:
    """Tính diện tích đa giác 4 đỉnh bằng công thức Shoelace."""
    try:
        valid_points = _validate_points(points)
        x_coords = np.array([point[0] for point in valid_points])
        y_coords = np.array([point[1] for point in valid_points])

        area = 0.5 * np.abs(
            np.dot(x_coords, np.roll(y_coords, -1))
            - np.dot(y_coords, np.roll(x_coords, -1))
        )
        return float(area)
    except (TypeError, ValueError, ZeroDivisionError):
        return float("nan")


def calculate_angle(
    p1: Sequence[float],
    vertex: Sequence[float],
    p2: Sequence[float],
) -> float:
    """Tính góc (độ) tạo bởi ba điểm theo thứ tự p1-vertex-p2."""
    try:
        point_1 = np.array(_to_point(p1), dtype=float)
        point_v = np.array(_to_point(vertex), dtype=float)
        point_2 = np.array(_to_point(p2), dtype=float)

        vector_1 = point_1 - point_v
        vector_2 = point_2 - point_v

        norm_1 = np.linalg.norm(vector_1)
        norm_2 = np.linalg.norm(vector_2)

        # Tránh chia cho 0 khi một trong hai vector có độ dài bằng 0.
        if norm_1 == 0.0 or norm_2 == 0.0:
            raise ZeroDivisionError("Không thể tính góc khi điểm trùng nhau.")

        cos_theta = float(np.dot(vector_1, vector_2) / (norm_1 * norm_2))
        cos_theta = float(np.clip(cos_theta, -1.0, 1.0))

        angle = np.degrees(np.arccos(cos_theta))
        return float(angle)
    except (TypeError, ValueError, ZeroDivisionError, FloatingPointError):
        return float("nan")
