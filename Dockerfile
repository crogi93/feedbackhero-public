FROM python:3.8-alpine as builder

RUN apk add \
  build-base

COPY requirements.txt ./
RUN pip install --user --requirement requirements.txt

FROM python:3.8-alpine

WORKDIR /app

COPY --from=builder /root/.local /root/.local/

COPY manage.py ./
COPY core ./core
COPY feedbackhero ./feedbackhero

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py" , "runserver" , "0.0.0.0:8000"]
