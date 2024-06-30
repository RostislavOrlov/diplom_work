package repository

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
	"log"
	"message_microservice/dto"
	"message_microservice/models"
	"time"
)

type ApiRepository struct {
	db *pgxpool.Pool
}

func NewApiRepository(db *pgxpool.Pool) *ApiRepository {
	return &ApiRepository{db: db}
}

func (apiRepository *ApiRepository) GetMessagesForChat(chatId int) ([]models.Message, error) {
	var messages = make([]models.Message, 0, 2048)
	query := fmt.Sprintf("select * from messages where chat_id = $1")
	rows, err := apiRepository.db.Query(context.Background(), query, chatId)

	for rows.Next() {
		var message models.Message

		err := rows.Scan(&message.Id, &message.SenderId, &message.SenderUsername,
			&message.ChatId, &message.MessageText, &message.DateOfCreation, &message.EditedAt)
		if err != nil {
			log.Fatal(err)
		}
		messages = append(messages, message)
	}
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
	return messages, nil
}

func (apiRepository *ApiRepository) SendMessageInChat(message dto.MessageSendMessageInChat) (*dto.MessageSendMessageInChatResponse, error) {

	query := fmt.Sprintf("insert into messages(sender_id, sender_username, chat_id, message_text, date_of_creation, edited_at) values ($1, $2, $3, $4, $5, $6) returning *")
	rows, err := apiRepository.db.Query(context.Background(), query, message.SenderId,
		message.SenderUsername, message.ChatId, message.MessageText, time.Now(), time.Now())
	if err != nil {
		fmt.Println(err.Error())
	}

	var resp dto.MessageSendMessageInChatResponse
	for rows.Next() {
		err := rows.Scan(&resp.MessageId, &resp.SenderId, &resp.SenderUsername,
			&resp.ChatId, &resp.MessageText, &resp.DateOfCreation, &resp.EditedAt)
		if err != nil {
			log.Fatal(err)
		}
	}
	return &resp, nil
}

func (apiRepository *ApiRepository) SetPinnedStatusOfMessage(userId, messageId int, pinnedStatus bool) error {
	//query := fmt.Sprintf("insert into users_messages values($1, $2, $3, false, false, false) on conflict (record_id) do update set pinned_status = $4")
	//apiRepository.db.QueryRow(context.Background(), query, userId, messageId, pinnedStatus, pinnedStatus)
	return nil
}

func (apiRepository *ApiRepository) ForwardMessage(userId, messageId int) error {
	//query := fmt.Sprintf("insert into users_messages values ($1, $2, false, false, true, false) on conflict (record_id) do update set forward_status = true")
	//apiRepository.db.QueryRow(context.Background(), query, userId, messageId)
	return nil
}

func (apiRepository *ApiRepository) SetReadStatusOfMessage(userId, messageId int, readStatus bool) (*dto.MessageSetReadStatusOfMessageResponse, error) {
	query := fmt.Sprintf("insert into users_messages(user_id, message_id, read_status) values($1, $2, true) on conflict (record_id) do update set read_status = $3 returning user_id, message_id, read_status")
	row := apiRepository.db.QueryRow(context.Background(), query, userId, messageId, readStatus)
	var resp dto.MessageSetReadStatusOfMessageResponse
	err := row.Scan(&resp.UserId, &resp.MessageId, &resp.ReadStatus)
	query = "select sender_id from messages where message_id = $1"
	row = apiRepository.db.QueryRow(context.Background(), query, messageId)
	var senderId int
	err = row.Scan(&senderId)
	resp.SenderId = senderId
	if err != nil {
		return nil, err
	}
	return &resp, nil
}

func (apiRepository *ApiRepository) ReplyToMessage(userId, messageId int) error {
	//query := fmt.Sprintf("insert into users_messages values($1, $2, false, false, false, true) on conflict (record_id) do update set reply_status = true")
	//apiRepository.db.QueryRow(context.Background(), query, userId, messageId)
	return nil
}

func (apiRepository *ApiRepository) EditMessage(message dto.MessageEditMessage) (*dto.MessageEditMessageResponse, error) {
	query := fmt.Sprintf("update messages set message_text = $1 where message_id = $2 returning message_id, message_text")
	row := apiRepository.db.QueryRow(context.Background(), query, message.MessageText, message.MessageId)
	var resp dto.MessageEditMessageResponse
	err := row.Scan(&resp.MessageId, &resp.MessageText)
	if err != nil {
		return nil, err
	}
	return &resp, nil
}

//func (apiRepository *ApiRepository) GetMessagesByContext(chatId int) ([]models.Message, error) {
//	query :=
//}
