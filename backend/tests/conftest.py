"""
Pytest fixtures. API keys must exist before importing app.config (Config reads env at import time).
"""

from __future__ import annotations

import os

import pytest

# Ensure keys before any `app` import (Config class body reads os.environ)
if not os.environ.get("LLM_API_KEY"):
    os.environ["LLM_API_KEY"] = "test-llm-key"
if not os.environ.get("ZEP_API_KEY"):
    os.environ["ZEP_API_KEY"] = "test-zep-key"

from app import create_app


@pytest.fixture
def app():
    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()
