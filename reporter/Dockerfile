FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/

RUN uv pip install --target=/deps .

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /deps /usr/local/lib/python3.13/site-packages
COPY src /app/src

ENV PYTHONPATH=/app/src

CMD ["python3", "-m", "reporter.main"]
