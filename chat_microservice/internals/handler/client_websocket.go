package handler

import (
	"chat_microservice_new/internals/dto"
	"encoding/json"
	"fmt"
	"github.com/gorilla/websocket"
	"time"
)

const (
	// Time allowed to write a message to the peer.
	writeWait = 10 * time.Hour

	// Time allowed to read the next pong message from the peer.
	pongWait = 60 * time.Hour

	// Send pings to peer with this period. Must be less than pongWait.
	pingPeriod = (pongWait * 9) / 10

	// Maximum message size allowed from peer.
	maxMessageSize = 512
)

func (client *WebsocketClient) Read(handler *Handler) {

	defer func() {
		client.ws.Close()
	}()
	client.ws.SetReadLimit(maxMessageSize)
	client.ws.SetReadDeadline(time.Now().Add(pongWait))
	client.ws.SetPongHandler(func(string) error { client.ws.SetReadDeadline(time.Now().Add(pongWait)); return nil })
	for {
		_, byteMessage, err := client.ws.ReadMessage()
		if err != nil {
			fmt.Println("ERROR", err)
			fmt.Println(clients)
			//break
		}

		var message dto.MessageRequest
		err = json.Unmarshal(byteMessage, &message)
		if err != nil {
			return
		}

		HandleMessage(client, handler, message)
	}
}

func (client *WebsocketClient) Write() {
	ticker := time.NewTicker(pingPeriod)
	defer func() {
		ticker.Stop()
		client.ws.Close()
	}()

	for {
		select {
		case message, _ := <-client.send:
			client.ws.SetWriteDeadline(time.Now().Add(writeWait))
			//if !ok {
			//	// The hub closed the channel.
			//	client.ws.WriteMessage(websocket.CloseMessage, []byte{})
			//	return
			//}

			w, err := client.ws.NextWriter(websocket.TextMessage)
			if err != nil {
				return
			}
			w.Write(message)
			//
			//// Add queued chat messages to the current websocket message.
			//n := len(client.send)
			//for i := 0; i < n; i++ {
			//	w.Write(newline)
			//	w.Write(<-c.send)
			//}

			if err := w.Close(); err != nil {
				return
			}
		case <-ticker.C:
			client.ws.SetWriteDeadline(time.Now().Add(writeWait))
			if err := client.ws.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}

}
