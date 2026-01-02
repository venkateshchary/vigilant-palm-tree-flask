#!/bin/sh
set -e

# POSIX-compatible idempotent init script for Postgres container
# Processes .sql and .sql.gz files in /docker-entrypoint-initdb.d
# Always connect to the 'postgres' maintenance database when checking/creating DBs
MAINT_DB=postgres

for f in /docker-entrypoint-initdb.d/*; do
  case "$f" in
    *.sql|*.sql.gz)
      echo "-- processing $f"

      if grep -i -m1 -E 'CREATE[[:space:]]+DATABASE' "$f" >/dev/null 2>&1; then
        create_line=$(grep -i -m1 -E 'CREATE[[:space:]]+DATABASE' "$f" 2>/dev/null || true)
        # portable extraction: find the token after the word DATABASE, then strip quotes
        dbname=$(printf '%s' "$create_line" | awk 'BEGIN{IGNORECASE=1} {for(i=1;i<=NF;i++){if(tolower($i)=="database"){print $(i+1); exit}}}')
        dbname=$(printf '%s' "$dbname" | tr -d '"\047')
        [ -z "$dbname" ] && dbname="$POSTGRES_DB"

        exists=$(psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$MAINT_DB" -tAc "SELECT 1 FROM pg_database WHERE datname='$dbname'" 2>/dev/null || true)
        if echo "$exists" | grep -q 1; then
          echo "Database $dbname exists, skipping $f"
        else
          echo "Running $f to create/populate database $dbname (connected to $MAINT_DB)"
          if echo "$f" | grep -q '\.gz$'; then
            gunzip -c "$f" | psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$MAINT_DB" -f -
          else
            psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$MAINT_DB" -f "$f"
          fi
        fi

      else
        dbname=${POSTGRES_DB:-$POSTGRES_USER}

        exists=$(psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$MAINT_DB" -tAc "SELECT 1 FROM pg_database WHERE datname='$dbname'" 2>/dev/null || true)
        if echo "$exists" | grep -q 1; then
          echo "Database $dbname exists, skipping import of $f"
        else
          echo "Creating database $dbname and importing $f (using $MAINT_DB to run CREATE)"
          psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$MAINT_DB" -c "CREATE DATABASE \"$dbname\";"
          if echo "$f" | grep -q '\.gz$'; then
            gunzip -c "$f" | psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$dbname"
          else
            psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$dbname" -f "$f"
          fi
        fi
      fi
      ;;
    *)
      ;;
  esac
done

echo "init scripts finished"
