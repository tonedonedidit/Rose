#!/bin/sh
# Usage: ./set-domain.sh stoneandrose.com
# Replaces the YOURDOMAIN placeholder in every site file with your real domain.
[ -z "$1" ] && { echo "Usage: ./set-domain.sh yourdomain.com"; exit 1; }
grep -rl "YOURDOMAIN.com" --include='*.html' --include='*.xml' --include='*.txt' . | xargs sed -i "s/www\.YOURDOMAIN\.com/www.$1/g"
echo "Done. Remaining placeholders:"; grep -rn "YOURDOMAIN" --include='*.html' --include='*.xml' --include='*.txt' . || echo "none"
