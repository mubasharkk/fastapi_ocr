import utils.image_ocr as ocr_image
from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from typing import List
import asyncio

router = APIRouter(
    prefix='/v1/search',
    tags=['Search'],
)


@router.post("/images/{text}")
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
