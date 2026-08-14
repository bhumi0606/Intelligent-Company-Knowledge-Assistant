FROM python:3.10-slim

WORKDIR /app

RUN pip install \
    "mcp==1.29.0" \
    "open_meteo_mcp[auth]==0.2.0"

EXPOSE 8080

CMD ["python", "-m", "open_meteo_mcp", "--mode", "streamable-http"]