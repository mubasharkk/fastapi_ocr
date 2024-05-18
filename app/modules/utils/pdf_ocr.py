import uuid
import ocrmypdf


def convert_pdfa(input_file: str, lang: str = 'eng', force_ocr: bool = True, skip_text: bool = True) -> str:
    output_file = f'/tmp/{uuid.uuid4()}.pdf'
    ocrmypdf.ocr(
        input_file,
        output_file,
        deskew=True,
        language=lang,
        rotate_pages=True,
        jobs=6,
        # redo_ocr=True,
        force_ocr=force_ocr,
        clean=True,
        invalidate_digital_signatures=True,
        keep_temporary_files=False,
        optimize=1,
        # skip_big=5
        skip_text=skip_text
    )
    return output_file


def perform_ocr_on_storage_file(key: str, bucket: str):
    return key
