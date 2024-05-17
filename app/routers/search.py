import modules.utils.image_ocr as ocr_image
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from typing import List
import asyncio
from middlewares.check_api_token import JWTBearer, check_api_key

router = APIRouter(
    prefix='/v1/search',
    tags=['Search'],
    dependencies=[Depends(JWTBearer()), Depends(check_api_key)]
)


@router.post("/images")
async def search_text_in_images(text: str, images: List[UploadFile] = File(...)):
    tasks = []
    for img in images:
        temp_file = ocr_image.save_file(img)
        tasks.append(asyncio.create_task(ocr_image.read_image(temp_file)))
    texts = await asyncio.gather(*tasks)
    results = []
    for i in range(len(texts)):
        if text.casefold() in texts[i].casefold():
            results.append({"search": text, text: texts[i], "file_name": images[i].filename})

    return results
