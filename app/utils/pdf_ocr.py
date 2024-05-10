import uuid
import ocrmypdf


def convert_pdfa(input_file, lang='eng'):
    output_file = f'/tmp/{uuid.uuid4()}.pdf'
    ocrmypdf.ocr(
        input_file,
        output_file,
        deskew=True,
        language=lang,
        rotate_pages=True,
        jobs=6,
        # redo_ocr=True,
        force_ocr=True,
        clean=True,
        invalidate_digital_signatures=True,
        keep_temporary_files=False,
        optimize=1,
        # skip_big=5
        # skip_text=True
    )
    return output_file
