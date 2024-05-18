#!/usr/bin/env bash

mysql --user=root --password="$MYSQL_ROOT_PASSWORD" <<-EOSQL
    CREATE DATABASE IF NOT EXISTS ocr_api_db;
    GRANT ALL PRIVILEGES ON \`ocr_api_db%\`.* TO '$MYSQL_USER'@'%';
EOSQL
