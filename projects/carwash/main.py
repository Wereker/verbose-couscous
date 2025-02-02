import uvicorn

from app.core.config import settings
from app.api import router as api_router

from create_fastapi_app import create_app
from fastapi_pagination import add_pagination

main_app = create_app(
    create_custom_static_urls=True
)

main_app.include_router(api_router)
add_pagination(main_app)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )