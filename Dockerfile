FROM python:3.14-slim

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 808

COPY . .

CMD ["uvicorn", "api.main:app","--host" , "0.0.0.0","--port", "8080"]
