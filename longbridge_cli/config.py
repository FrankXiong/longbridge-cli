"""长桥 OpenAPI 配置初始化"""
import os
from pathlib import Path

import click
from longbridge.openapi import Config


def _load_dotenv() -> None:
    """从 .env 文件加载环境变量（会覆盖已有的系统环境变量）。

    查找顺序：当前工作目录 → 用户主目录。
    """
    candidates = [Path.cwd() / ".env", Path.home() / ".env"]
    for dotenv_path in candidates:
        if not dotenv_path.is_file():
            continue
        with dotenv_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    os.environ[key] = value
        break  # 找到第一个就停止


_load_dotenv()

# 下单权限控制：设置 LONGBRIDGE_TRADE_ENABLED=true 才允许 buy/sell/cancel
_TRADE_ENV_VAR = "LONGBRIDGE_TRADE_ENABLED"


def is_trade_enabled() -> bool:
    """返回是否已开启交易权限（默认关闭，只读模式）"""
    return os.environ.get(_TRADE_ENV_VAR, "").strip().lower() == "true"


def require_trade_enabled() -> None:
    """若未开启交易权限，抛出友好错误并提示配置方式"""
    if not is_trade_enabled():
        raise click.ClickException(
            "当前为只读模式，下单/撤单操作已禁用。\n"
            f"如需开启交易权限，请设置环境变量：\n"
            f"  export {_TRADE_ENV_VAR}=true\n"
            "⚠️  开启后请确保操作正确，下单指令将直接提交至长桥交易系统。"
        )


def get_config() -> Config:
    """从环境变量初始化长桥配置。

    需要设置以下环境变量：
        LONGBRIDGE_APP_KEY
        LONGBRIDGE_APP_SECRET
        LONGBRIDGE_ACCESS_TOKEN
    """
    try:
        return Config.from_apikey_env()
    except Exception as e:
        raise click.ClickException(
            "无法初始化长桥配置，请确认已设置以下环境变量：\n"
            "  LONGBRIDGE_APP_KEY\n"
            "  LONGBRIDGE_APP_SECRET\n"
            "  LONGBRIDGE_ACCESS_TOKEN\n"
            f"错误详情：{e}"
        )
