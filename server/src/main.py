
import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from config.server_config import HOST, PORT, LOG_LEVEL, STATIC_FOLDER
from config.logging import setup_logging, get_logger
from config.database import init_database, get_db, engine

from api.routes import ALL_ROUTERS


setup_logging(log_level=LOG_LEVEL, log_dir='logs')
logger = get_logger(__name__)

app = FastAPI(
    title='Smart Doorbell System',
    description='스마트 현관 방문자 감지 시스템',
    version='1.0.0',
)

for router in ALL_ROUTERS:
    app.include_router(router)


# 임시
app.mount('/static', StaticFiles(directory=STATIC_FOLDER), name=STATIC_FOLDER)


async def startup_event():
    if not init_database():
        logger.error('Database initialization failed!')
    else:
        logger.info('Database initialized successfully')

app.add_event_handler('startup', startup_event)



@app.api_route('/', methods=['GET', 'POST'])
async def index(request: Request):
    logger.info(f'[{request.method}] index: {request.client.host}')
    return {'message': 'Smart Doorbell System API'}

@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='Smart Doorbell System API Docs'
    )

    

if __name__ == '__main__':
    uvicorn.run(
        app, 
        host=HOST, 
        port=PORT,
        log_level=LOG_LEVEL,
    )