from typing import Any


def success_response(
        data: Any = None,
        message: str = "操作成功",
        code: int = 200
) -> dict:
    """
    成功响应
    """
    return {
        "code": code,
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
        message: str = "操作失败",
        code: int = 500,
        data: Any = None
) -> dict:
    """
    错误响应
    """
    return {
        "code": code,
        "success": False,
        "message": message,
        "data": data
    }
