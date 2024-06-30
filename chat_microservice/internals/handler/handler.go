package handler

import (
	"chat_microservice_new/internals/constants"
	"chat_microservice_new/internals/dto"
	"chat_microservice_new/internals/models"
	"chat_microservice_new/internals/service"
	"encoding/json"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"net/http"
	"strconv"
)

var (
	upgrader = websocket.Upgrader{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
	}

	clients = make([]WebsocketClient, 0, 2048)
)

type (
	Handler struct {
		services *service.Service
	}
	WebsocketClient struct {
		ws     *websocket.Conn
		userId int
		send   chan []byte
	}
)

func NewHandler(services *service.Service) *Handler {
	return &Handler{
		services: services,
	}
}

func (handler *Handler) InitRoutes() *gin.Engine {

	router := gin.New()

	router.GET("/ws/:user_id", handler.ServeWS)
	router.GET("/api/chat/:chat_id/users", handler.GetUsersForChatHandler)

	router.Use(func(c *gin.Context) {
		c.Set("handler", handler)
		c.Next()
	})

	router.Use(cors.New(cors.Config{
		AllowOrigins: []string{"http://localhost:8080", "http://192.168.1.123:8080"}, //"http://localhost:8085"},
		AllowMethods: []string{"GET", "POST"},
	}))

	return router
}

func (handler *Handler) GetUsersForChatHandler(c *gin.Context) {
	chatId, err := strconv.Atoi(c.Param("chat_id"))
	if err != nil {
		return
	}
	usersIds, err := handler.GetUsersForChat(chatId)
	if err != nil {
		return
	}
	usersJson := dto.GetUsersForChatResponse{UsersIds: usersIds}

	//idsBytes, err := json.Marshal(usersJson)
	//if err != nil {
	//	return
	//}

	c.JSON(http.StatusOK, usersJson)
}

func (handler *Handler) ServeWS(c *gin.Context) {

	upgrader.CheckOrigin = func(r *http.Request) bool {
		return true
	}
	ws, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		return
	}

	//chatHandler := c.MustGet("handler").(*Handler)
	userId, err := strconv.Atoi(c.Param("user_id"))
	client := &WebsocketClient{
		ws:     ws,
		userId: userId,
		send:   make(chan []byte, 256),
	}

	flag := isExistingClient(client)

	if !flag {
		clients = append(clients, *client)
	}

	fmt.Println(clients)

	go client.Write()
	go client.Read(handler)

}

func isExistingClient(client *WebsocketClient) bool {
	for _, currClient := range clients {
		if currClient.userId == client.userId {
			return true
		}
	}
	return false
}

func HandleMessage(client *WebsocketClient, handler *Handler, message dto.MessageRequest) {
	switch message.Topic {
	case constants.CREATE_CHAT:
		var params dto.MessageCreateChat
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}

		chat, err := handler.CreateChat(params)
		if err != nil {
			return
		}
		chatBytes, err := json.Marshal(dto.FullCreateChatResponse{
			Request: "createChatForUser",
			Params: dto.CreateChatResponse{
				ChatId:   chat.Id,
				ChatName: chat.ChatName,
			},
		})
		if err != nil {
			return
		}
		client.send <- chatBytes

	case constants.JOIN_CHAT:
		var params dto.MessageJoinChat
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}
		resp, err := handler.JoinChat(params)
		if err != nil {
			return
		}
		respBytes, err := json.Marshal(dto.FullMessageJoinChatResponse{
			Request: "joinChatForUser",
			Params: dto.MessageJoinChatResponse{
				UserId:            resp.UserId,
				ChatId:            resp.ChatId,
				ChatName:          resp.ChatName,
				ParticipantStatus: resp.ParticipantStatus,
				Username:          resp.Username,
			},
		})
		if err != nil {
			return
		}
		//client.send <- respBytes
		usersIds, err := handler.GetUsersForChat(params.ChatId)
		for _, userId := range usersIds {
			for _, currClient := range clients {
				if userId == currClient.userId {
					currClient.send <- respBytes
				}
			}
		}

	case constants.FETCH_ALL_CHATS_FOR_USER:
		var params dto.MessageFetchAllChatsForUser
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}
		chats, err := handler.FetchAllChatsForUser(params.UserId)
		if err != nil {
			return
		}
		chatsBytes, err := json.Marshal(dto.FullFetchChatsForUserResponse{
			Request: "fetchChatsForUser",
			Params: dto.FetchChatsForUserResponse{
				Chats: chats,
			},
		})
		if err != nil {
			return
		}
		//client.Write(chatsBytes)
		client.send <- chatsBytes

	case constants.SET_ARCHIVED_STATUS:
		var params dto.MessageSetArchivedStatus
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}
		err = handler.SetArchivedStatus(params.UserId, params.ChatId, params.IsArchived)
		if err != nil {
			return
		}

	case constants.SET_UNREAD_STATUS:
		var params dto.MessageSetUnreadStatus
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}
		err = handler.SetUnreadStatus(params.UserId, params.ChatId, params.IsUnread)
		if err != nil {
			return
		}

	case constants.SET_PINNED_STATUS:
		var params dto.MessageSetPinnedStatus
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}
		err = handler.SetPinnedStatus(params.UserId, params.ChatId, params.IsPinned)
		if err != nil {
			return
		}

	case constants.DELETE_CHAT_FOR_USER:
	}

}

func (handler *Handler) CreateChat(params dto.MessageCreateChat) (models.Chat, error) {

	chat, err := handler.services.CreateChat(params)
	if err != nil {
		fmt.Println("Ошибка")
	}

	return chat, nil
}

func (handler *Handler) JoinChat(params dto.MessageJoinChat) (*dto.MessageJoinChatResponse, error) {
	resp, _ := handler.services.JoinChat(params)
	return resp, nil
}

func (handler *Handler) FetchAllChatsForUser(userId int) ([]models.Chat, error) {
	return handler.services.FetchAllChatsForUser(userId)
}

func (handler *Handler) SetArchivedStatus(userId, chatId int, archivedStatus bool) error {
	return handler.services.SetArchivedStatus(userId, chatId, archivedStatus)
}

func (handler *Handler) SetUnreadStatus(userId, chatId int, readStatus bool) error {
	return handler.services.SetUnreadStatus(userId, chatId, readStatus)
}

func (handler *Handler) SetPinnedStatus(userId, chatId int, pinnedStatus bool) error {
	return handler.services.SetPinnedStatus(userId, chatId, pinnedStatus)
}

func (handler *Handler) GetUsersForChat(chatId int) ([]int, error) {
	return handler.services.GetUsersForChat(chatId)
}
