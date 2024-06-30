package handler

import (
	"encoding/json"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"io"
	"message_microservice/constants"
	"message_microservice/dto"
	"message_microservice/models"
	"message_microservice/service"
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

	router.Use(func(c *gin.Context) {
		c.Set("handler", handler)
		c.Next()
	})

	router.Use(cors.New(cors.Config{
		AllowOrigins: []string{"http://localhost:8080"},
		AllowMethods: []string{"GET", "POST"},
	}))

	return router
}

func (handler *Handler) GetUsersForChat(chatId int) ([]int, error) {
	client := http.Client{}
	req, err := http.NewRequest("GET", fmt.Sprintf("http://localhost:8084/api/chat/%d/users", chatId), nil)
	if err != nil {
		fmt.Println("error getting users for chat")
	}
	resp, err := client.Do(req)

	//defer func(Body io.ReadCloser) {
	//	err := Body.Close()
	//	if err != nil {
	//		fmt.Println(err.Error())
	//	}
	//}(resp.Body)

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err.Error())
	}

	//usersIds := make([]int, 0, 2048)
	var respBody dto.UsersIdsResponse
	err = json.Unmarshal(body, &respBody)
	if err != nil {
		return nil, err
	}

	return respBody.UsersIds, nil
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
	case constants.SEND_MESSAGE:
		var params dto.MessageSendMessageInChat
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}

		resp, err := handler.SendMessageInChat(params)
		if err != nil {
			return
		}
		respBytes, err := json.Marshal(dto.FullMessageSendMessageInChatResponse{
			Request: "sendMessageInChat",
			Params: dto.MessageSendMessageInChatResponse{
				MessageId:      resp.MessageId,
				SenderId:       resp.SenderId,
				SenderUsername: resp.SenderUsername,
				ChatId:         resp.ChatId,
				MessageText:    resp.MessageText,
				DateOfCreation: resp.DateOfCreation,
				EditedAt:       resp.EditedAt,
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

	case constants.GET_MESSAGES_FOR_CHAT:
		var params dto.MessageGetMessagesForChat
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}

		messages, err := handler.GetMessagesForChat(params)
		if err != nil {
			return
		}
		respBytes, err := json.Marshal(dto.FullGetMessagesForChatResponse{
			Request: "getMessagesForChat",
			Params: dto.GetMessagesForChatResponse{
				Messages: messages,
			},
		})
		if err != nil {
			return
		}
		client.send <- respBytes

	case constants.READ_MESSAGE:
		var params dto.MessageSetReadStatusOfMessage
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}

		resp, err := handler.services.SetReadStatusOfMessage(params.UserId, params.MessageId, params.ReadStatus)
		if err != nil {
			return
		}
		respBytes, err := json.Marshal(dto.FullSetReadStatusOfMessageResponse{
			Request: "readMessage",
			Params: dto.MessageSetReadStatusOfMessageResponse{
				UserId:     resp.UserId,
				MessageId:  resp.MessageId,
				ReadStatus: resp.ReadStatus,
				SenderId:   resp.SenderId,
			},
		})
		if err != nil {
			return
		}
		client.send <- respBytes
		for _, currClient := range clients {
			if currClient.userId == params.SenderId {
				currClient.send <- respBytes
			}
		}

	case constants.EDIT_MESSAGE:
		var params dto.MessageEditMessage
		err := json.Unmarshal(message.Params, &params)
		if err != nil {
			return
		}

		resp, err := handler.services.EditMessage(params)
		if err != nil {
			return
		}
		respBytes, err := json.Marshal(dto.FullMessageEditMessageResponse{
			Request: "editMessage",
			Params: dto.MessageEditMessageResponse{
				MessageId:   resp.MessageId,
				MessageText: resp.MessageText,
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

	}
}

func (handler *Handler) SendMessageInChat(params dto.MessageSendMessageInChat) (*dto.MessageSendMessageInChatResponse, error) {
	return handler.services.SendMessageInChat(params)
}

func (handler *Handler) GetMessagesForChat(params dto.MessageGetMessagesForChat) ([]models.Message, error) {
	return handler.services.GetMessagesForChat(params.ChatId)
}
