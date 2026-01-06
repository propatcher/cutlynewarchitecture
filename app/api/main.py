from fastapi import FastAPI
from app.api.routes.users import router as user_router
def create_app() -> FastAPI:
    app = FastAPI(
        title='Cutly',
        docs_url='/docs',
        description='Cutly new arch',
        debug=True,
    )
    app.include_router(user_router)
    return app
