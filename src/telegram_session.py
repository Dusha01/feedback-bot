from __future__ import annotations

import logging
from typing import Optional
from aiohttp_socks import ProxyConnector
from aiogram.client.session.aiohttp import AiohttpSession

logger = logging.getLogger(__name__)


def create_telegram_aiohttp_session(proxy_url: Optional[str]) -> AiohttpSession:

    raw = (proxy_url or "").strip()
    if not raw:
        return AiohttpSession()

    low = raw.lower()
    if low.startswith("socks5://") or low.startswith("socks4://"):
        
        connector = ProxyConnector.from_url(raw)
        logger.info("Telegram API: используется SOCKS-прокси")
        return AiohttpSession(connector=connector)

    logger.info("Telegram API: используется HTTP(S)-прокси")
    return AiohttpSession(proxy=raw)
