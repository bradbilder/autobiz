"""
Entry point principal do FastAPI - Autobiz
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import time
import structlog

from app.config import settings
from app.routers import (
    auth,
    onboarding,
    admin,
    dynamic_crud,
    schema,
    reports,
    integrations,
    plugins,
    webhook
)
from app.core.engine import AutoModelEngine
from app.plugins.manager import PluginManager

# Logger estruturado
logger = structlog.get_logger()

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema auto-modelável para gestão de negócios",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware de logging e timing
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log da requisição
    logger.info(
        "request_started",
        method=request.method,
        url=str(request.url),
        client=request.client.host if request.client else None,
    )
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log da resposta
        logger.info(
            "request_completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time=round(process_time, 3),
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "request_failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
            process_time=round(process_time, 3),
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Erro interno do servidor"}
        )

# Inicialização do motor auto-modelável
engine = AutoModelEngine()

# Gerenciador de plugins
plugin_manager = PluginManager()


@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação"""
    logger.info(
        "application_startup",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )
    
    # Inicializar motor auto-modelável
    await engine.initialize()
    
    # Carregar plugins
    await plugin_manager.load_all_plugins()
    
    logger.info("application_startup_complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de desligamento da aplicação"""
    logger.info("application_shutdown")
    
    # Desligar motor
    await engine.shutdown()
    
    # Descarregar plugins
    await plugin_manager.unload_all_plugins()


# Health check
@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": time.time(),
    }


# Incluir routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(onboarding.router, prefix="/api/v1/onboarding", tags=["Onboarding"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Administração Master"])
app.include_router(schema.router, prefix="/api/v1/schema", tags=["Schema Dinâmico"])
app.include_router(dynamic_crud.router, prefix="/api/v1/data", tags=["CRUD Dinâmico"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Relatórios"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["Integrações"])
app.include_router(plugins.router, prefix="/api/v1/plugins", tags=["Plugins"])
app.include_router(webhook.router, prefix="/api/v1/webhooks", tags=["Webhooks"])

# Montar arquivos estáticos
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
    )
