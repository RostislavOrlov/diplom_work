set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
	CREATE DATABASE auth_microservice OWNER postgres;
	CREATE DATABASE chat_microservice OWNER postgres;
	CREATE DATABASE message_microservice OWNER postgres;
	CREATE DATABASE videoconf_microservice OWNER postgres;
	CREATE DATABASE teams_microservice OWNER postgres;
EOSQL

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "chat_microservice" -f /app/sql/init-chat.sql
psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "message_microservice" -f /app/sql/init-message.sql