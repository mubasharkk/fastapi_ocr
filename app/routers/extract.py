import utils.image_ocr as ocr_image
import time
import asyncio
import requests
import pytesseract
import io

from typing import List
from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from PIL import Image

router = APIRouter(
    prefix='/v1/extract',
    tags=['Extract']
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
        image = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))