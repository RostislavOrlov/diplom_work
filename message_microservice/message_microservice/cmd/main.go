package main

import (
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
	"github.com/spf13/viper"
	"log"
	"message_microservice/handler"
	"message_microservice/repository"
	"message_microservice/server"
	"message_microservice/service"
	"os"
)

func main() {

	if err := InitConfig(); err != nil {
		log.Fatalf("error initializing configs: %s", err.Error())
	}

	if err := godotenv.Load(); err != nil {
		log.Fatalf("error loading environment variables: %s", err.Error())
	}

	pgDB, err := repository.NewPostgresDB(repository.Config{
		Host:     viper.GetString("db.host"),
		Port:     viper.GetString("db.port"),
		Username: viper.GetString("db.username"),
		Password: os.Getenv("DB_PASSWORD"),
		DBName:   viper.GetString("db.dbname"),
		SSLMode:  viper.GetString("db.sslmode"),
	})

	if err != nil {
		log.Fatalf("error initializing database: %s", err.Error())
	}

	repos := repository.NewRepository(pgDB)
	services := service.NewService(repos)

	handlers := handler.NewHandler(services)
	//go handlers.HandleMessage()
	srv := new(server.Server)
	if err := srv.Run("8085", handlers.InitRoutes()); err != nil {
		log.Fatalf("error occured while running server: %s", err.Error())
	}

}

func InitConfig() error {
	viper.AddConfigPath("configs")
	viper.SetConfigName("config")
	return viper.ReadInConfig()
}
