package models

type Chat struct {
	Id       int    `json:"chat_id"`
	ChatName string `json:"chat_name"`
	//DateOfCreation time.Time
	//IsPinned   bool
	//IsArchived bool
	//IsUnread   bool
	//ChatRef string
}

type Message struct {
	Id          int
	Sender_id   int
	Chat_id     int
	MessageText string
	//date_of_creation time.Time
	Is_pinned bool
	//edited_at time.Time
}
