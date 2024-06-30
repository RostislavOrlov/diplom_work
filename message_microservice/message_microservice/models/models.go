package models

import "time"

type Message struct {
	Id             int
	SenderId       int
	SenderUsername string
	ChatId         int
	MessageText    string
	DateOfCreation time.Time
	EditedAt       time.Time
}

type UsersMessages struct {
	Id            int
	UserId        int
	MessageId     int
	PinnedStatus  bool
	ReadStatus    bool
	ForwardStatus bool
	ReplyStatus   bool
}

type Chat struct {
	Id       int
	ChatName string
	//DateOfCreation time.Time
}
