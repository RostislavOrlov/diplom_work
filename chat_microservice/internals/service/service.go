package service

import (
	"chat_microservice_new/internals/dto"
	"chat_microservice_new/internals/models"
	"chat_microservice_new/internals/repository"
	"encoding/json"
	"fmt"
)

type Api interface {
	CreateChat(params dto.MessageCreateChat) (models.Chat, error)
	JoinChat(params dto.MessageJoinChat) (*dto.MessageJoinChatResponse, error)
	SetUnreadStatus(userId, chatId int, unreadStatus bool) error
	SetPinnedStatus(userId, chatId int, pinnedStatus bool) error
	FetchAllChatsForUser(userId int) ([]models.Chat, error)
	DeleteChatForUser(userId, chatId int) error
	AssignAdminOfChat(userId, chatId int) error

	GetUsersForChat(chatId int) ([]int, error)

	//лишние методы
	SetArchivedStatus(userId, chatId int, archivedStatus bool) error
}

type PubSub interface {
	CreateTopicByChatId(chatId int) (string, error)
	SubscribeUserToChatTopic(userId int, topic string) error
	FetchChatTopicByChatId(chatId int) (string, error)
}

type Service struct {
	Api
	PubSub
}

func NewService(apiRepos *repository.Repository) *Service {
	return &Service{
		Api: NewApiService(apiRepos),
	}
}

type ApiService struct {
	apiRepos repository.Api
}

func NewApiService(apiRepos repository.Api) *ApiService {
	return &ApiService{apiRepos: apiRepos}
}

func (apiService *ApiService) CreateChat(params dto.MessageCreateChat) (models.Chat, error) {

	chat, err := apiService.apiRepos.CreateChat(params)
	_, err = json.Marshal(chat)
	if err != nil {
		fmt.Println("Ошибка")
	}
	return chat, err
}

func (apiService *ApiService) JoinChat(params dto.MessageJoinChat) (*dto.MessageJoinChatResponse, error) {
	resp, _ := apiService.apiRepos.JoinChat(params)
	chat, _ := apiService.apiRepos.GetChatByChatId(params.ChatId)
	resp.ChatName = chat.ChatName
	return resp, nil
}

func (apiService *ApiService) AssignAdminOfChat(userId, chatId int) error {
	return apiService.apiRepos.AssignAdminOfChat(userId, chatId)
}

func (apiService *ApiService) SetArchivedStatus(userId, chatId int, archivedStatus bool) error {
	return apiService.apiRepos.SetArchivedStatus(userId, chatId, archivedStatus)
}

func (apiService *ApiService) SetUnreadStatus(userId, chatId int, unreadStatus bool) error {
	return apiService.apiRepos.SetUnreadStatus(userId, chatId, unreadStatus)
}

func (apiService *ApiService) SetPinnedStatus(userId, chatId int, pinnedStatus bool) error {
	return apiService.apiRepos.SetPinnedStatus(userId, chatId, pinnedStatus)
}

func (apiService *ApiService) FetchAllChatsForUser(userId int) ([]models.Chat, error) {
	return apiService.apiRepos.FetchAllChatsForUser(userId)
}

func (apiService *ApiService) DeleteChatForUser(userId, chatId int) error {
	return apiService.apiRepos.DeleteChatForUser(userId, chatId)
}

func (apiService *ApiService) GetUsersForChat(chatId int) ([]int, error) {
	return apiService.apiRepos.GetUsersForChat(chatId)
}
