FROM python:3.9
LABEL authors="VladTam"

WORKDIR /WebMoneyManager

RUN mkdir -p currency_service

WORKDIR /WebMoneyManager/currency_service

COPY . .

RUN pip install -r requirements.txt

RUN alembic upgrade head

WORKDIR /WebMoneyManager

EXPOSE 8001

CMD ["uvicorn", "currency_service.src.main:app", "--host", "0.0.0.0", "--port", "8001"]