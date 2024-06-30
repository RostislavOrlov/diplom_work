FROM postgres:latest

COPY init.sh /docker-entrypoint-initdb.d/init.sh
COPY init-chat.sql /app/sql/init-chat.sql
COPY init-message.sql /app/sql/init-message.sql

