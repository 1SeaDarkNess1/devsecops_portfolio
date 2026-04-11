#!/bin/bash
# scripts/update_threats.sh - Fetches banned IPs and generates GeoIP threat map
set -e

# Get script directory to work with relative paths
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OUTPUT="$DIR/../app/static/threats.json"
TMP=$(mktemp)

echo "[INFO] Starting Threat Map update..."

# Extract banned IPs from fail2ban
# Note: Requires fail2ban installed and sudo access for the running user
IPS=$(sudo fail2ban-client status sshd 2>/dev/null | grep "Banned IP list:" | sed 's/.*Banned IP list:\s*//' | tr ' ' '\n' | sort -u | head -100)

echo '{"attacks":[' > "$TMP"
FIRST=1
COUNT=0

for IP in $IPS; do
  [ -z "$IP" ] && continue
  
  # GeoIP lookup (ip-api.com: free, 45 req/min)
  GEO=$(curl -s --max-time 3 "http://ip-api.com/json/${IP}?fields=status,country,countryCode,lat,lon" 2>/dev/null)
  STATUS=$(echo "$GEO" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
  
  if [ "$STATUS" != "success" ]; then
    echo "[WARN] Could not resolve GeoIP for $IP"
    continue
  fi

  LAT=$(echo "$GEO" | grep -o '"lat":[^,}]*' | cut -d: -f2)
  LON=$(echo "$GEO" | grep -o '"lon":[^,}]*' | cut -d: -f2)
  COUNTRY=$(echo "$GEO" | grep -o '"country":"[^"]*"' | cut -d'"' -f4)
  CC=$(echo "$GEO" | grep -o '"countryCode":"[^"]*"' | cut -d'"' -f4)

  if [ $FIRST -eq 0 ]; then
    echo "," >> "$TMP"
  fi
  
  echo "{\"ip\":\"${IP:0:7}***\",\"lat\":$LAT,\"lon\":$LON,\"country\":\"$COUNTRY\",\"cc\":\"$CC\"}" >> "$TMP"
  FIRST=0
  COUNT=$((COUNT+1))
  
  # Respect rate limit (45 req/min ~ 1.33s/req)
  sleep 1.5
done

echo "],\"total\":$COUNT,\"updated\":$(date +%s)}" >> "$TMP"

# Validate JSON before replacing
if python3 -c "import json; json.load(open('$TMP'))" 2>/dev/null; then
  mv "$TMP" "$OUTPUT"
  chmod 644 "$OUTPUT"
  echo "[OK] Threat map updated with $COUNT blocks."
else
  echo "[ERROR] Generated JSON is invalid. Aborting update."
  rm "$TMP"
  exit 1
fi
