FROM python:3.11-slim

WORKDIR /app

# gcc needed for some litellm/tokenizer native extensions
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Run as a non-root user to avoid root-owned output files on bind mounts
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID app && useradd -m -u $UID -g $GID app

COPY . .

# Install AutoSpecTest and optional graph-rendering libs
RUN pip install --no-cache-dir . && \
    pip install --no-cache-dir networkx matplotlib scipy

RUN mkdir -p /app/outputs && chown -R app:app /app

USER app

# Outputs land here; mount a host directory to persist them
VOLUME ["/app/outputs"]

ENTRYPOINT ["autospectest"]
