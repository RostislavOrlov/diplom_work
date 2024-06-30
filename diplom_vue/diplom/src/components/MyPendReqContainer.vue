<script setup>
import { getPendReqWebsocket } from '@/websocket';
import { onMounted, ref } from 'vue';

    let pendingRequests = ref([
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
        // {
        //     username: 'test',
        //     email: 't1@mail.ru'
        // },
    ])

    let socket;

    function acceptPendingRequest(user) {
        console.log("acceptPendingRequest")
        socket.send(JSON.stringify({
            'payload': {'request': 'acceptPendingRequestForTeam', 'params': {
                'user_id': user.user_id,
                'team_id': Number(localStorage.getItem('currTeamId')),
                'username': user.username,
                'email': user.email
        }
    }
        }))
        
        pendingRequests.value = pendingRequests.value.filter(req => req.user_id != user.user_id)
    }

    function rejectPendingRequest(user) {
        console.log("rejectPendingRequest")
        socket.send(JSON.stringify({
            'payload': {'request': 'rejectPendingRequestForTeam', 'params': {
                'user_id': user.user_id,
                'team_id': user.team_id,
                'username': user.username,
                'email': user.email
        }
    }
        }))

        pendingRequests.value = pendingRequests.value.filter(req => req.user_id != user.user_id)
    }

    function getPendingRequestsForTeam() {
        console.log("getPendingRequestsForTeam")
        socket.send(JSON.stringify({
            'payload': {'request': 'getPendingRequestsForTeam', 'params': {
                'team_id': Number(localStorage.getItem('currTeamId'))
        }
    }
        }))
    }

    onMounted(() => {
        console.log("MyPendReqContainer mounted") 
        socket = getPendReqWebsocket()
        socket.onmessage = (event) => {
            console.log(event.data)
            let dataJson = JSON.parse(event.data)
            if(dataJson['request'] == 'applyJoinTeam') {
                console.log('applyJoinTeam', dataJson['params'])
            }
            else if(dataJson['request'] == 'getPendingRequestsForTeam') {
                console.log('getPendingRequestsForTeam', dataJson['params']['requests'])
                
                let newRequests = dataJson['params']['requests']

                for(let i = 0; i < newRequests.length; i++) {
                    pendingRequests.value.push({
                        user_id: newRequests[i].user_id,
                        username: newRequests[i].username,
                        email: newRequests[i].email,
                    })
                }
            }
        }
        setTimeout(() => {
            getPendingRequestsForTeam()
        }, 2000);
    })
        
    function updatePendReqList() {
        getPendingRequestsForTeam()
    }

</script>

<template>
    <div class="pr-container">
        <button @click="updatePendReqList()">Обновить список</button>
        <div class="pr" v-for="req in pendingRequests" :key="req.user_id">
            <div class="pr-start">
            <!-- <div class="pr-img">{{ req.imgRef }}</div> -->
            <div class="pr-username">{{ req.username }}</div>
            <div class="pr-email">(почта: {{ req.email }})</div>
        </div>
            <div class="pr-end">
                <button @click="acceptPendingRequest(req)">Принять</button>
                <button @click="rejectPendingRequest(req)">Отклонить</button>
            </div>
            
        </div>
    </div>
</template>

<style scoped>

    .pr-container {
        display: flex;
        flex-direction: column;
        width: 80%;
        /* background-color: green; */
        height: fit-content;
        overflow-y: scroll;
        scrollbar-width: none;
        align-items: center;
    }

    .pr {
        display: flex;
        background-color: rgb(245, 245, 245);
        width: 100%;
        height: 7vh;
        margin: 15px;
        justify-content: flex-start;
    }

    .pr-start {
        width: 70%;
        height: 7vh;
        display: flex;
        align-items: center;
    }

    .pr-username {
        display: flex;
        text-align: center;
        padding-left: 15%;
    }

    .pr-email {
        display: flex;
        text-align: center;
        padding-left: 10%;
    }

    .pr-end {
        display: flex;
        width: 30%;
        height: 7vh;
        justify-content: flex-end;
        align-content: flex-end;
    }

</style>