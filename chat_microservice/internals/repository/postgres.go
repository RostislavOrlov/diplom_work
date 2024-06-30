package repository

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
)

const (
	chatsTable       = "chats"
	usersChatsTable  = "users_chats"
	chatsTopicsTable = "chats_topics"
	usersTopicsTable = "users_topics"
)

type Config struct {
	Host     string
	Port     string
	Username string
	Password string
	DBName   string
	SSLMode  string
}

//func NewPostgresDB(cfg Config) (*sqlx.DB, error) {
//	db, err := sqlx.Open("postgres",
//		fmt.Sprintf("host=%s port=%s user=%s dbname=%s password=%s sslmode=%s",
//			cfg.Host, cfg.Port, cfg.Username, cfg.DBName, cfg.Password, cfg.SSLMode))
//
//	if err != nil {
//		return nil, err
//	}
//
//	err = db.Ping()
//
//	if err != nil {
//		fmt.Println("Неудачное подключение к базе данных")
//		return nil, err
//	}
//
//	return db, err
//}

func NewPostgresDB(cfg Config) (*pgxpool.Pool, error) {
	pool, err := pgxpool.New(context.Background(),
		fmt.Sprintf("host=%s port=%s user=%s dbname=%s password=%s sslmode=%s",
			cfg.Host, cfg.Port, cfg.Username, cfg.DBName, cfg.Password, cfg.SSLMode))

	if err != nil {

	}

	return pool, nil
}
