from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title='Cutly',
        docs_url='/api/docs',
        description='Culty new arch',
        debug=True,
    )
    return app