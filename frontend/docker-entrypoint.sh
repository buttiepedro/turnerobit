#!/bin/sh
set -e

PORT="${PORT:-80}"
# API_URL should be the full backend URL including /api, e.g. https://backend.up.railway.app/api
API_URL="${API_URL:-}"

echo "Frontend starting on port $PORT"

# Generate runtime env config so the browser can read the API URL without a rebuild
cat > /usr/share/nginx/html/env-config.js <<EOF
window.__API_URL__ = '${API_URL}';
EOF

sed -e "s|__PORT__|$PORT|g" \
  /etc/nginx/conf.d/app.conf.template > /etc/nginx/conf.d/default.conf

exec nginx -g "daemon off;"
