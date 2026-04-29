FROM python:3.11-slim

WORKDIR /app

# Flush Python stdout/stderr immediately so docker logs stream in real time
ENV PYTHONUNBUFFERED=1

# gcc needed for some litellm/tokenizer native extensions
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Run as a non-root user to avoid root-owned output files on bind mounts
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID app && useradd -m -u $UID -g $GID app

# --- Dependency layer (only re-runs when pyproject.toml changes) ---
# Copy the manifest first so Docker can cache this heavy layer independently
# of source code edits.
COPY pyproject.toml .
# Read declared deps from pyproject.toml and install them (plus optional
# graph-rendering libs) without installing the package itself.
RUN python3 -c "\
import tomllib, subprocess, sys; \
d = tomllib.load(open('pyproject.toml', 'rb')); \
extras = ['networkx', 'matplotlib', 'scipy']; \
deps = d['project']['dependencies'] + extras; \
subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir'] + deps, check=True)"

# Pre-download the embedding model used by the semantic-dedup pass so cold
# starts inside the container don't have to fetch ~80 MB on first use.
# This layer is also cached independently of source changes.
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# --- Source layer (only re-runs when source files change) ---
# Pass --build-arg CACHE_BUST=$(date +%s) to force this layer to rebuild
# without touching the expensive dep/model layers above.
ARG CACHE_BUST=1
RUN echo "cache bust: $CACHE_BUST"
COPY . .
RUN pip install --no-cache-dir . --no-deps

RUN mkdir -p /app/outputs && chown -R app:app /app

USER app

# Outputs land here; mount a host directory to persist them
VOLUME ["/app/outputs"]

ENTRYPOINT ["autospectest"]
