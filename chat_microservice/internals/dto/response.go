package dto

import "chat_microservice_new/internals/models"

type MessageCreateChatResponse struct {
	ChatId int
}

func NewMessageCreateChatResponse(chatId int) *MessageCreateChatResponse {
	return &MessageCreateChatResponse{ChatId: chatId}
}

type ChatResponse struct {
	ChatId int    `json:"chat_id"`
	Name   string `json:"name"`
}

type FullFetchChatsForUserResponse struct {
	Request string
	Params  FetchChatsForUserResponse
}

type FetchChatsForUserResponse struct {
	Chats []models.Chat `json:"chats"`
}

type FullCreateChatResponse struct {
	Request string
	Params  CreateChatResponse
}

type CreateChatResponse struct {
	ChatId   int    `json:"chat_id"`
	ChatName string `json:"chat_name"`
}

type FullMessageJoinChatResponse struct {
	Request string
	Params  MessageJoinChatResponse
}

type MessageJoinChatResponse struct {
	UserId            int    `json:"user_id"`
	Username          string `json:"username"`
	ChatId            int    `json:"chat_id"`
	ChatName          string `json:"chat_name"`
	ParticipantStatus string `json:"participant_status"`
}

type GetUsersForChatResponse struct {
	UsersIds []int `json:"users_ids"`
}
