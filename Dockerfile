# Image faster to download and to deploy
FROM python:3.11-slim

WORKDIR /app

# Better use of Docker cache, it accelerates the construction
COPY pyproject.toml ./

# Install without cache, the files during the install are not preserved 
RUN pip install uv --no-cache-dir && \ 
    uv pip install --system --no-cache -r pyproject.toml

EXPOSE 8000

# Add new location to the main in the new architecture
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
