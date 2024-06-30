package dto

import (
	"encoding/json"
)

type (
	MessageRequest struct {
		Topic  string
		Params json.RawMessage
	}

	MessageSendMessageInChat struct {
		SenderId       int    `json:"sender_id"`
		SenderUsername string `json:"sender_username"`
		ChatId         int    `json:"chat_id"`
		MessageText    string `json:"message_text"`
	}

	MessageSetReadStatusOfMessage struct {
		MessageId  int  `json:"message_id"`
		SenderId   int  `json:"sender_id"`
		UserId     int  `json:"user_id"`
		ReadStatus bool `json:"read_status"`
	}

	MessageGetMessagesForChat struct {
		ChatId int `json:"chat_id"`
		//TODO: limit/offset
	}

	MessageEditMessage struct {
		MessageId   int    `json:"message_id"`
		ChatId      int    `json:"chat_id"`
		MessageText string `json:"message_text"`
	}
)
