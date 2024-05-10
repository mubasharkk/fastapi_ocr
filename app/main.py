import asyncio
import io
import time
import uuid
from typing import List
import pytesseract
import requests
import uvicorn
from PIL import Image
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates

import utils.image_ocr as ocr_image
import utils.image_preprocesing as preprocesing
import utils.pdf_ocr as ocr_pdf

description=""
tags_metadata = [
    {
        "name": "Extractions",
        "description": "Extract text from images using Tesseract 5.",
    },
    {
        "name": "Search",
        "description": "Search help via OCR",
    },
    {
        "name": "Conversions",
        "description": "API endpoints to convert files into requested format while applying OCR",
    },
]

app = FastAPI(
    title="FastApi OCR",
    description=description,
    summary="An API for extract texts from Images and PDFs.",
    version="1.0.0",
    terms_of_service="/",
    contact={
        "name": "Mubashar Khokhar",
        "url": "http://github.com/mubasharkk",
        "email": "m.khokhar@social-gizmo.com",
    },
    openapi_tags=tags_metadata
)

templates = Jinja2Templates(directory="templates")


@app.get("/", tags=['Extractions'])
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/extract/text", tags=['Extractions'])
async def perform_ocr(image: UploadFile = File(...)):
    temp_file = ocr_image.save_file(image)
    text = await ocr_image.read_image(temp_file)
    return {"filename": image.filename, "text": text}


@app.post("/extract/multitext", tags=['Extractions'])
async def extract_text(Images: List[UploadFile] = File(...)):
    response = {}
    s = time.time()
    tasks = []
    for img in Images:
        print("Images Uploaded: ", img.filename)
        temp_file = ocr_image.save_file(img)
        tasks.append(asyncio.create_task(ocr_image.read_image(temp_file)))
    text = await asyncio.gather(*tasks)
    for i in range(len(text)):
        response[Images[i].filename] = text[i]
    response["Time Taken"] = round((time.time() - s), 2)

    return response


@app.post("/extract/{language}/text", tags=['Extractions'])
async def extract_text_with_language(image: UploadFile = File(...), language: str = "eng"):
    temp_file = ocr_image.save_file(image)
    image = Image.open(temp_file)
    text = pytesseract.image_to_string(image, lang=language)
    return {"text": text}


@app.post("/extract/url", tags=['Extractions'])
async def extract_text_from_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="Invalid image URL")
        image = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/convert/image/text", tags=['Conversions'])
async def post_image_to_text(file: UploadFile = File(...)):
    img = await pytesseract.image_to_pdf_or_hocr(file, HTTPException(status_code=422, detail="Invalid image"))

    ocr_predictions: str = ocr_image.apply_ocr(img)
    print(ocr_predictions)
    return {
        "results": {
            "raw": ocr_predictions,
            "cleaned": ocr_predictions.replace("\n", " ").strip(),
            "lines": ocr_predictions.split("\n"),
        }
    }


@app.post("/convert/image/pdf", tags=['Conversions'])
async def post_image_to_pdf(image: UploadFile = File(...)):
    try:
        temp_file = ocr_image.save_file(image)
        pdf = pytesseract.image_to_pdf_or_hocr(Image.open(temp_file), extension='pdf')
        temp_file = f'/tmp/{uuid.uuid4()}.pdf'
        with open(temp_file, 'w+b') as f:
            f.write(pdf)
        return FileResponse(path=temp_file)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/convert/pdf/ocr", tags=['Conversions'])
async def post_image_to_pdf(file: UploadFile = File(...)):
    try:
        temp_file = ocr_image.save_file(file)
        pdf = ocr_pdf.convert_pdfa(temp_file)
        return FileResponse(path=pdf)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/convert/image", tags=['Conversions'])
async def post_image_with_bounding_boxes(image: UploadFile = File(...)):
    temp_file = ocr_image.save_file(image)
    img = preprocesing.get_image_with_bounding_boxes(temp_file)
    img_pil = Image.fromarray(img)
    # Save the image to a BytesIO object
    img_bytes = io.BytesIO()
    img_pil.save(img_bytes, format='JPEG')
    # Set the pointer to the beginning of the BytesIO object
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type='image/jpeg')


@app.post("/search/images/{text}", tags=['Search'])
async def search_text_in_images(text_to_search: str, images: List[UploadFile] = File(...)):
    tasks = []
    for img in images:
        temp_file = ocr_image.save_file(img)
        tasks.append(asyncio.create_task(ocr_image.read_image(temp_file)))
    texts = await asyncio.gather(*tasks)
    for i in range(len(texts)):
        if text_to_search in texts[i]:
            return {"status": "found", "text": text_to_search, "file_name": images[i].filename}
    return {"status": "not found", "text": text_to_search}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
