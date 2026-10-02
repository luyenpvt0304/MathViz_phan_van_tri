# -*- coding: utf-8 -*-
"""Giải thích tĩnh cho các hình học lớp 8."""

from __future__ import annotations

from typing import Any, Dict, List

EXPLANATIONS: Dict[str, Dict[str, Any]] = {
    "Tứ giác": {
        "định_nghĩa": (
            "Tứ giác là hình gồm 4 đoạn thẳng nối 4 điểm phân biệt, "
            "trong đó hai đoạn liên tiếp không thẳng hàng. "
            "Tổng bốn góc trong của một tứ giác luôn bằng 360°."
        ),
        "tính_chất": [
            "Có 4 cạnh: AB, BC, CD, DA và 4 đỉnh: A, B, C, D",
            "Có 2 đường chéo: AC và BD",
            "Tổng các góc trong: ∠A + ∠B + ∠C + ∠D = 360°",
            "Có thể có cạnh song song (∥) hoặc vuông góc (⊥) tùy từng loại",
            "Là hình cơ bản để tạo nên nhiều dạng đặc biệt khác",
        ],
        "công_thức": {
            "diện_tích": "S = 1/2 |x1y2 + x2y3 + x3y4 + x4y1 - (y1x2 + y2x3 + y3x4 + y4x1)|",
            "chu_vi": "P = AB + BC + CD + DA",
        },
        "ví_dụ": "Hình ABCD có AB = 4 cm, BC = 5 cm, CD = 3 cm, DA = 6 cm là một tứ giác.",
    },
    "Hình thang cân": {
        "định_nghĩa": (
            "Hình thang cân là hình thang có hai cạnh bên bằng nhau. "
            "Trong hình thang cân, hai cạnh đáy song song với nhau và "
            "hai góc kề một đáy bằng nhau."
        ),
        "tính_chất": [
            "Hai đáy song song: AB ∥ CD",
            "Hai cạnh bên bằng nhau: AD = BC",
            "Hai góc kề một đáy bằng nhau: ∠A = ∠B, ∠C = ∠D",
            "Hai đường chéo bằng nhau: AC = BD",
            "Có trục đối xứng đi qua trung điểm hai đáy và ⊥ với hai đáy",
        ],
        "công_thức": {
            "diện_tích": "S = ((a + b) x h) / 2 (a, b là độ dài hai đáy)",
            "chu_vi": "P = a + b + 2c (c là cạnh bên)",
        },
        "ví_dụ": "Hình thang cân ABCD có AB ∥ CD, AB = 8 cm, CD = 4 cm, AD = BC = 5 cm.",
    },
    "Hình bình hành": {
        "định_nghĩa": (
            "Hình bình hành là tứ giác có hai cặp cạnh đối song song. "
            "Vì các cạnh đối song song nên các cạnh đối cũng bằng nhau. "
            "Đây là dạng tứ giác rất thường gặp trong thực tế."
        ),
        "tính_chất": [
            "Cạnh đối song song và bằng nhau: AB ∥ CD, AD ∥ BC, AB = CD, AD = BC",
            "Góc đối bằng nhau: ∠A = ∠C, ∠B = ∠D",
            "Hai góc kề một cạnh bất kỳ thì bù nhau: ∠A + ∠B = 180°",
            "Hai đường chéo cắt nhau tại trung điểm mỗi đường",
            "Có thể xem là hình thang có thêm một cặp cạnh đối song song",
        ],
        "công_thức": {
            "diện_tích": "S = a x h (a là cạnh đáy, h là chiều cao tương ứng)",
            "chu_vi": "P = 2(a + b)",
        },
        "ví_dụ": "Hình ABCD có AB = 5 cm, AD = 3 cm, AB ∥ CD, AD ∥ BC là hình bình hành.",
    },
    "Hình chữ nhật": {
        "định_nghĩa": (
            "Hình chữ nhật là hình bình hành có một góc vuông. "
            "Khi một góc bằng 90° thì bốn góc đều vuông. "
            "Vì vậy hình chữ nhật có hai cặp cạnh đối song song và bằng nhau."
        ),
        "tính_chất": [
            "Bốn góc vuông: ∠A = ∠B = ∠C = ∠D = 90°",
            "Cạnh đối song song và bằng nhau: AB ∥ CD, AD ∥ BC, AB = CD, AD = BC",
            "Hai đường chéo bằng nhau: AC = BD",
            "Hai đường chéo cắt nhau tại trung điểm mỗi đường",
            "Hai cạnh kề vuông góc: AB ⊥ BC",
        ],
        "công_thức": {
            "diện_tích": "S = a x b (a là chiều dài, b là chiều rộng)",
            "chu_vi": "P = 2(a + b)",
        },
        "ví_dụ": "Hình chữ nhật ABCD có AB = 7 cm, BC = 4 cm, mỗi góc đều bằng 90°.",
    },
    "Hình thoi": {
        "định_nghĩa": (
            "Hình thoi là hình bình hành có bốn cạnh bằng nhau. "
            "Ngoài tính chất của hình bình hành, hình thoi có thêm "
            "tính chất đặc biệt về hai đường chéo."
        ),
        "tính_chất": [
            "Bốn cạnh bằng nhau: AB = BC = CD = DA",
            "Cạnh đối song song: AB ∥ CD, AD ∥ BC",
            "Góc đối bằng nhau: ∠A = ∠C, ∠B = ∠D",
            "Hai đường chéo vuông góc: AC ⊥ BD",
            "Hai đường chéo là phân giác các góc của hình thoi",
        ],
        "công_thức": {
            "diện_tích": "S = (d1 x d2) / 2 (d1, d2 là hai đường chéo)",
            "chu_vi": "P = 4a",
        },
        "ví_dụ": "Hình thoi ABCD có AB = BC = CD = DA = 5 cm và AC ⊥ BD.",
    },
}


def get_explanation(shape_name: str) -> Dict[str, Any]:
    """Lấy giải thích đầy đủ của một hình theo tên."""
    return EXPLANATIONS.get(shape_name, {})


def get_definition(shape_name: str) -> str:
    """Lấy định nghĩa của hình theo tên."""
    return str(EXPLANATIONS.get(shape_name, {}).get("định_nghĩa", ""))


def get_properties(shape_name: str) -> List[str]:
    """Lấy danh sách tính chất của hình theo tên."""
    properties = EXPLANATIONS.get(shape_name, {}).get("tính_chất", [])
    return list(properties) if isinstance(properties, list) else []
