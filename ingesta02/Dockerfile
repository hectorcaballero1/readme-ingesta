FROM python:3.12-slim

RUN pip install uv --quiet

WORKDIR /app
COPY pyproject.toml .
RUN uv sync

COPY main.py .

CMD ["uv", "run", "python", "main.py"]
