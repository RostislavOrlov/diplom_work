<script>
    // import MyMessage from './MyMessage.vue';
    // import MyReceivedMessage from './MyReceivedMessage.vue'
    // import { ref } from 'vue';

    // const messageClickListener = () => {
    //     // console.log(messages.value.length)
    //     alert("Message")
    // }
    //      const messages = ref([
    //      {
    //       id: 15,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 14,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 13,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 12,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //      {
    //       id: 11,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //      {
    //       id: 10,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 9,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 8,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 7,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 6,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "6",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 5,
    //       senderName: "Jane Smith",
    //       profilePhoto: "",
    //       text: "5",
    //       sendingTime: new Date('December 17, 1995 03:28:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 4,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "4",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 3,
    //       senderName: "Jane Smith",
    //       profilePhoto: "",
    //       text: "3",
    //       sendingTime: new Date('December 17, 1995 03:28:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 2,
    //       senderName: "Jane Smith",
    //       profilePhoto: "",
    //       text: "2",
    //       sendingTime: new Date('December 17, 1995 03:28:00'),
    //       messageClickListener: messageClickListener,
    //     },
    //     {
    //       id: 1,
    //       senderName: "Slava",
    //       profilePhoto: "",
    //       text: "1",
    //       sendingTime: new Date('December 17, 1995 03:24:00'),
    //       messageClickListener: messageClickListener,
    //     },

    // ])
    import { getChatWebsocket, getMessagesWebsocket } from '@/websocket';
import MyMessageFinal from './MyMessageFinal.vue';
import MyReceivedMessageFinal from './MyReceivedMessageFinal.vue';

    export default {
        data() {
            return {
                messages: [],
                socket: null,
                socketMessages: null,
                messageInput: '',
                addUser: false,
                userAddId: 0, 
                userAddUsername: '',
                userAddEmail: '',
                chatName: localStorage.getItem('currChatName'),
                currUser: localStorage.getItem('userName'),
                currMessageId: 0,
                currMessageText: ''
            }
        },

        computed: {
            messagesComputed() {
                 return localStorage.getItem('userMessages' + String(localStorage.getItem('currChatId')))
        },
            // currUser() {
            //     return localStorage.getItem('userName')
            // }
    },

        // components: {MyMessage, MyReceivedMessage},
        components: { MyMessageFinal, MyReceivedMessageFinal },

        methods: {
            fetchMessagesForChat() {
                console.log('fetching messages for chat')
                this.socketMessages.send(JSON.stringify({
                    'topic': 'getMessagesForChat',
                    'params': {
                        chat_id: Number(localStorage.getItem('currChatId'))
                    }
                }))
            },
            sendMessage() {
                if((this.messageInput != '') && (this.currMessageId == 0)) {
                    console.log(this.messageInput)
                    this.socketMessages.send(JSON.stringify({
                        'topic': 'sendMessageInChat',
                        'params': {
                            sender_id: Number(localStorage.getItem('userId')),
                            sender_username: localStorage.getItem('userName'),
                            chat_id: Number(localStorage.getItem('currChatId')),
                            message_text: this.messageInput
                        }
                    }))
                    this.messageInput = ''
                }
                else if (this.currMessageId != 0) {
                    this.socketMessages.send(JSON.stringify({
                        'topic': 'editMessage',
                        'params': {
                            'message_id': this.currMessageId,
                            'chat_id': Number(localStorage.getItem('currChatId')),
                            'message_text': this.messageInput
                        }
                    }))
                    this.messageInput = ''
                }
            },
            toAddUser() {
                this.addUser = true
            },
            joinChatForUser() {
                this.getUserByEmail() 
                setTimeout(() => {
                    this.socket.send(JSON.stringify({
                    'topic': 'joinChatForUser',
                    'params': {
                        'user_id': this.userAddId,
                        'username': this.userAddUsername,
                        'chat_id': Number(localStorage.getItem('currChatId')),
                        'participant_status': "Участник"
                    }
                }))
                }, 2000);
                
                this.addUser = false
            },
            getUserByEmail() {
                fetch(`http://localhost:8082/api/users/email`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: this.userAddEmail
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.userAddId = data['id']
                    this.userAddUsername = data['username']
                    this.userAddEmail = data['email']
                })
            },
            messageReadListener(message) {
                if(message.senderName != localStorage.getItem('userName')) {
                    console.log('messageReadListener')
                    this.socketMessages.send(JSON.stringify({
                        'topic': 'readMessage',
                        'params': {
                            'message_id': message.messageId,
                            'sender_id': message.senderId,
                            'user_id': Number(localStorage.getItem('userId')),
                            'read_status': true
                        }
                    }))
                }
            },
            editMessage(message) {
                if(message.senderId == Number(localStorage.getItem('userId'))) {
                    // console.log(message.messageText)
                    this.messageInput = message.messageText
                    // console.log("MESSAGE INPUT", this.messageInput)
                    console.log('editMessageListener')
                    this.currMessageId = message.messageId
                    this.currMessageText = message.messageText
                    console.log("CURR MESSAGE ID", this.currMessageId)
                    console.log("CURR MESSAGE TEXT", this.currMessageText)
                }
            }
        },

        created() {
            this.socket = getChatWebsocket()
            this.socketMessages = getMessagesWebsocket()
            this.socket.onmessage = (event) => {
                console.log("data messages", event.data)
                let dataJson = JSON.parse(event.data)
                console.log("USER ID", Number(localStorage.getItem('userId')))
                if(dataJson['Request'] == 'joinChatForUser') {
                    if(dataJson['Params'].user_id == Number(localStorage.getItem('userId'))) {
                        //emit to MyChatPage
                        this.$emit('joinChat', dataJson['Params'].chat_id)
                    } 
                }

            }
            this.socketMessages.onmessage = (event) => {
                console.log("data messages (websocket of messages)", event.data)
                let dataJson = JSON.parse(event.data)
                if(dataJson['Request'] == 'getMessagesForChat') {
                    for (let i = 0; i < dataJson['Params'].messages.length; i++) {
                        this.messages.push({
                            messageId: dataJson['Params'].messages[i].Id,
                            senderId: dataJson['Params'].messages[i].SenderId,
                            senderName: dataJson['Params'].messages[i].SenderUsername,
                            messageText: dataJson['Params'].messages[i].MessageText,
                            isReaded: false
                    })
                    }
                }
                else if(dataJson['Request'] == 'sendMessageInChat') {
                    console.log("SEND MESSAGE IN CHAT", dataJson['Params'])
                    this.messages.push(
                        {
                            messageId: dataJson['Params'].message_id,
                            senderId: dataJson['Params'].sender_id,
                            senderName: dataJson['Params'].sender_username,
                            messageText: dataJson['Params'].message_text,
                            isReaded: false
                        }
                    )
                    // this.$emit('joinChat', dataJson['Params'])
                    // localStorage.setItem('userMessages' + String(localStorage.getItem('currChatId')), dataJson['params'])
                }
                else if(dataJson['Request'] == 'readMessage') {
                    if((dataJson['Params'].sender_id == Number(localStorage.getItem('userId'))) && (dataJson['Params'].sender_id != dataJson['Params'].user_id)) {
                        this.messages.map(currMessage => {
                            if(currMessage.messageId == dataJson['Params'].message_id) {
                                currMessage.isReaded = true
                            }})
                        }
                }
                else if(dataJson['Request'] == 'editMessage') {
                    this.messages.map(currMessage => {
                            if(currMessage.messageId == dataJson['Params'].message_id) {
                                currMessage.messageText = dataJson['Params'].message_text
                            }})
                }

            }
            setTimeout(() => {
                this.fetchMessagesForChat()
            }, 2000);
        }
    }
    
</script>

<template>
    <div class="chat" v-if="addUser == false">
        <div class="chat-navbar">
            <div class="chat-navbar-left">
                <!-- <img alt="Chat photo"> -->
                <h3 class="chat-name">{{ chatName }}</h3>
                <button @click="toAddUser">Добавить участника</button>
            </div>
            <div class="chat-navbar-right">
                <!-- <img alt="Search">
                <img alt="More"> -->
            </div>
        </div>

        <div class="pin-message"></div>
        <div class="dialog-container-parent">
        <!-- <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div>
        <div class="tests"></div> -->
        
        <div v-for="message in messages" :key="message.id" class="dialog" @mouseover="messageReadListener(message)" @click="editMessage(message)">
            <MyMessageFinal v-if="message.senderName === currUser" :messageTextFinal="message.messageText" :sending-time="message.messageDateFinal"
            :messageSenderNameFinal="message.senderName" :isReaded="message.isReaded"></MyMessageFinal>
            <MyReceivedMessageFinal v-else :messageTextFinal="message.messageText" :sending-time="message.sendingTime" 
             :messageSenderNameFinal="message.senderName" profile-photo=""></MyReceivedMessageFinal>
        </div>

    <!-- </div> -->
    <!-- <div></div> -->
</div>
        <!-- </div> -->

        <footer class="chat-footbar">
            <!-- <img alt="profile-image">
            <img alt="files"> -->
            <input class="message-input" placeholder="Сообщение..." v-model="messageInput">
            <button @click="sendMessage">Отправить</button>
        </footer>
    </div>

    <div class="add-user-page" v-if="addUser == true">
        <input v-model="userAddEmail">
        <button @click="joinChatForUser">Добавить участника</button>
    </div>
</template>

<style scoped>

.tests {
    width: 50%;
    background-color: lightgreen;
    height: 10vh;
    margin: 2vh;
}

.dialog-container-parent {
    display: flex;
    flex-direction: column;
    flex-grow: 2;
    width: 75%;
    height: 80vh; 
    justify-content: flex-end;
    /* align-items: flex-start; */
    overflow-y: scroll;
    scrollbar-width: none;
    background-color: rgb(222, 254, 238);
    border-bottom: 10px solid white;
    
}

.my-message {
        background-color: rgb(48, 195, 11);
        color: #333;
        border-radius: 0.5em;
        padding: 10px;
        width: 35%;
        align-self: flex-end;
    }

    .my-message .sending-time {
        font-size: 12px;
        color:  #5d5d5d;
        align-self: flex-end;        
    }

    .received-message {
        background-color: #e6e6e6;
        color: #333;
        border-radius: 0.5em;
        padding: 10px;
        align-self: flex-start;
        width: 35%;
    }

    .received-message .received-sending-time {
        font-size: 12px;
        color: #5d5d5d;
        align-self: flex-end;
    }

    .received-sending-time {
        align-items: flex-end;
    }

    .received-message-header {
        display: flex;
        align-items: center;
    }

    .sender-name {
        font-size: medium;
        font-style: italic;
    }

    .dialog-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        /* flex-grow: 1; */
        width: 100%;
        /* height: fit-content; */
        /* overflow: scroll; */
    }

    .dialog {
        /* overflow: hidden; */
        /* width: 100%; */
        display: flex;
        flex-direction: column;
        /* flex: 1; */
        /* align-items: center; */
        /* flex-grow: 1; */
        /* justify-content: flex-end; */
    }

    .chat {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: 90vh;
        padding-top: 5vh;
        /* justify-content: space-between; */
    }

    .chat-navbar {
        display: flex;
        width: 75%;
        border: 1px solid lightgray;
        /* border: 0; */
        /* border-radius: 5%; */
        align-items: center;
    }

    .chat-navbar-left {
        display: flex;
        justify-content: space-around;
        width: 30%;
    } 

    .chat-navbar-right {
        display: flex;
        justify-content: flex-end;
        /* width: 50%; */
    }

    .chat-footbar {
        display: flex;
        /* margin-bottom: 0%; */
        height: 75px;
        width: 75%;
        align-items: center;
        justify-content: center;
        /* border-top: 1px solid gray; */
        /* background-color: rgb(243, 225, 240); */
        background-color: rgb(208, 243, 226);
        /* border: 1px solid gray; */
    }

    .message-input {
        width: 75%;
        height: 5vh;
        border: 0;
    }

    /* .my-message {
        display: flex;
        justify-content: flex-end;
        height: 5vh;
        align-items: center;
    }

    .my-message-text {
        border: 1px solid gray;
        border-radius: 1em;
        width: 30%;
        background-color: rgb(29, 141, 1);
        font-size: 30px;
        word-wrap: break-word;
        padding-top: 5px;
        padding-left: 10px;
        display: flex;
        flex-direction: column;
        align-items: end;
        color: white
    }

    .sending-time {
        padding-right: 20px;
        font-size: 20px;
    }

    .received-message {
        display: flex;
        justify-content: flex-start;
        height: 5vh;
        flex-direction: column;
        align-items: center;
        border: 1px solid gray;
        border-radius: 1em;
        background-color: lightgrey;
        width: 35%;
    }

    .received-message-text {
        width: 30%;
        font-size: 30px;
        word-wrap: break-word;
        padding-top: 5px;
        padding-left: 10px;
        display: flex;
        flex-direction: column; 
        align-items: flex-end;
        justify-content: flex-start;  
    }

    .received-sending-time-container { 
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }

    .received-sending-time {
        padding-right: 20px;
        font-size: 20px;
        justify-content: flex-end;
        align-self: flex-end;
        width: 100%;
    } */

</style>

<!-- <MyMessage :text="MyText"/>
            <MyReceivedMessage :text="ReceivedText"/> -->
            
            <!-- v-for="message in messages" :key="message.id" @click="message.messageClickListener" -->
        <!-- <div class="dialog-container">  -->
            <!-- <MyMessageFinal :isReaded="false"/>
            <MyReceivedMessageFinal/> -->

            

            <!-- <div v-if="message.senderName === currUser" class="my-message">
                {{ message.text }}
                <div class="sending-time">{{ message.sendingTime }}</div>
            </div>
            <div v-else class="received-message">
                <div class="received-message-header">
                    <img class="profile-photo" src="" alt="Profile Photo">
                    <div class="sender-name">{{ message.senderName }}</div>
                </div>
                {{ message.text }}
                <div class="received-sending-time">{{ message.sendingTime }}</div>
            </div> -->

            <!------------------------------------------------------------------------------------------------------->


            <!-- <MyMessage text="text of message" :sending-time="new Date('December 17, 1995 03:24:00')"
            :messageClickListener="messageClickListener"/>
            <MyReceivedMessage text="text of message" :sending-time="new Date('December 17, 1995 03:24:00')" sender-name="Nikita" profile-photo=""/> -->
            <!-- <MyMessage v-for="message in messages" :key="message.id" :text="message.text" :sending-time="message.sendingTime"
            v-if="message.senderName === 'Slava'"></MyMessage>
            <MyReceivedMessage v-else v-for="message in messages" :key="message.id" :text="message.text" :sending-time="message.sendingTime"
            :sender-name="message.senderName" profile-photo=""></MyReceivedMessage> -->