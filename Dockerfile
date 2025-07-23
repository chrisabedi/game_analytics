FROM python:3.12.3-slim

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1


COPY requirements.txt /app
RUN  pip install --upgrade pip && pip install -r requirements.txt
COPY . .


EXPOSE 8000

CMD ["python","manage.py","runserver", "0.0.0.0:8000"]