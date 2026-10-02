# -*- coding: utf-8 -*-
"""Tiện ích gọi Gemini API cho ứng dụng hình học lớp 8."""

from __future__ import annotations

import json
import time
from functools import lru_cache
from typing import Any, Dict, List, Optional, Sequence

try:
    from google import genai
except ImportError:
    genai = None
import streamlit as st

MODEL_NAME = "gemini-2.5-flash"
MODEL_CANDIDATES = (
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
)
CACHE_TTL = 3600  # Cache 1 giờ


# Các câu trả lời dự phòng để ứng dụng không bị crash khi API lỗi.
FALLBACK_EXPLANATION = (
    "Hiện tại chưa lấy được giải thích từ AI. "
    "Bạn hãy thử lại sau hoặc kiểm tra API key."
)
FALLBACK_DEFINITION = (
    "Hiện tại chưa lấy được định nghĩa từ AI. "
    "Bạn vui lòng kiểm tra kết nối API và thử lại."
)
FALLBACK_PROPERTIES = [
    "Hiện tại chưa lấy được danh sách tính chất từ AI.",
    "Bạn hãy thử lại sau.",
]


def _current_cache_bucket() -> int:
    """Trả về mốc thời gian cache theo từng giờ để giả lập TTL với lru_cache."""
    return int(time.time() // CACHE_TTL)


def _get_api_key_from_app() -> str:
    """Lấy API key từ Streamlit secrets hoặc session_state (nếu có)."""
    api_key = ""

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        # Một số môi trường local không cấu hình secrets.
        api_key = ""

    if not api_key:
        api_key = str(st.session_state.get("api_key", "")).strip()

    return str(api_key).strip()


def _normalize_model_name(name: str) -> str:
    """Chuẩn hóa tên model từ API (có thể có tiền tố models/)."""
    normalized = str(name).strip()
    if normalized.startswith("models/"):
        return normalized.split("/", 1)[1]
    return normalized


def _is_text_generation_model(model_name: str) -> bool:
    """Lọc model text tránh audio/image/transcribe/embedding/live."""
    lowered = model_name.lower()
    blocked_keywords = ("image", "audio", "tts", "transcribe", "embedding", "live")
    return not any(keyword in lowered for keyword in blocked_keywords)


@lru_cache(maxsize=32)
def _discover_available_models(api_key: str, cache_bucket: int) -> tuple[str, ...]:
    """Lấy danh sách model khả dụng cho key hiện tại, ưu tiên text flash."""
    del cache_bucket

    if genai is None:
        return tuple(MODEL_CANDIDATES)

    discovered: List[str] = []

    try:
        client = genai.Client(api_key=str(api_key).strip())
        for model in client.models.list():
            raw_name = getattr(model, "name", "")
            model_name = _normalize_model_name(raw_name)
            if not model_name or not _is_text_generation_model(model_name):
                continue

            # Một số phiên bản SDK trả về supported_actions, một số khác có thể không có field này.
            supported_actions: Sequence[str] = getattr(model, "supported_actions", ()) or ()
            supports_generate_content = any(
                str(action).lower() == "generatecontent"
                for action in supported_actions
            )

            if supported_actions and not supports_generate_content:
                continue

            discovered.append(model_name)
    except Exception as exc:
        print(f"Cảnh báo: Không lấy được danh sách model từ API: {exc}")
        return tuple(MODEL_CANDIDATES)

    if not discovered:
        return tuple(MODEL_CANDIDATES)

    unique_discovered = list(dict.fromkeys(discovered))
    prioritized: List[str] = [
        model for model in MODEL_CANDIDATES if model in unique_discovered
    ]
    prioritized.extend(
        model for model in unique_discovered if model not in prioritized
    )

    return tuple(prioritized)


def _safe_generate(prompt: str, api_key: str) -> Optional[str]:
    """Gọi Gemini an toàn, lỗi thì trả về None và in cảnh báo."""
    if genai is None:
        print("Cảnh báo: Thiếu thư viện google-genai.")
        return None

    if not api_key:
        print("Cảnh báo: Chưa có API key Gemini.")
        return None

    try:
        if not configure_gemini(api_key):
            print("Cảnh báo: Không cấu hình được Gemini API.")
            return None

        client = genai.Client(api_key=str(api_key).strip())
        available_models = _discover_available_models(api_key, _current_cache_bucket())
        for model_name in available_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "automatic_function_calling": {"disable": True},
                    },
                )
                text = getattr(response, "text", "")

                if text and str(text).strip():
                    return str(text).strip()

                print(f"Cảnh báo: Gemini trả về dữ liệu rỗng với model {model_name}.")
            except Exception as model_exc:
                error_text = str(model_exc).lower()
                if "not found" in error_text or "not supported" in error_text or "404" in error_text:
                    print(f"Cảnh báo: Model {model_name} không khả dụng, thử model khác.")
                    continue

                print(f"Cảnh báo: Lỗi khi gọi model {model_name}: {model_exc}")
                return None

            print(
                "Cảnh báo: Không model Gemini text nào khả dụng cho generate_content với API key hiện tại."
            )
        return None
    except Exception as exc:
        print(f"Cảnh báo: Lỗi khi gọi Gemini API: {exc}")
        return None


def configure_gemini(api_key: str) -> bool:
    """Cấu hình Gemini API bằng API key, thành công trả về True."""
    try:
        if genai is None:
            print("Cảnh báo: Chưa cài thư viện google-genai.")
            return False

        if not api_key or not str(api_key).strip():
            print("Cảnh báo: API key rỗng.")
            return False

        # SDK mới dùng client theo từng request, không còn cấu hình global.
        _ = genai.Client(api_key=str(api_key).strip())
        return True
    except Exception as exc:
        print(f"Cảnh báo: Không cấu hình được Gemini API: {exc}")
        return False


def test_api_connection(api_key: str) -> bool:
    """Kiểm tra kết nối Gemini API bằng prompt đơn giản 'Xin chào'."""
    try:
        if genai is None:
            print("Cảnh báo: Thiếu thư viện google-genai.")
            return False

        if not configure_gemini(api_key):
            return False

        text = _safe_generate("Xin chào", api_key)
        return bool(text and str(text).strip())
    except Exception as exc:
        print(f"Cảnh báo: Kiểm tra kết nối API thất bại: {exc}")
        return False


@lru_cache(maxsize=256)
def _cached_explanation(
    shape_name: str,
    properties_json: str,
    api_key: str,
    cache_bucket: int,
) -> str:
    """Sinh giải thích có cache theo lru_cache và mốc thời gian."""
    del cache_bucket  # Biến chỉ dùng để làm key cache theo giờ.

    properties_text = properties_json
    try:
        properties_obj = json.loads(properties_json)
        if isinstance(properties_obj, dict):
            properties_text = ", ".join(
                f"{key}: {value}" for key, value in properties_obj.items()
            )
    except Exception:
        properties_text = properties_json

    prompt = (
        f"Bạn là giáo viên toán lớp 8. Giải thích ngắn gọn (3-4 câu) về: {shape_name}\n"
        f"Tính chất: {properties_text}\n"
        "- Dùng từ đơn giản\n"
        "- Dễ hiểu\n"
        "- Có ví dụ cụ thể\n"
        "- Tiếng Việt"
    )

    ai_text = _safe_generate(prompt, api_key)
    if ai_text:
        return ai_text

    # Fallback đúng yêu cầu prompt tổng quát.
    return (
        f"Giải thích về {shape_name} có: {properties_text}. "
        f"{FALLBACK_EXPLANATION}"
    )


def get_explanation(shape_name: str, properties: Dict[str, Any]) -> str:
    """Lấy giải thích ngắn gọn bằng tiếng Việt cho hình học và tính chất."""
    api_key = _get_api_key_from_app()
    if not api_key:
        return "Cần API key"

    try:
        properties_json = json.dumps(properties, ensure_ascii=False, sort_keys=True)
    except Exception:
        properties_json = str(properties)

    return _cached_explanation(
        shape_name=str(shape_name).strip(),
        properties_json=properties_json,
        api_key=api_key,
        cache_bucket=_current_cache_bucket(),
    )


@lru_cache(maxsize=256)
def _cached_definition(shape_name: str, api_key: str, cache_bucket: int) -> str:
    """Lấy định nghĩa 2-3 câu cho hình học, có cache theo giờ."""
    del cache_bucket

    prompt = (
        f"Bạn là giáo viên toán lớp 8. Hãy nêu định nghĩa ngắn gọn (2-3 câu) cho {shape_name}. "
        "Dùng ngôn ngữ đơn giản, dễ hiểu, tiếng Việt."
    )

    ai_text = _safe_generate(prompt, api_key)
    if ai_text:
        return ai_text

    return f"Định nghĩa của {shape_name}: {FALLBACK_DEFINITION}"


def get_definition(shape_name: str) -> str:
    """Trả về định nghĩa ngắn gọn (2-3 câu) cho tên hình."""
    api_key = _get_api_key_from_app()
    if not api_key:
        return "Cần API key"

    return _cached_definition(
        shape_name=str(shape_name).strip(),
        api_key=api_key,
        cache_bucket=_current_cache_bucket(),
    )


@lru_cache(maxsize=256)
def _cached_properties_list(shape_name: str, api_key: str, cache_bucket: int) -> tuple[str, ...]:
    """Lấy danh sách tính chất dạng list string, có cache theo giờ."""
    del cache_bucket

    prompt = (
        f"Bạn là giáo viên toán lớp 8. Liệt kê các tính chất quan trọng của {shape_name}.\n"
        "Yêu cầu:\n"
        "- Chỉ trả về danh sách ngắn\n"
        "- Mỗi dòng một tính chất\n"
        "- Dùng tiếng Việt đơn giản"
    )

    ai_text = _safe_generate(prompt, api_key)
    if not ai_text:
        return tuple(FALLBACK_PROPERTIES)

    lines = [line.strip("-• \t") for line in ai_text.splitlines()]
    clean_lines = [line for line in lines if line]

    if not clean_lines:
        return tuple(FALLBACK_PROPERTIES)

    return tuple(clean_lines)


def get_properties_list(shape_name: str) -> List[str]:
    """Trả về danh sách tính chất của hình dưới dạng list các chuỗi."""
    api_key = _get_api_key_from_app()
    if not api_key:
        return ["Cần API key"]

    return list(
        _cached_properties_list(
            shape_name=str(shape_name).strip(),
            api_key=api_key,
            cache_bucket=_current_cache_bucket(),
        )
    )


def get_properties(shape_name: str) -> List[str]:
    """Alias cho get_properties_list()."""
    return get_properties_list(shape_name)
