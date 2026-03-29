FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN uv pip install --system --no-cache -r /code/requirements.txt

COPY src/ /code/src/

EXPOSE 8050

ENV PYTHONPATH=/code/src

CMD ["sh", "-c", "echo 'Container dash_app started. Waiting for PostgreSQL to initialize (15s)...'; sleep 5; \
                    echo 'Database setup in progress (10s remaining)...'; sleep 5; \
                    echo 'Finalizing connection... Starting Dash in 5s...'; sleep 2; \
                    echo '3...'; sleep 1; \
                    echo '2...'; sleep 1; \
                    echo '1...'; sleep 1; \
                    echo 'Launching Dash Application now!'; \
                    python src/app/index.py"]
