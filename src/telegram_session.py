from __future__ import annotations

import logging

from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

logger = logging.getLogger(__name__)


def create_telegram_aiohttp_session(proxy_url: str | None) -> AiohttpSession:

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
