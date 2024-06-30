<template>
    <div class="container">
        <div class="users">
                    <div class="users-title">Ожидающие запросы</div>
                    <div class="user" v-for="user in users" :key="user.id">
                        <div class="img-user">
                            <img src="" alt="IMAGE">
                        </div>
                        <div class="name-user">{{ user.username }}</div>
                        <button @click="acceptPendingRequest">Принять</button>
                        <button @click="rejectPendingRequest">Отклонить</button>
                    </div>
                </div>
    </div>
</template>

<script>
    import { getPendReqWebsocket } from '@/websocket'
    export default {
        data() {
            return {
                users: [
                    // {
                    //     userId:
                    //     username: 
                    //     userEmail:
                    // }
                ],
                socket: null,
                currUserIdPendReq: 0,
                currUsernamePendReq: '',
            }
        },

        methods: {

            acceptPendingRequest() {
                this.socket.send(JSON.stringify({
                    'payload': {'request': 'acceptPendingRequestForTeam', 'params': {
                        'user_id': this.currUserIdPendReq,
                        'team_id': Number(localStorage.getItem('currTeamId')),
                        'username': this.currUsernamePendReq,
                }
            }
                }))
            },

            rejectPendingRequest() {

            }

        },

        created() {
            localStorage.setItem('currTeamId', 1)
            this.socket = getPendReqWebsocket()
            this.socket.onmessage = (event) => {
                console.log("FROM ON MESSAGE (POST WEBSOCKET)", event.data)
                const dataJson = JSON.parse(event.data)
                console.log("DATAJSON (POST WEBSOCKET)", dataJson['request'])
                if(dataJson['request'] == 'getPendingRequestsForTeam') {
                    this.users = dataJson['params']
                }
            }
            setTimeout(() => {
                this.socket.send(JSON.stringify({
                'payload': {'request': 'getPendingRequestsForTeam', 'params': {
                    'team_id': Number(localStorage.getItem('currTeamId'))
                }
            }
            }))
            }, 3000);
        }
    }
</script>