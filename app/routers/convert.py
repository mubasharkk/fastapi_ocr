import pytesseract
import io
import uuid
import modules.utils.image_ocr as ocr_image
import modules.utils.pdf_ocr as ocr_pdf
import modules.utils.image_preprocesing as preprocesing
from middlewares.check_api_token import JWTBearer, check_api_key
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from PIL import Image
from fastapi.responses import StreamingResponse, FileResponse
from PyPDF2 import PdfMerger, PdfReader

router = APIRouter(
    prefix='/v1/convert',
    tags=['Convert'],
    dependencies=[Depends(JWTBearer()), Depends(check_api_key)]
)


@router.post("/image/pdf")
async def convert_image_to_pdf(image: UploadFile = File(...)):
    try:
        image = Image.open(
            ocr_image.save_file(image)
        )
        pdf_pages = []
        for frame in range(image.n_frames):
            image.seek(frame)
            pdf = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', config=r'--oem 3 --psm 6')
            temp_file = f'/tmp/{uuid.uuid4()}.pdf'
            pdf_pages.append(temp_file)
            with open(temp_file, 'a+b') as f:
                f.write(pdf)

        output_file = f'/tmp/{uuid.uuid4()}.pdf'
        merger = PdfMerger()
        for pdf_page in pdf_pages:
            merger.append(PdfReader(open(pdf_page, 'rb')))

        merger.write(output_file)

        return FileResponse(path=output_file)
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
