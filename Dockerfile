FROM python:3.11-slim

WORKDIR /app

# 1. System dependencies (Caches perfectly)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# 2. Setup user (Caches perfectly)
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID app && useradd -m -u $UID -g $GID app

# 3. Install heavy external libraries FIRST
# Moving this up means it will only ever rebuild if you change this specific line
RUN pip install --no-cache-dir networkx matplotlib scipy

# 4. Copy ONLY the files needed to determine dependencies
# Adjust these filenames if you use requirements.txt instead of pyproject.toml/setup.py
COPY pyproject.toml setup.py* setup.cfg* ./

# 5. Install the project's dependencies
# (If your setup.py requires the source code to just run, skip this and use a requirements.txt instead:
# COPY requirements.txt . -> RUN pip install -r requirements.txt)
RUN pip install --no-cache-dir . || true 

# 6. NOW copy the rest of the source code
COPY . .

# 7. Install the actual package (this will be fast because dependencies are already cached)
RUN pip install --no-cache-dir --no-deps .

# 8. Final setup
RUN mkdir -p /app/outputs && chown -R app:app /app

USER app

VOLUME ["/app/outputs"]

ENTRYPOINT ["autospectest"]