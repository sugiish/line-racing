FROM python:3.12.2-slim

RUN apt update && apt install -y curl
RUN pip install --no-cache-dir fastapi uvicorn numpy

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
