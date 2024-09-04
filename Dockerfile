FROM python:3.12.0

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt
RUN python -m nltk.downloader punkt

COPY app app/

EXPOSE 5000

CMD ["python", "app/main.py"]