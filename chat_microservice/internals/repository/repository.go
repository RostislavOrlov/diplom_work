package repository

import (
	"chat_microservice_new/internals/constants"
	"chat_microservice_new/internals/dto"
	"chat_microservice_new/internals/models"
	"context"
	"errors"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
	"log"
)

type Api interface {
	CreateChat(params dto.MessageCreateChat) (models.Chat, error)
	SetArchivedStatus(userId, chatId int, archivedStatus bool) error
	SetUnreadStatus(userId, chatId int, unreadStatus bool) error
	SetPinnedStatus(userId, chatId int, unreadStatus bool) error
	JoinChat(params dto.MessageJoinChat) (*dto.MessageJoinChatResponse, error)
	FetchAllChatsForUser(userId int) ([]models.Chat, error)
	DeleteChatForUser(userId, chatId int) error
	AssignAdminOfChat(userId, chatId int) error

	GetUsersForChat(chatId int) ([]int, error)
	GetChatByChatId(chatId int) (*models.Chat, error)
	//LeaveChat(userId, chatId int) error
	//DeleteChat(chatId int) error
	//
	////для подписчиков
	//ChatCreated(chatId int) error
	//UserJoinedChat(userId, chatId int) error
	//UserLeavedChat(userId, chatId int) error
	//
	////многопользовательские чаты
	//AssignAdminOfChat(userId, chatId int) error
	//SetSettingsOfChat(chatId int) error
	//SetAdminPermissionsOfChat(chatId int) error
}

type PubSub interface {
	CreateTopicByChatId(chatId int) (string, error)
	SubscribeUserToChatTopic(userId int, topic string) error
	FetchChatTopicByChatId(chatId int) (string, error)
}

type Repository struct {
	Api
	PubSub
}

func NewRepository(pgDB *pgxpool.Pool) *Repository {
	return &Repository{
		Api: NewApiPostgres(pgDB),
		//PubSub: NewPubSubRedis(context.Background()),
	}
}

type ApiPostgres struct {
	db *pgxpool.Pool
}

func NewApiPostgres(db *pgxpool.Pool) *ApiPostgres {
	return &ApiPostgres{db: db}
}

func (apiPostgres *ApiPostgres) CreateChat(params dto.MessageCreateChat) (models.Chat, error) {
	var chat models.Chat
	query := fmt.Sprintf("insert into %s (name) values ($1) returning *", chatsTable)
	row := apiPostgres.db.QueryRow(context.Background(), query, params.ChatName)
	err := row.Scan(&chat.Id, &chat.ChatName)
	if err != nil {
		return models.Chat{}, err
	}
	query2 := fmt.Sprintf("insert into %s (user_id, chat_id, participant_status, username) values ($1, $2, $3, $4)", usersChatsTable)
	_ = apiPostgres.db.QueryRow(context.Background(), query2, params.UserId, chat.Id, constants.ADMIN, params.Username)
	return chat, nil
}

func (apiPostgres *ApiPostgres) SetArchivedStatus(userId, chatId int, archivedStatus bool) error {
	query := fmt.Sprintf("update %s set chat_archived_status = $1 where user_id = $2 and chat_id = $3", usersChatsTable)
	_ = apiPostgres.db.QueryRow(context.Background(), query, archivedStatus, userId, chatId)
	return nil
}

func (apiPostgres *ApiPostgres) SetUnreadStatus(userId, chatId int, unreadStatus bool) error {
	query := fmt.Sprintf("update %s set chat_unread_status = $1 where user_id = $2 and chat_id = $3", usersChatsTable)
	_ = apiPostgres.db.QueryRow(context.Background(), query, unreadStatus, userId, chatId)
	return nil
}

func (apiPostgres *ApiPostgres) SetPinnedStatus(userId, chatId int, pinnedStatus bool) error {
	query := fmt.Sprintf("update %s set chat_pinned_status = $1 where user_id = $2 and chat_id = $3", usersChatsTable)
	_ = apiPostgres.db.QueryRow(context.Background(), query, pinnedStatus, userId, chatId)
	return nil
}

func (apiPostgres *ApiPostgres) JoinChat(params dto.MessageJoinChat) (*dto.MessageJoinChatResponse, error) {
	var resp dto.MessageJoinChatResponse
	var temp int
	query := fmt.Sprintf("insert into %s(user_id, chat_id, participant_status, username) values ($1, $2, $3, $4) returning *", usersChatsTable)
	row := apiPostgres.db.QueryRow(context.Background(), query, params.UserId, params.ChatId, constants.USER, params.Username)
	err := row.Scan(&temp, &resp.UserId, &resp.ChatId, &resp.ParticipantStatus, &resp.Username)
	if err != nil {
		return nil, errors.New("error join chat repository")
	}
	return &resp, nil
}

func (apiPostgres *ApiPostgres) AssignAdminOfChat(userId, chatId int) error {
	query := fmt.Sprintf("insert into %s(user_id, chat_id, participant_status) "+
		"values($1, $2, $3)", "participant_multiplayer_chat")
	_ = apiPostgres.db.QueryRow(context.Background(), query, userId, chatId, "ADMIN")
	return nil
}

func (apiPostgres *ApiPostgres) FetchAllChatsForUser(userId int) ([]models.Chat, error) {
	var chats = make([]models.Chat, 0, 2048)
	query := fmt.Sprintf("select * from chats where chat_id in (select chat_id from users_chats where user_id = $1)")

	rows, err := apiPostgres.db.Query(context.Background(), query, userId)
	if err != nil {
		return nil, err
	}

	for rows.Next() {
		var chat models.Chat

		err := rows.Scan(&chat.Id, &chat.ChatName)
		if err != nil {
			log.Fatal(err)
		}
		chats = append(chats, chat)
	}
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
	return chats, nil
}

func (apiPostgres *ApiPostgres) DeleteChatForUser(userId, chatId int) error {
	query := fmt.Sprintf("delete from %s where chat_id = $1; "+
		"delete from %s where user_id = $2 and chat_id = $3", chatsTable, usersChatsTable)

	_ = apiPostgres.db.QueryRow(context.Background(), query, chatId, userId, chatId)
	return nil
}

func (apiPostgres *ApiPostgres) GetUsersForChat(chatId int) ([]int, error) {
	var ids []int
	query := fmt.Sprintf("select user_id from users_chats where chat_id = $1")
	rows, err := apiPostgres.db.Query(context.Background(), query, chatId)
	for rows.Next() {
		var userId int
		err := rows.Scan(&userId)
		if err != nil {
			log.Fatal(err)
		}
		ids = append(ids, userId)
	}
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
	return ids, nil
}

func (apiPostgres *ApiPostgres) GetChatByChatId(chatId int) (*models.Chat, error) {
	var chat models.Chat
	query := fmt.Sprintf("select * from %s where chat_id = $1", chatsTable)
	row := apiPostgres.db.QueryRow(context.Background(), query, chatId)
	err := row.Scan(&chat.Id, &chat.ChatName)
	if err != nil {
		return nil, errors.New("failed to scan GetChatByChatId")
	}
	return &chat, nil
}
