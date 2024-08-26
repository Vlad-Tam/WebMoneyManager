FROM python:3.9
LABEL authors="VladTam"

WORKDIR /WebMoneyManager

RUN mkdir -p main_service

WORKDIR /WebMoneyManager/main_service

COPY . .

RUN pip install -r requirements.txt

RUN alembic upgrade head

WORKDIR /WebMoneyManager

EXPOSE 8000

CMD ["uvicorn", "main_service.src.main:app", "--host", "0.0.0.0", "--port", "8000"]