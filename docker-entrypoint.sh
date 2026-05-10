#!/bin/sh
set -e
mkdir -p /app/outputs/.checkpoints
chown app:app /app/outputs /app/outputs/.checkpoints 2>/dev/null || true
exec gosu app autospectest "$@"
