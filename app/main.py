import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from routers.extract import router as extract_router
from routers.convert import router as convert_router
from routers.search import router as search_router

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

app.include_router(extract_router)
app.include_router(convert_router)
app.include_router(search_router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
