FROM python:3.9
LABEL authors="VladTam"

WORKDIR /WebMoneyManager/main_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["alembic", "upgrade", "head"]

WORKDIR /WebMoneyManager

CMD ["uvicorn", "main_service.src.main:app", "--host", "0.0.0.0", "--port", "8000"]