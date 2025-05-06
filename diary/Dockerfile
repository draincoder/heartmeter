FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY ./common /common/
COPY ./diary/pyproject.toml /app/
COPY ./diary/uv.lock /app/

RUN uv pip install --target=/deps .

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /deps /usr/local/lib/python3.13/site-packages
COPY ./diary/src /app/src

ENV PYTHONPATH=/app/src

CMD ["python3", "-m", "diary.main"]
