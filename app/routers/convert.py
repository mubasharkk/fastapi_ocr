import pytesseract
import io
import uuid
import modules.utils.image_ocr as ocr_image
import modules.utils.pdf_ocr as ocr_pdf
import modules.utils.image_preprocesing as preprocesing

from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from PIL import Image
from fastapi.responses import StreamingResponse, FileResponse

router = APIRouter(
    prefix='/v1/convert',
    tags=['Convert']
)


@router.post("/image/pdf")
async def convert_image_to_pdf(image: UploadFile = File(...)):
    try:
        temp_file = ocr_image.save_file(image)
        pdf = pytesseract.image_to_pdf_or_hocr(Image.open(temp_file), extension='pdf')
        temp_file = f'/tmp/{uuid.uuid4()}.pdf'
        with open(temp_file, 'w+b') as f:
            f.write(pdf)
        return FileResponse(path=temp_file)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/pdf/ocr")
async def convert_pdf_to_pdfa(file: UploadFile = File(...)):
    try:
        temp_file = ocr_image.save_file(file)
        pdf = ocr_pdf.convert_pdfa(temp_file)
        return FileResponse(path=pdf)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/image-bounding-boxes")
async def convert_image_with_bounding_boxes(image: UploadFile = File(...)):
    temp_file = ocr_image.save_file(image)
    img = preprocesing.get_image_with_bounding_boxes(temp_file)
    img_pil = Image.fromarray(img)
    # Save the image to a BytesIO object
    img_bytes = io.BytesIO()
    img_pil.save(img_bytes, format='JPEG')
    # Set the pointer to the beginning of the BytesIO object
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type='image/jpeg')
