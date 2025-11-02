FROM python:3.12-bookworm

RUN pip install playwright==1.55.0 && \
    playwright install --with-deps

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]