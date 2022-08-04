FROM python:3.9.6

COPY . /fast-api/api

COPY requirements.txt /fast-api/api/requirements.txt
WORKDIR /fast-api/api

RUN pip install -r requirements.txt

EXPOSE 28000


CMD ["uvicorn", "main:app","--host=0.0.0.0" ,"--port","28000", "--reload"]