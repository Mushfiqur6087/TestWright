FROM python:3.11-slim

WORKDIR /app

# gcc needed for some litellm/tokenizer native extensions
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Run as a non-root user to avoid root-owned output files on bind mounts
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID app && useradd -m -u $UID -g $GID app

# ── Dependency layer ────────────────────────────────────────────────────────
# Copy only pyproject.toml so this layer is invalidated when deps change
# but NOT when source code changes.
COPY pyproject.toml .

# Extract [project.dependencies] from pyproject.toml and install them.
# tomllib is in the Python 3.11 stdlib — no extra install needed.
RUN python3 -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); open('/tmp/req.txt','w').write('\n'.join(d['project']['dependencies']))" \
    && pip install --no-cache-dir -r /tmp/req.txt

# ── Source layer ────────────────────────────────────────────────────────────
# Changing source code only re-runs this fast --no-deps install, not the pip above.
COPY . .
RUN pip install --no-cache-dir --no-deps .

RUN mkdir -p /app/outputs && chown -R app:app /app

USER app

# Outputs land here; mount a host directory to persist them
VOLUME ["/app/outputs"]

ENTRYPOINT ["autospectest"]
