from __future__ import annotations

import json
import logging
import threading

from pathlib import Path


logger = logging.getLogger(__name__)

_cache_lock = threading.Lock()


CACHE_FILE = (Path("cache") / "architecture_cache.json")
ARCH_CACHE_VERSION = 9

_cache: dict[str,list[str]] = {}
_loaded = False


def load_cache():

    global _loaded

    if _loaded:

        return
    
    with _cache_lock:

        if _loaded:

            return

        if CACHE_FILE.exists():

            try:

                _cache.update(json.loads(CACHE_FILE.read_text( encoding="utf-8")))

                logger.info("Architecture cache loaded=%s", len(_cache))

            except Exception:

                logger.exception("Cache load failed")
        
        _loaded = True


def get_cached(query:str)->list[str]|None:

    load_cache()

    return _cache.get(query.lower().strip())


def save_cached(query:str, entities:list[str]):

    load_cache()

    key = (query.lower().strip())

    with _cache_lock:

        _cache[key] = entities

        CACHE_FILE.parent.mkdir(exist_ok=True)

        CACHE_FILE.write_text(

            json.dumps(_cache, indent=2), encoding="utf-8")

    logger.info("Architecture cache saved=%s", key)

