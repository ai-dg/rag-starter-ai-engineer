FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv pip install --system -r pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
