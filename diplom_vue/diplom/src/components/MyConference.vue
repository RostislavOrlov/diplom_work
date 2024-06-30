<script setup>

import { getOwnerWebsocket } from '@/websocket'

let localVideo = document.getElementById('video-user')
let remoteVideo = document.querySelector('#remoteVideo')

let otherUser;
let remoteRTCMessage;

let iceCandidatesFromCaller = [];
let peerConnection;
let remoteStream;
let localStream;

//event from html
function call() {
    console.log(localVideo)
    let userToCall = 'test3'
    otherUser = userToCall;

    beReady()
    .then(() => {
            processCall(userToCall);
        })
}

function beReady() {
    return navigator.mediaDevices.getUserMedia({
        audio: true,
        video: true
    })
        .then(function(stream) {
            alert("before localStream = stream")
            localStream = stream;
            // localVideo.srcObject = stream;
            console.log(stream)
            return createConnectionAndAddStream()
            // return true
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}

function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    // alert("TEST2")
    return true;
}

//event from html
function answer() {
    
    beReady()
        .then(() => {
            processAccept();
        })

    // document.getElementById("answer").style.display = "none";
}

let pcConfig = {
    "iceServers":
        [
            // { "url": "stun:stun.jap.bloggernepal.com:5349" },
            // {
            //     "url": "turn:turn.jap.bloggernepal.com:5349",
            //     "username": "guest",
            //     "credential": "somepassword"
            // },
            {"url": "stun:stun.l.google.com:19302"}
        ]
};

/////////////////////////////////////////////

// let socket;
let callSocket;
function connectSocket() {
    // createPeerConnection()
    let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";
    console.log(ws_scheme);

    callSocket = new WebSocket('ws://localhost:8086/ws/conf/');

    callSocket.onopen = () =>{
    //let's send myName to the socket
        callSocket.send(JSON.stringify({
            type: 'login',
            data: {
                name: localStorage.getItem('userName')
            }
        }));
    }

    callSocket.onmessage = (e) =>{
        let response = JSON.parse(e.data);

        // console.log(response);

        let type = response.type;

        if(type == 'connection') {
            console.log(response.data.message)
        }

        if(type == 'call_received') {
            // console.log(response);
            onNewCall(response.data)
        }

        if(type == 'call_answered') {
            onCallAnswered(response.data);
        }

        if(type == 'ICEcandidate') {
            onICECandidate(response.data);
        }
    }

    const onNewCall = (data) =>{
        //when other called you
        //show answer button

        otherUser = data.caller;
        remoteRTCMessage = data.rtcMessage

        console.log(otherUser)
        console.log(remoteRTCMessage)

        // document.getElementById("profileImageA").src = baseURL + callerProfile.image;
        // document.getElementById("callerName").innerHTML = otherUser;
        // document.getElementById("call").style.display = "none";
        // document.getElementById("answer").style.display = "block";
        console.log("ON NEW CALL")
    }

    const onCallAnswered = (data) =>{
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        console.log("onCallAnswered")
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        // document.getElementById("calling").style.display = "none";

        console.log("Call Started. They Answered");
        // console.log(pc);
        console.log("ON CALL ANSWERED")
    }

    const onICECandidate = (data) =>{
        // console.log(data);
        console.log("GOT ICE candidate");

        let message = data.rtcMessage

        let candidate = new RTCIceCandidate({
            sdpMLineIndex: message.label,
            candidate: message.candidate
        });

        if (peerConnection) {
            console.log("ICE candidate Added");
            peerConnection.addIceCandidate(candidate);
        } else {
            console.log("ICE candidate Pushed");
            iceCandidatesFromCaller.push(candidate);
        }

    }

}

function sendCall(data) {
    //to send a call
    console.log("Send Call");

    // socket.emit("call", data);
    callSocket.send(JSON.stringify({
        type: 'call',
        data
    }));
}

function answerCall(data) {
    //to answer a call
    // socket.emit("answerCall", data);
    callSocket.send(JSON.stringify({
        type: 'answer_call',
        data
    }));
}

function sendICEcandidate(data) {
    //send only if we have caller, else no need to
    console.log("Send ICE candidate");
    // socket.emit("ICEcandidate", data)
    callSocket.send(JSON.stringify({
        type: 'ICEcandidate',
        data
    }));

}

function processCall(userName) {
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            name: userName,
            rtcMessage: sessionDescription
        })
    }, (error) => {
        console.log("Error", error);
    });
}

function processAccept() {
    // processCall()
    console.log("Process Accept")
    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));
    peerConnection.createAnswer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);

        if (iceCandidatesFromCaller.length > 0) {
            for (let i = 0; i < iceCandidatesFromCaller.length; i++) {
                //
                let candidate = iceCandidatesFromCaller[i];
                console.log("ICE candidate Added From queue");
                try {
                    peerConnection.addIceCandidate(candidate).then(done => {
                        console.log(done);
                    }).catch(error => {
                        console.log(error);
                    })
                } catch (error) {
                    console.log(error);
                }
            }
            iceCandidatesFromCaller = [];
            console.log("ICE candidate queue cleared");
        } else {
            console.log("NO Ice candidate in queue");
        }

        answerCall({
            caller: otherUser,
            rtcMessage: sessionDescription
        })

    }, (error) => {
        console.log("Error", error);
    })
}

/////////////////////////////////////////////////////////

function createPeerConnection() {
    try {
        peerConnection = new RTCPeerConnection(pcConfig);
        console.log('Created RTCPeerConnnection without listeners');
        // peerConnection = new RTCPeerConnection();
        peerConnection.onicecandidate = handleIceCandidate;
        peerConnection.onaddstream = handleRemoteStreamAdded;
        peerConnection.onremovestream = handleRemoteStreamRemoved;
        console.log('Created RTCPeerConnnection');
        return;
    } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
}

function handleIceCandidate(event) {
    // console.log('icecandidate event: ', event);
    if (event.candidate) {
        console.log("Local ICE candidate");
        // console.log(event.candidate.candidate);

        sendICEcandidate({
            user: otherUser,
            rtcMessage: {
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteStream = event.stream;
    remoteVideo.srcObject = remoteStream;
}

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed. Event: ', event);
    remoteVideo.srcObject = null;
    localVideo.srcObject = null;
}

// window.onbeforeunload = function () {
//     if (callInProgress) {
//         stop();
//     }
// };


// function stop() {
//     localStream.getTracks().forEach(track => track.stop());
//     callInProgress = false;
//     peerConnection.close();
//     peerConnection = null;
//     otherUser = null;
// }

// function callProgress() {

//     // document.getElementById("videos").style.display = "block";
//     // document.getElementById("otherUserNameC").innerHTML = otherUser;
//     // document.getElementById("inCall").style.display = "block";

//     callInProgress = true;
// }
// import { getConfWebsocket } from '@/websocket';
import { onMounted, ref } from 'vue';
let allParticipants = ref([])
// let currUsername = localStorage.getItem('userName')
// let currEmail = localStorage.getItem('userEmail')
let admins = ref([
{
        userId: 2,
        username: "Петр Иванов1",
        user_email: "email_1@ex.com"
    },
    {
        userId: 3,
        username: "Петр Иванов2",
        user_email: "email_2@ex.com"
    },
    {
        userId: 4,
        username: "Петр Иванов3",
        user_email: "email_3@ex.com"
    },
    {
        userId: 7,
        username: "Петр Иванов7",
        user_email: "email_7@ex.com"
    },
    
    
])
let notAdmins = ref([
{
        userId: 5,
        username: "Петр Иванов4",
        user_email: "email_4@ex.com"
    },
    {
        userId: 6,
        username: "Петр Иванов5",
        user_email: "email_5@ex.com"
    },
    {
        userId: 7,
        username: "Петр Иванов6",
        user_email: "email_6@ex.com"
    },
])
let usersWaitingHall = ref([
    {
        userId: 8,
        username: "Петр Иванов8",
        user_email: "email_5@ex.com"
    },
    {
        userId: 9,
        username: "Петр Иванов9",
        user_email: "email_6@ex.com"
    },
])
let otherUsers = ref([
    {
        userId: 2,
        username: "Петр Иванов1",
        user_email: "email_1@ex.com"
    },
    {
        userId: 3,
        username: "Петр Иванов2",
        user_email: "email_2@ex.com"
    },
    {
        userId: 4,
        username: "Петр Иванов3",
        user_email: "email_3@ex.com"
    },
    {
        userId: 5,
        username: "Петр Иванов4",
        user_email: "email_4@ex.com"
    },
    {
        userId: 6,
        username: "Петр Иванов5",
        user_email: "email_5@ex.com"
    },
    {
        userId: 7,
        username: "Петр Иванов6",
        user_email: "email_6@ex.com"
    },
    
])
function fetchUsersForMeeting() {
    console.log('fetchUsersForMeeting')
    fetch(`http://localhost:8086/api/fetch_users_for_meeting`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    // meeting_id: Number(localStorage.getItem('currMeetingId'))
                    meeting_id: Number(localStorage.getItem('currMeetingId')),
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                for(let i = 0; i < data.length; i++) {
                    if(data[i]['user_id'] != Number(localStorage.getItem('userId'))) {
                        otherUsers.value.push({
                            userId: data[i]['user_id'],
                            username: data[i]['username'],
                            user_email: data[i]['user_email'],
                            userImgRef: data[i]['user_img_ref'],
                            userRole: data[i]['user_role'],
                        });
                    }
                    allParticipants.value.push({
                        userId: data[i]['user_id'],
                        username: data[i]['username'],
                        user_email: data[i]['user_email'],
                        userImgRef: data[i]['user_img_ref'],
                        userRole: data[i]['user_role']
                    })
                    if(data[i]['user_role'] == 'MeetingRole.PARTICIPANT') {
                        notAdmins.value.push({
                            userId: data[i]['user_id'],
                            username: data[i]['username'],
                            user_email: data[i]['user_email'],
                            userImgRef: data[i]['user_img_ref'],
                            userRole: data[i]['user_role']
                    })
                    }
                    else {
                        admins.value.push({
                            userId: data[i]['user_id'],
                            username: data[i]['username'],
                            user_email: data[i]['user_email'],
                            userImgRef: data[i]['user_img_ref'],
                            userRole: data[i]['user_role']
                    })
                    }
                }
                console.log("otherUsers", otherUsers);
                console.log("allParticipants", allParticipants)
                console.log("notAdmins", notAdmins);
            })
            .catch(error => {
            console.error(error);
            })
}
function joinMeeting() {
    console.log('joinMeeting')
    console.log("MEETING ID FROM CONFERENCE", localStorage.getItem('currMeetingId'))
    fetch(`http://localhost:8086/api/join_user_meeting`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            meeting_id: Number(localStorage.getItem('currMeetingId')),
            user_id: Number(localStorage.getItem('userId')),
            username: localStorage.getItem('userName'),
            user_email: localStorage.getItem('userEmail'),
            user_img_src: '',
            user_role: 'Участник'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
    console.error(error);
    })
            }
function shareScreen() {
    navigator.mediaDevices.getDisplayMedia({ video: true, audio: true })
        .then((stream) => {
            document.getElementById('video-user').srcObject = stream
        })
        .catch((error) => {
            console.error("Error sharing screen:", error)
        })
}

// import { defineModel } from 'vue'
// let socket;
// let newMessage = defineModel()

// function fetchMessagesOfChat() {
//     socket.send(JSON.stringify({
//         'type': 'fetchMessagesOfChat',
//         'data': {
//             meeting_id: Number(localStorage.getItem('currMeetingId'))
//         }
//     }))
// }

let ownerSocket = null

onMounted(() => {
    console.log("MyConference mounted")
    // socket = getConfWebsocket()
    connectSocket()
    joinMeeting()
    setTimeout(() => {
        fetchUsersForMeeting()
    }, 2000);

    ownerSocket = getOwnerWebsocket(localStorage.getItem('userName'))
    ownerSocket.onmessage = (event) => {
        console.log("OWNER SOCKET DATA", event.data)
        let data = event.data
        let dataJson = JSON.parse(data)
        if(dataJson['request'] == 'joinConfFromWaitingHall') {
            usersWaitingHall.value.push({
                userId: dataJson['params']['user_id'],
                username: dataJson['params']['username'],
            })
        }
    }
    // setTimeout(() => {
    //     fetchMessagesOfChat()
    // }, 2500);
    // socket.onmessage = (event) => {
    //     console.log(event.data)
    //     let data = event.data
    //     if(data['type'] == 'sendMessageToEveryone') {
    //         let message = data['data']
    //         messages.push({
    //             message_id: message['message_id'],
    //             chat_id: message['chat_id'],
    //             message_text: message['message_text'],
    //             sender_id: message['sender_id'],
    //             sender_name: message['sender_name'],
    //             sender_img_src: message['sender_img_src'],
    //         })
    //     }
    //     else if(data['type'] == 'fetchMessagesOfChat') {
    //         for(let i = 0; i < data['data'].length; i++) {
    //             let message = data['data'][i]
    //             messages.push({
    //                 message_id: message['message_id'],
    //                 chat_id: message['chat_id'],
    //                 message_text: message['message_text'],
    //                 sender_id: message['sender_id'],
    //                 sender_name: message['sender_name'],
    //                 sender_img_src: message['sender_img_src'],
    //             })
    //         }
    //     }
    // }
})

// function sendMessage() {
//     socket.send(JSON.stringify({
//             'type': 'sendMessageToEveryone',
//             'data': {
//                 'chat_id': 1,
//                 'meeting_id': 1,
//                 'to_everyone': true,
//                 'receiver_name': 'all',
//                 'message_text': newMessage,
//                 'sender_id': Number(localStorage.getItem('userId')),
//                 'sender_name': localStorage.getItem('userName'),
//                 'sender_img_src': ''
//             }
//         }))
// }
</script>

<template>
    <div class="conference-container">
        <div class="navbar-and-users">
        <div class="conference-navbar">
            <div class="item1" @click="call()">Вкл звук</div>
            <div class="item2" @click="answer()">Вкл видео</div>
            <div class="item3" @click="fetchUsersForMeeting()">Участники</div>
            <!-- <div class="item4" @click="test2">Чат</div> -->
            <div class="item5" @click="shareScreen()">Демонстрация экрана</div>
            <!-- <div class="item6">Запись</div> -->
            <!-- <div class="item7">Сессионные залы</div> -->
            <!-- <div class="item8" @click="start">Еще</div> -->
            <!-- <div class="item9">Выйти</div> -->
        </div>
        <div class="user-and-more-users">
        <div class="conference-users">
            <!-- <div class="one-user-or-leading"> -->
                <video id="video-user" autoplay="true" playsinline="true"></video>
                <div class="user-details">
                    <div class="user-username">Петр Иванов 7</div>
                    <div class="user-email">email_7@ex.com</div>
                </div>
            <!-- </div> -->
            <!-- <div class="meet-other-users-title">Пригласите других участников</div> -->
            <!-- ОДНО ИЗ ДВУХ (ИЛИ НЕТ) -->
        </div>
        <div class="more-users">
            <div v-for="user in otherUsers" :key="user.userId">
            <div class="current-user">
                <div class="other-user-details">
                    <div class="other-user-username">{{ user.username }}</div>
                    <div class="other-user-email">{{ user.user_email }}</div>
                </div>
            </div>
        </div>
        </div>
    </div>
    </div>
    <div class="conference-users-window">
        <!-- <div class="users-window-navbar">
            <div class="users-window-navbar-title-and-cancel">
                <div class="users-window-navbar-title">Участники</div>
                <div class="users-window-navbar-cancel">K</div>
            </div>
            <div class="users-window-navbar-functions">
                <div class="users-window-navbar-copy-link">
                    <div class="users-window-navbar-copy-link-img">
                        <img src="" alt="1">
                    </div>
                    <div class="users-window-navbar-copy-link-title">Скопировать ссылку</div>
                </div>
                <div class="users-window-navbar-add-users">
                    <div class="users-window-navbar-add-users-img">
                        <img src="" alt="2">
                    </div>
                    <div class="users-window-navbar-add-users-title">Добавить участников</div>
                </div>
                <div class="users-window-navbar-user-permissions">
                    <div class="users-window-navbar-user-permissions-img">
                        <img src="" alt="3">
                    </div>
                    <div class="users-window-navbar-user-permissions-title">Доступы участников</div>
                </div>
            </div>
        </div> -->
        <MyUsersNavbarVue/>
        <div class="users-window-search">
            <input placeholder="Поиск..." class="users-window-search-input">
        </div>
        <div class="users-window-admins">
            <div class="users-window-admins-meta">
                <div class="users-window-admins-title">Администраторы</div>
                <div class="users-window-admins-count">{{ admins.length }}</div>
        </div>
            <div class="users-window-admins-people" v-for="admin in admins" :key="admin.userId">
                <!-- <div class="users-window-admins-people-img"></div> -->
                <div class="users-window-admins-people-fullname">{{ admin.username }}</div>
                <div class="users-window-admins-people-email">({{ admin.user_email }})</div>
                <!-- <div class="users-window-admins-people-audio"></div>
                <div class="users-window-admins-people-video"></div>
                <div class="users-window-admins-people-more"></div> -->
            </div>
        </div>
        <div class="users-window-users">
            <div class="users-window-users-meta">
                <div class="users-window-users-title">Участники</div>
                <div class="users-window-users-count">{{ notAdmins.length }}</div>
        </div>
        <div class="users-window-users-people" v-for="user in notAdmins" :key="user.userId">
                <!-- <div class="users-window-users-people-img"></div> -->
                <div class="users-window-users-people-fullname">{{ user.username }}</div>
                <div class="users-window-users-people-email">({{ user.user_email }})</div>
                <!-- <div class="users-window-users-people-audio"></div>
                <div class="users-window-users-people-video"></div>
                <div class="users-window-users-people-more"></div> -->
            </div>
        </div>
        <div class="users-window-users-waiting-hall">
            <div class="users-window-users-waiting-hall-meta">
                <div class="users-window-users-waiting-hall-title">В зале ожидания</div>
                <div class="users-window-users-waiting-hall-count">3</div>
        </div>
        <div class="users-window-users-waiting-hall" v-for="user in usersWaitingHall" :key="user.userId">
                <!-- <div class="users-window-users-people-img"></div> -->
                <div class="users-window-users-people-fullname">{{ user.username }}</div>
                <div class="users-window-users-people-email">{{ user.user_email }}</div>
                <!-- <div class="users-window-users-people-audio"></div>
                <div class="users-window-users-people-video"></div>
                <div class="users-window-users-people-more"></div> -->
            </div>
        </div>
    </div>
    <!-- <div class="conference-chat-window">
        <div class="conference-chat-window-navbar">Чат конференции</div>
        <div class="conference-chat-window-dialog">
            <div class="message" v-for="message in messages" :key="message.id">
                <div class="message-sender-details">
                    <div class="message-sender-img">
                        <img src="" alt="userImg">
                    </div>
                    <div class="message-sender-username">{{ message.senderName }}</div>
                </div>
                <div class="message-text">{{ message.messageText }}</div>
                <div class="message-date">{{ message.messageDate }}</div>
            </div>
        </div>
        <div class="conference-chat-window-message-input">
            <div class="conference-chat-window-message">
                <input v-model="newMessage">
            </div>
            <button @click="sendMessage">Отправить</button>
        </div>
    </div> -->
</div>
</template>

<style scoped>

    .users-window-users-waiting-hall {
        display: flex;
        width: 100%;
        height: 5vh;
        padding-left: 15px;
        margin-top: 3%;
        margin-bottom: 3%;
    }


    .users-window-users-people-fullname {

    }

    .users-window-users-people {
        display: flex;
        width: 100%;
        height: 5vh;
        padding-left: 24px;
    }

    .users-window-users-people-fullname {
        width: 27%;
    }

    .users-window-users-people-email {
        color: gray;
    }

    .users-window-users-title {
        padding-bottom: 3%;
    }

    .users-window-users-waiting-hall-title {
        padding-bottom: 3%;
    }

    .video-user {
        width: 100%;
        height: 100%;
    }

    .user-details {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-end;
        width: 20%;
        height: 2vh;
    }

    .message-date {
        width: 100%;
        text-align: end;
        height: 4vh;
    }

    .message-text {
        word-wrap: break-word;
        padding-top: 5%;
    }

    .message-sender-details {
        display: flex;
        width: 100%;
        height: 1vh;
        /* align-items: flex-start; */
    }

    .conference-chat-window-dialog {
        display: flex;
        flex-direction: column;
        overflow-y: scroll;
        scrollbar-width: none;
        height: 50vh;
        justify-content: flex-end;
    }

    .message {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        width: 100%;
        height: fit-content;
        /* padding-top: 5vh; */
        /* margin-bottom: 5vh; */
        background-color: aqua;
        border-radius: 10%;
    }

    #video-user {
        width: 100%;
        height: 100%;
    }
    .conference-container {
        display: flex;
    }

    .conference-navbar {
        display: flex;
        justify-content: space-around;
        align-items: end;
        height: 7vh;
        width: 100%;
        background-color: lightgreen;
    }

    .conference-users-window {
        width: 30%;
        height: 100vh;
        /* background-color: plum; */
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .navbar-and-users {
        display: flex;
        flex-direction: column;
        width: 70%;
        height: 100vh;
        /* background-color: darkslategray; */
    }

    .conference-users {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-end;
        height: 90vh;
        background-color: rgb(36, 31, 34);
    }


    .user-details {
        padding-right: 2px;
        padding-bottom: 2px;
    }

    .user-username {
        color: white;
    }

    .user-email {
        color: lightgray;
    }

    /* .one-user-or-leading {
        width: 100%;
        height: 100%;
        border: 2px solid plum;
    } */
    
    .meet-other-users-title {
        font-size: 40px;
    }

    .more-users {
        display: flex;
        justify-content: flex-start;
        align-self: flex-end;
        background-color: lightgreen;
        width: 100%;
        height: 20vh;
    }

    .user-and-more-users {
        display: flex;
        flex-direction: column;
        height: 93vh;
    }

    .current-user {
        height: 100%;
        width: 150px;
        background-color: rosybrown;
        border: 4px solid rgb(91, 78, 93);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-end;
        background-color: rgb(36, 31, 34); 
    }

    .other-user-details {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-end;
        width: 100%;
        height: 2vh;
        
    }

    .other-user-username {
        color: white;
    }

    .other-user-email {
        color: lightgray;
    }

    /* .users-window-navbar {
        display: flex;
        flex-direction: column;
        background-color: rgb(235, 229, 229);
        height: 30vh;
    }

    .users-window-navbar-title-and-cancel {
        display: flex;
    }

    .users-window-navbar-title {
        font-size: 20px;
        text-align: center;
        width: 95%;
    }

    .users-window-navbar-cancel {
        font-size: 20px;
        align-self: flex-end;
        width: 5%;
    }

    .users-window-navbar-functions {
        display: flex;
        justify-content: space-around;
        height: 30vh;
        padding-top: 15%;
    }

    .users-window-navbar-copy-link {
        background-color: plum;
        width: 15vh;
        height: 15vh;
        display: flex;
        flex-direction: column;
        text-align: center;
        
    }
 
    .users-window-navbar-add-users {
        background-color: yellow;
        width: 15vh;
        height: 15vh;
        display: flex;
        flex-direction: column;
        text-align: center;
    }

    .users-window-navbar-user-permissions {
        background-color: yellowgreen;
        width: 15vh;
        height: 15vh;
        display: flex;
        flex-direction: column;
        text-align: center;
    } */

    .users-window-search {
        width: 90%;
        height: 3vh;
        padding-top: 2%;
        /* justify-content: center; */
    }
    
    .users-window-search-input {
        width: 100%;
    }

    .users-window-admins {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: fit-content;
    }

    .users-window-admins-meta {
        width: 100%;
        display: flex;
        justify-content: center;
        padding-top: 5px;
    }

    .users-window-admins-title {
        
        /* text-align: start; */
        /* align-self: flex-start; */
        width: 50%;
        text-align: end;
    }

    .users-window-admins-count {
        width: 50%;
        text-align: start;
        padding-left: 5px;
        color: lightgray;
    }

    .users-window-users {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: fit-content;
    }

    .users-window-users-meta {
        width: 100%;
        display: flex;
        justify-content: center;
        padding-top: 5px;
    }

    .users-window-users-title {
        
        /* text-align: start; */
        /* align-self: flex-start; */
        width: 50%;
        text-align: end;
    }

    .users-window-users-count {
        width: 50%;
        text-align: start;
        padding-left: 5px;
        color: lightgray;
    }

    .users-window-users-waiting-hall {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: fit-content;
    }

    .users-window-users-waiting-hall-meta {
        width: 100%;
        display: flex;
        justify-content: center;
        padding-top: 5px;
    }

    .users-window-users-waiting-hall-title {
        
        /* text-align: start; */
        /* align-self: flex-start; */
        width: 50%;
        text-align: end;
    }

    .users-window-users-waiting-hall-count {
        width: 50%;
        text-align: start;
        padding-left: 5px;
        color: lightgray;
    }

    .users-window-admins-people {
        display: flex;
        justify-content: flex-start;
        width: 90%;
        /* background-color: red; */
        height: 5vh;
        align-self: center;
        align-items: center;
    }

    .users-window-admins-people-img {
        width: 10%;
    }

    .users-window-admins-people {
        padding: 5px;
        /* border-top: 1px solid gray;
        border-bottom: 1px solid gray; */
    }

    .users-window-users-people {
        display: flex;
    }

    .users-window-admins-people-fullname {
        width: 30%;
        
    }

    .users-window-admins-people-email {
        color: gray;
    }

    .users-window-admins-people-audio {
        width: 6%;
    }

    .users-window-admins-people-video {
        width: 6%;
    }

    .users-window-admins-people-more {
        width: 6%;
    }

    .conference-chat-window {
        display: flex;
        flex-direction: column;
        height: 100vh;
        text-align: center;
    }

    .conference-chat-window-navbar {
        height: 7vh;
        text-align: center;
    }

    .conference-chat-window-dialog {
        height: 77vh;
        /* background-color: red; */
        border-bottom: 3px solid lightgray;
    }

    .conference-chat-window-message-input {
        display: flex;
        flex-direction: column;
    }

    .conference-chat-window-message-input-to {
        height: 30%;
    }

</style>
