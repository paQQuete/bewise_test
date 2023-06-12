import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import questions, auth, files
from core.config import SETTINGS
from core.logger import LOGGING


app = FastAPI(
    title=SETTINGS.PROJECT.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,

)

app.include_router(questions.router, prefix='/api/v1/questions', tags=['questions'])
app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(files.router, prefix='/api/v1/files', tags=['files'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=9000,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
