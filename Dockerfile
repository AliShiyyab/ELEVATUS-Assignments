FROM python:3.9.13-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirments.txt /code/requirments.txt
WORKDIR /code
RUN pip install -r requirments.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
