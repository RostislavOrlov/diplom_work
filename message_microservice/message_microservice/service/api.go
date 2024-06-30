package service

import (
	"fmt"
	"message_microservice/dto"
	"message_microservice/models"
	"message_microservice/repository"
)

type ApiService struct {
	repos repository.Api
}

func NewApiService(repos repository.Api) *ApiService {
	return &ApiService{repos: repos}
}

func (apiService *ApiService) GetMessagesForChat(chatId int) ([]models.Message, error) {
	return apiService.repos.GetMessagesForChat(chatId)
}

func (apiService *ApiService) SendMessageInChat(message dto.MessageSendMessageInChat) (*dto.MessageSendMessageInChatResponse, error) {
	return apiService.repos.SendMessageInChat(message)
}

func (apiService *ApiService) PublishMessageSentToChatEvent(messageId int) {
	fmt.Println("Сообщение " + string(messageId) + " отправлено")
}

func (apiService *ApiService) FetchChatTopicByChatId(chatId int) (string, error) {
	return "топик", nil
}

func (apiService *ApiService) SetPinnedStatusOfMessage(userId, messageId int, pinnedStatus bool) error {
	return apiService.repos.SetPinnedStatusOfMessage(userId, messageId, pinnedStatus)
}

func (apiService *ApiService) ForwardMessage(userId, messageId int) error {
	return apiService.repos.ForwardMessage(userId, messageId)
}

func (apiService *ApiService) SetReadStatusOfMessage(userId, messageId int, readStatus bool) (*dto.MessageSetReadStatusOfMessageResponse, error) {
	return apiService.repos.SetReadStatusOfMessage(userId, messageId, readStatus)
}

func (apiService *ApiService) ReplyToMessage(userId, messageId int) error {
	return apiService.repos.ReplyToMessage(userId, messageId)
}

func (apiService *ApiService) EditMessage(message dto.MessageEditMessage) (*dto.MessageEditMessageResponse, error) {
	return apiService.repos.EditMessage(message)
}

//func (apiService *ApiService) GetMessagesByContext(chatId int) ([]models.Message, error) {
//	return apiService.repos.GetMessagesByContext(chatId)
//}
