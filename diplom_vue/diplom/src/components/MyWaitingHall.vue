<script>
import { getPeerConnection, initPeerConnection } from '@/webrtc';
import { getOwnerWebsocket } from '@/websocket'


// function start() {
//     var config = {
//         sdpSemantics: 'unified-plan'
//     };

//     pc = new RTCPeerConnection(config);

//     // connect audio / video
//     pc.addEventListener('track', function(evt) {
//         if (evt.track.kind == 'video') {
//             document.getElementById('video2').srcObject = evt.streams[0];
//         } else {
//             document.getElementById('audio2').srcObject = evt.streams[0];
//         }
//     });
// }

export default {
    data() {
        return {
            pc: null,
            socket: null,
            ownerSocket: null
        }
    },
    methods: {
        createPeerConnection,
        negotiate,
        start,
        joinConf() {
            this.ownerSocket.send(JSON.stringify({
                type: 'a',
                data: {
                    meeting_id: Number(localStorage.getItem('currMeetingId')), 
                    user_id: Number(localStorage.getItem('userId')),
                    username: localStorage.getItem('userName'),
                    user_email: localStorage.getItem('userEmail'),
                    user_img_ref: localStorage.getItem('user_img_ref'),
                    user_registrant_username: localStorage.getItem('user_registrant_username')
                }
                
            }))
        }
    },
    created() {
        // this.socket = getConfContainerWebsocket()
        // this.socket.onmessage = (event) => {
        //     console.log(event.data)
        // }
        this.ownerSocket = getOwnerWebsocket(localStorage.getItem('userName'))
        this.ownerSocket.onmessage = (event) => {
            console.log("OWNER SOCKET DATA", event.data)
        }
        setTimeout(() => {

            this.ownerSocket.send(JSON.stringify({
                type: 'login',
                data: {
                    name: localStorage.getItem('userName')
                }
            }))

            setTimeout(() => {
                this.ownerSocket.send(JSON.stringify({
                type: 'login',
                data: {
                    name: localStorage.getItem('userName')
                }
            }))
                setTimeout(() => {
                    this.joinConf()
                }, 2000); 
            }, 2000);
        }, 2000);
    }
}

// peer connection
var pc;

// data channel
// var dc = null, dcInterval = null;

function createPeerConnection() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    initPeerConnection(config);
    var pc = getPeerConnection();

    return pc;
}

function negotiate() {
    // alert("TEST")
    return pc.createOffer().then(function(offer) {
        // alert("TEST")
        return pc.setLocalDescription(offer);
    }).then(function() {
        var offer = pc.localDescription;
        return fetch('http://localhost:8000/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
                user_id: 1,
                meeting_id: 1,
                // video_transform: document.getElementById('video-transform').value
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        // document.getElementById('answer-sdp').textContent = answer.sdp;
        return pc.setRemoteDescription(answer);
    }).catch(function(e) {
        alert("ОШИБКА " + e);
    });
}

var dataChannel = null;

function start() {
    // document.getElementById('start').style.display = 'none';
    

    pc = createPeerConnection();

    var constraints = {
        audio: true,
        video: true
    };

    pc.addEventListener('track', function(evt) {
        if (evt.track.kind == 'video') {
            document.getElementById('video2').srcObject = evt.streams[0];
        } else {
            document.getElementById('audio2').srcObject = evt.streams[0];
        }
    });

    dataChannel = pc.createDataChannel('userDataChannel');
    dataChannel.addEventListener('open', () => {
        var message = 'ping';
        dataChannel.send(message)
    })

    dataChannel.addEventListener('message', (event) => {
        if(event.data == 'pong') {
            console.log(event.data)
        //  } else {
        //      if (event.data == 'video-off') {
        //          userTracks.forEach(function(track) {
        //              if(track.kind == 'video') {
                        
        //              }
        //          })
        //      }
        }
    })
    // alert("TEST")
    
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        //alert("TEST")
        stream.getTracks().forEach(function() {
            alert("TEST")
            document.getElementById('video2').srcObject = stream;

            // pc.addTrack(track, stream);
        });
        // return negotiate();
     }, function(err) {
        // alert('Could not acquire media: ' + err);
        console.log(err)
    });

}
</script>

<template>
    <!-- <div class="waiting-hall-title">Зал ожидания</div> -->
    <div class="waiting-hall-container">
        <div class="participant-media">
            <audio id="audio2" autoplay="true" playsinline="true"></audio>
            <video id="video2" autoplay="true" playsinline="true"></video>
        </div>
        <div class="conference-details">
            <div class="conference-name">Название конференции</div>
            <div class="start-time">Начало: 10:00</div>
            <div class="waiting-text">Подождите, пока организатор не разрешит вам войти...</div>
            <button class="start-button" @click="start">Проверить аудио и видео</button>
        </div>
    </div>
</template>

<style scoped>

    .start-button {
        width: 20%;
    }

    .waiting-hall-container {
        display: flex;
        height: fit-content;
        width: 100%;
        height: 100vh;
        justify-content: center;
        align-items: center;
    }

    .participant-media {
        width: 30%;
        height: 30vh;
        /* background-color: green; */
        align-self: center;
    }

    #video2 {
        width: 100%;
        height: 30vh;
        /* background-color: green; */
        align-self: center;
        border: 1px solid purple;
    }

    .conference-details {
        display: flex;
        flex-direction: column;
        width: 70%;
        justify-content: center;
        height: 30vh;
        padding-left: 5%;
    }

    .conference-name {
        flex-grow: 1;
        font-size: 40px;
        font-weight: bold;
    }

    .start-time {
        flex-grow: 1;
        color: gray;
    }

    .waiting-text {
        flex-grow: 1;
    }

</style>