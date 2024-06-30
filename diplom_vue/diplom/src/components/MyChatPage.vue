<!-- <template>
    <div class="chat-list">
      <h1>Chat List</h1>
      <ul>
        <li v-for="chat in chats" :key="chat.id">{{ chat.name }}</li>
      </ul>
      <input type="text" v-model="newChatName" placeholder="Enter chat name">
      <button @click="addChat">Add Chat</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        chats: [
          { id: 1, name: "Chat 1" },
          { id: 2, name: "Chat 2" },
          { id: 3, name: "Chat 3" }
        ],
        newChatName: ""
      };
    },
    methods: {
      addChat() {
        if (this.newChatName) {
          const newChat = {
            id: this.chats.length + 1,
            name: this.newChatName
          };
          this.chats.push(newChat);
          this.newChatName = "";
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-list {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  </style>
   -->


   <!-- <template>
    <div class="chat-page">
        контейнер
    </div>
   </template>

   <style>
    .chat-page {
      flex-direction: column;
    }
  </style> -->






  <script>

  import { getChatWebsocket, getMessagesWebsocket } from '@/websocket';
import MyChat from './MyChat.vue';
    
  export default {
      data() {
        return {
          chats: [],

          socket: null,

          socketMessages: null,

          chatSearchInput: '',

          createChat: false,

          chatName: '',

          theChat: false
        }
      },

      methods: {
        toChat(chat) {
          localStorage.setItem('currChatId', chat.chat_id)
          localStorage.setItem('currChatName', chat.chat_name)
          this.$router.push(`/chats/${localStorage.getItem('currChatId')}`)
          this.theChat = true
        },

        fetchChats() {
          this.socket.send(
            JSON.stringify({
              'topic': 'fetchChatsForUser',
              'params': {
                'user_id': Number(localStorage.getItem('userId'))
              }
            }
            )
          )
        },

        toCreateChat() {
          this.createChat = true
        },

        createChatForUser() {
          this.socket = getChatWebsocket()
          this.socket.send(JSON.stringify({
            'topic': 'createChatForUser',
            'params': {
              'user_id': Number(localStorage.getItem('userId')),
              'chat_name': this.chatName
            }
          }))
          this.createChat = false
        },

        addNewChat(newChat) {
          console.log("NEW CHAT", newChat)
          // this.chats.push(
          //   {
          //     chat_name: newChat.chat_name
          //   }
          // )
        }

        // fetchUsersByContext()
      },

      components: { MyChat },

      created() {
        this.socket = getChatWebsocket()
        this.socket.onmessage = (event) => {
          console.log("data chats", event.data)
          let dataJson = JSON.parse(event.data)
          console.log("dataJson", dataJson)
          // let dataJsonParams = JSON.parse(dataJson['Params'])
          if(dataJson['Request'] == 'fetchChatsForUser') {
            this.chats = dataJson['Params'].chats
            // this.chats.push({name: "What?"})
          }
          else if(dataJson['Request'] == 'createChatForUser') {
            this.chats.push(
              {
                chat_id: dataJson['Params'].chat_id,
                chat_name: dataJson['Params'].chat_name
              }
            )
          }
          else if(dataJson['Request'] == 'joinChatForUser') {
            this.addNewChat(dataJson['Params'])
          }
        }

        this.socketMessages = getMessagesWebsocket()
        this.socketMessages.onmessage = (event) => {
          console.log("data messages (websocket of messages)", event.data)
          let dataJson = JSON.parse(event.data)
          if(dataJson['Request'] == 'sendMessageInChat') {
            console.log("SEND MESSAGE IN CHAT", dataJson['Params'])
          }
        }

        // this.chatSearchInput.addEventListener('change', function() {
        //   console.log(this.chatSearchInput)
        // })
        setTimeout(() => {
          this.fetchChats()
        }, 2000);
      }
  };
  </script>


  <template>
    <div class="chat-page" v-if="createChat == false && theChat == false">
    <div class="chat-search-container">
      <input placeholder="Поиск..." class="chat-search" v-model="chatSearchInput">
    </div>
    <button class="create-button" @click="toCreateChat">Создать чат</button>
    <!-- <div class="chat-archive"></div> -->
    <div class="chat-list" v-if="chatSearchInput == ''">
      <div v-for="chat in chats" :key="chat.id" class="chat-item" @click="toChat(chat)">
        <img :src="chat.profileImage" alt="Profile Image" class="profile-image">
        <div class="chat-details-container">
          <div class="chat-details">
            <h3 class="chat-name">{{ chat.chat_name }}</h3>
            <div class="message-details">
              <p class="me-or-not">{{ chat.isMe ? "Вы:" : "" }}</p>
              <p class="last-message">{{ chat.lastMessage }}</p>
            </div>
            <p class="last-message-time">{{ chat.sendingTime }}</p>
          </div>
          <div class="read-status">{{ chat.isAllMessagesRead }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class="create-chat" v-if="createChat && theChat == false">
    Создать чат
    <input placeholder="Введите название..." v-model="chatName">
    <button @click="createChatForUser">Создать чат</button>
  </div>
  <MyChat v-if="createChat == false && theChat" @joinChat="addNewChat(newChat)" />
    <!-- <div class="chat-list">
      <div class="chat-item" @click="chatClickListener">
        <img alt="Profile Image" class="profile-image">
        <div class="chat-details">
          <h3 class="chat-name">Имя собеседника</h3>
          <div class="message-details">
            <p class="me-or-not">Вы: </p>
            <p class="last-message">Текст</p>
          </div>
          <p class="last-message-time">10:00</p>
        </div>
      </div>
    </div> -->
  </template>
  
  
  <style scoped>

/* .chat-page {
  display: flex;
  flex-direction: column;
} */

  .create-button {
    width: 10%;
    display: flex;
    align-self: center;
    text-align: center;
  }

  .chat-list {
    display: flex;
    flex-direction: column;
    /* height: 80vh; */
    align-items: center;
    /* justify-content: center; */
  }
  
/* .chat-archive {
  width: 50%;
  height: 5vh;
  border-bottom: 1px solid #888;
  justify-content: center;
} */

  .chat-item {
    display: flex;
    align-items: center;
    width: 50%;
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }
  
  .profile-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
  }

  .chat-details-container {
    display: flex;
    justify-content: space-between;
    flex-grow: 1;
    align-items: center;
  }
  
  .chat-details {
    flex: 1;
  }
  
  .chat-name {
    font-size: 16px;
    font-weight: bold;
  }
  
  .last-message, .me-or-not {
    /* font-size: 14px; */
    color: #888;
  }
  
  .last-message {
    margin-left: 5px;
  }

  .last-message-time {
    font-size: 12px;
    color: #ccc;
  }

  .message-details {
    display: flex;

  }

  .chat-page {
    display: flex;
    flex-direction: column;
    /* align-items: center; */
  }

  .chat-search-container {
    width: 100%;
    display: flex;
    /* align-items: center; */
    justify-content: center;
    padding-top: 5px;
  }

  .chat-search {
    width: 50%;
  }


  </style>
  