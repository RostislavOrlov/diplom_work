package dto

import (
	"message_microservice/models"
	"time"
)

type (
	FullMessageSendMessageInChatResponse struct {
		Request string
		Params  MessageSendMessageInChatResponse
	}

	MessageSendMessageInChatResponse struct {
		MessageId      int       `json:"message_id"`
		SenderId       int       `json:"sender_id"`
		SenderUsername string    `json:"sender_username"`
		ChatId         int       `json:"chat_id"`
		MessageText    string    `json:"message_text"`
		DateOfCreation time.Time `json:"date_of_creation"`
		EditedAt       time.Time `json:"edited_at"`
	}

	FullGetMessagesForChatResponse struct {
		Request string
		Params  GetMessagesForChatResponse
	}

	FullSetReadStatusOfMessageResponse struct {
		Request string
		Params  MessageSetReadStatusOfMessageResponse
	}

	MessageSetReadStatusOfMessageResponse struct {
		MessageId  int  `json:"message_id"`
		ReadStatus bool `json:"read_status"`
		UserId     int  `json:"user_id"`
		SenderId   int  `json:"sender_id"`
	}

	FullMessageEditMessageResponse struct {
		Request string
		Params  MessageEditMessageResponse
	}

	MessageEditMessageResponse struct {
		MessageId   int    `json:"message_id"`
		MessageText string `json:"message_text"`
	}

	GetMessagesForChatResponse struct {
		Messages []models.Message `json:"messages"`
	}

	UsersIdsResponse struct {
		UsersIds []int `json:"users_ids"`
	}
)
