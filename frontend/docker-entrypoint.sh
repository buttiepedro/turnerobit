#!/bin/sh
set -e

PORT="${PORT:-80}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

# Strip trailing slash from BACKEND_URL
BACKEND_URL="${BACKEND_URL%/}"

echo "Frontend starting on port $PORT"
echo "Proxying /api/ -> $BACKEND_URL/api/"

sed \
  -e "s|__PORT__|$PORT|g" \
  -e "s|__BACKEND_URL__|$BACKEND_URL|g" \
  /etc/nginx/conf.d/app.conf.template > /etc/nginx/conf.d/default.conf

exec nginx -g "daemon off;"
