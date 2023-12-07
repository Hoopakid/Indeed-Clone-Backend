FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Install build dependencies
RUN apk add --no-cache gcc musl-dev

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
