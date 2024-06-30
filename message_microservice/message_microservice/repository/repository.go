package repository

import (
	"github.com/jackc/pgx/v5/pgxpool"
	"message_microservice/dto"
	"message_microservice/models"
)

type Api interface {
	//тут нужно условно последние 50-100 сообщений
	//нужно подумать про Optional
	GetMessagesForChat(chatId int) ([]models.Message, error)
	SendMessageInChat(message dto.MessageSendMessageInChat) (*dto.MessageSendMessageInChatResponse, error)
	SetPinnedStatusOfMessage(userId, messageId int, pinnedStatus bool) error
	ForwardMessage(userId, messageId int) error
	SetReadStatusOfMessage(userId, messageId int, readStatus bool) (*dto.MessageSetReadStatusOfMessageResponse, error)
	ReplyToMessage(userId, messageId int) error
	EditMessage(message dto.MessageEditMessage) (*dto.MessageEditMessageResponse, error)
	//GetMessagesByContext(chatId int) ([]models.Message, error)
}

type Repository struct {
	Api
}

func NewRepository(db *pgxpool.Pool) *Repository {
	return &Repository{
		Api: NewApiRepository(db),
	}
}
