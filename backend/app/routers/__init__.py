"""
Routers da API Autobiz
"""
from .auth import router as auth_router
from .onboarding import router as onboarding_router
from .admin import router as admin_router
from .dynamic_crud import router as dynamic_crud_router
from .schema import router as schema_router
from .reports import router as reports_router
from .integrations import router as integrations_router
from .plugins import router as plugins_router
from .webhook import router as webhook_router

__all__ = [
    "auth_router",
    "onboarding_router",
    "admin_router",
    "dynamic_crud_router",
    "schema_router",
    "reports_router",
    "integrations_router",
    "plugins_router",
    "webhook_router",
]
