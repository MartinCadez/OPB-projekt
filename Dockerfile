FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN uv pip install --system --no-cache -r /code/requirements.txt

COPY src/ /code/src/

# COPY assets/ /code/assets/

EXPOSE 8050

ENV PYTHONPATH=/code/src

CMD ["python", "src/index.py"]
