FROM python:3.11-alpine

WORKDIR /app

COPY . .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/app/entrypoint.sh"]