package service

import (
	"message_microservice/dto"
	"message_microservice/models"
	"message_microservice/repository"
)

type Api interface {
	GetMessagesForChat(chatId int) ([]models.Message, error)
	SendMessageInChat(params dto.MessageSendMessageInChat) (*dto.MessageSendMessageInChatResponse, error)
	SetPinnedStatusOfMessage(userId, messageId int, pinnedStatus bool) error
	ForwardMessage(userId, messageId int) error
	SetReadStatusOfMessage(userId, messageId int, readStatus bool) (*dto.MessageSetReadStatusOfMessageResponse, error)
	ReplyToMessage(userId, messageId int) error
	//GetMessagesByContext(chatId int) ([]models.Message, error)
	EditMessage(message dto.MessageEditMessage) (*dto.MessageEditMessageResponse, error)

	FetchChatTopicByChatId(chatId int) (string, error)
	PublishMessageSentToChatEvent(messageId int)
}

type Service struct {
	Api
}

func NewService(repos *repository.Repository) *Service {
	return &Service{
		Api: NewApiService(repos),
	}
}
