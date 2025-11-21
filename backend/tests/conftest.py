"""
Pytest configuration helpers for backend tests.

- Ensures the backend package (`app`) is importable when tests run directly
  from the `backend` directory.
- Provides a compatibility shim so FastAPI's TestClient continues to work
  even when an httpx version without the legacy `app=` parameter is installed.
"""

from __future__ import annotations

import inspect
import os
import sys
from pathlib import Path

import pytest

import httpx

# Ensure repository root is on sys.path so `import app` works in tests.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def _patch_httpx_for_testclient() -> None:
    """
    Patch httpx.Client.__init__ to accept the legacy `app=` keyword.

    FastAPI/Starlette's TestClient (up to FastAPI 0.104) still passes `app=`
    into httpx.Client. Newer httpx releases removed that argument which breaks
    the tests when developers have a newer httpx installed globally.
    This shim reintroduces the keyword purely for the test process.
    """

    init_sig = inspect.signature(httpx.Client.__init__)
    if "app" in init_sig.parameters:
        # Environment already provides the legacy-compatible signature.
        return

    original_init = httpx.Client.__init__

    def patched_init(self, *args, app=None, **kwargs):  # type: ignore[override]
        if app is not None and "transport" not in kwargs:
            kwargs["transport"] = httpx.ASGITransport(app=app)
        return original_init(self, *args, **kwargs)

    httpx.Client.__init__ = patched_init  # type: ignore[assignment]


_patch_httpx_for_testclient()


def pytest_configure(config):  # noqa: D401
    """Pytest hook to ensure the shim is applied even if httpx is reloaded."""
    _patch_httpx_for_testclient()


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """
    Reset SlowAPI's in-memory limiter between tests.

    Tests invoke the same FastAPI app instance repeatedly which causes request
    counts to persist across test cases. Resetting the limiter avoids false
    positives caused by earlier tests exhausting shared buckets.
    """

    from main import app

    limiter = getattr(app.state, "limiter", None)
    if limiter is not None and hasattr(limiter, "reset"):
        limiter.reset()
    yield


