from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
import time
import asyncio
import requests
import pytesseract
import io
from typing import List
from PIL import Image
import modules.utils.image_ocr as ocr_image
from pypdf import PdfReader
from middlewares.check_api_token import JWTBearer, check_api_key

router = APIRouter(
    prefix='/v1/extract',
    tags=['Extract'],
    dependencies=[Depends(JWTBearer()), Depends(check_api_key)]
)


@router.post("/text")
async def extract_text(images: List[UploadFile] = File(...)):
    response = {'files': {}}
    s = time.time()
    tasks = []
    for img in images:
        print("Images Uploaded: ", img.filename)
        temp_file = ocr_image.save_file(img)
        tasks.append(asyncio.create_task(ocr_image.read_image(temp_file)))
    text = await asyncio.gather(*tasks)
    for i in range(len(text)):
        response['files'][images[i].filename] = text[i]

    response["time_taken"] = round((time.time() - s), 2)

    return response


@router.post("/{language}/text")
async def extract_text_with_language(image: UploadFile = File(...), language: str = "eng"):
    temp_file = ocr_image.save_file(image)
    image = Image.open(temp_file)
    text = pytesseract.image_to_string(image, lang=language)
    return {"text": text}


@router.post("/url")
async def extract_text_from_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="Invalid image URL")
        text = ocr_image.read_image(io.BytesIO(response.content))
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post('/pdf')
async def extract_text_from_pdf(file: UploadFile = File(...)):
    temp_file = ocr_image.save_file(file)
    reader = PdfReader(temp_file)
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text())
    return {'pages': pages_text}
