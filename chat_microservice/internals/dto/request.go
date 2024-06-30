package dto

import "encoding/json"

type (
	MessageRequest struct {
		Topic  string
		Params json.RawMessage
	}

	MessageCreateChat struct {
		UserId   int    `json:"user_id"`
		ChatName string `json:"chat_name"`
		Username string `json:"username"`
	}

	MessageJoinChat struct {
		UserId            int    `json:"user_id"`
		Username          string `json:"username"`
		ChatId            int    `json:"chat_id"`
		ParticipantStatus string `json:"participant_status"`
	}

	MessageGetMessagesForChat struct {
		ChatId int `json:"chat_id"`
	}

	MessageSetArchivedStatus struct {
		UserId     int  `json:"user_id"`
		ChatId     int  `json:"chat_id"`
		IsArchived bool `json:"is_archived"`
	}

	MessageSetUnreadStatus struct {
		UserId   int  `json:"user_id"`
		ChatId   int  `json:"chat_id"`
		IsUnread bool `json:"is_unread"`
	}

	MessageSetPinnedStatus struct {
		UserId   int  `json:"user_id"`
		ChatId   int  `json:"chat_id"`
		IsPinned bool `json:"is_pinned"`
	}

	MessageFetchAllChatsForUser struct {
		UserId int `json:"user_id"`
	}
)
