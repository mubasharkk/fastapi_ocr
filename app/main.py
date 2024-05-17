import uvicorn
from fastapi import FastAPI, Request, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from routers.extract import router as extract_router
from routers.convert import router as convert_router
from routers.search import router as search_router
from modules.storage.storage import Storage
from fastapi.responses import FileResponse
import botocore
from fastapi.middleware.trustedhost import TrustedHostMiddleware


app = FastAPI(
    title="FastApi OCR",
    description="",
    summary="An API for extract texts from Images and PDFs.",
    version="1.0.0",
    terms_of_service="/",
    contact={
        "name": "Mubashar Khokhar",
        "url": "http://github.com/mubasharkk",
        "email": "m.khokhar@social-gizmo.com",
    },
    openapi_tags=[
        {
            "name": "Extract",
            "description": "Extract text from images using Tesseract 5.",
        },
        {
            "name": "Search",
            "description": "Search help via OCR",
        },
        {
            "name": "Convert",
            "description": "API endpoints to convert files into requested format while applying OCR",
        },
    ]
)

# trusted_hosts = config('TRUSTED_HOSTS').split(',')
# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts=trusted_hosts
# )

app.include_router(extract_router)
app.include_router(convert_router)
app.include_router(search_router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/v1/healthcheck')
def healthcheck(request: Request):
    return {'status': 'alive', 'version': '1.0'}


@app.get("/test")
async def test(file: str):
    try:
        storage = Storage()
        return FileResponse(path=storage.s3.read(file))
    except botocore.exceptions.ClientError as ex:
        return ex.response['Error']

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
