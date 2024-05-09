
FROM python:3.12

COPY ./requirements.txt /requirements.txt
COPY ./app /var/www/app

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        libtesseract-dev \
        tesseract-ocr-eng \
        tesseract-ocr-deu \
        tesseract-ocr-fra \
        ocrmypdf \
        libgl1 \
        make \
        gcc \
    && python3 -m pip install -r /requirements.txt

RUN export PYTHONPATH=$PWD

#WORKDIR /var/www/app

#CMD ["fastapi", "dev", "app.py", "--host", "0.0.0.0","--port", "80"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "80", "--reload"]
