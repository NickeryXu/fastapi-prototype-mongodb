from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import fastapi_plugins

from app.core.errors import http_error_handler, http422_error_handler, catch_exceptions_middleware
from app.api import router as api_router
from app.core.config import allowed_hosts, api_key, debug, version, host, port, project_name
from app.db.mongodb import connect_to_mongodb, close_mongo_connection
from app.db.redis import redis_config

app = FastAPI(title=project_name, debug=debug, version=version)

# 普通异常全局捕获
app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongo_connection)


@app.on_event('startup')
async def startup() -> None:
    await fastapi_plugins.redis_plugin.init_app(app, config=redis_config)
    await fastapi_plugins.redis_plugin.init()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await fastapi_plugins.redis_plugin.terminate()


app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

app.include_router(api_router, prefix=api_key)

if __name__ == '__main__':
    uvicorn.run(
        "app.app:app",
        host=host,
        port=port,
        reload=True,
        workers=1
    )
