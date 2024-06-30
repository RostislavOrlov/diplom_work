<script>
    import { getManageTeamWebsocket } from '@/websocket'
    export default {
        data() {
            return {
                users: [],
                admins: [],
                userAddEmail: '',
                userAddId: 0,
                userAddUsername: '',
                socket: null
            }
        },

        computed: {
            teamName() {
                return localStorage.getItem('currTeamName')
            }
        },

        methods: {
            getParticipantsForTeam() {
                var curr2 = localStorage.getItem('currTeamId')
                fetch(`http://localhost:8000/teams/${curr2}/users`, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data['result']['users']);
                    this.users = data['result']['users'].filter(usr => usr.role != 'Владелец')
                    this.admins = data['result']['users'].filter(usr => usr.role == 'Владелец')
                })
            },

            getPendingRequestsForTeam() {
                this.socket.send(JSON.stringify({
                    'payload': {
                        'request': 'getPendingRequestsForTeam',
                        'params': {
                            'team_id': Number(localStorage.getItem('currTeamId'))
                        }
                    }
                }))
            },

            deleteUserFromTeam(user) {
                var curr2 = localStorage.getItem('currTeamId')
                fetch(`http://localhost:8000/teams/${curr2}/users/${user.user_id}`, {
                    method: 'DELETE',
                    // mode: 'no-cors',
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                })
            },

            changeUserRoleInTeam(user) {
                console.log(user.role)
                if(user.role == "Владелец") {
                    user.role = "Участник"
                    this.admins = this.admins.filter(currAdmin => currAdmin.user_id != user.user_id)
                    this.users.push(
                        {
                            user_id: user.user_id,
                            role: user.role,
                            team_id: user.team_id,
                            //username: user.username
                        }
                    )
                } else {
                    user.role = "Владелец"
                    this.users = this.users.filter(currUser => currUser.user_id != user.user_id)
                    this.admins.push(
                        {
                            user_id: user.user_id,
                            role: user.role,
                            team_id: user.team_id,
                            //username: user.username
                        }
                    )
                }
                this.socket.send(JSON.stringify({
                    'payload': {
                        'request': 'changeUserRoleInTeam',
                        'params': {
                            'user_id': user.user_id,
                            'role': user.role,
                            'team_id': user.team_id
                        }
                    }
                }))
            },

            addUserForTeam() {
                this.getUserByEmail()
                setTimeout(() => {
                    console.log("DATA1", this.userAddId)
                    console.log("DATA2", this.userAddUsername)
                    console.log("DATA3", this.userAddEmail)
                    const teamId = localStorage.getItem('currTeamId')
                    const userId = localStorage.getItem('userId')
                    fetch(`http://localhost:8000/teams/${teamId}/users/${userId}`, {
                        method: 'POST',
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            id: this.userAddId,
                            username: this.userAddUsername,
                            team_id: Number(teamId)
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                    })
                }, 1000);
            },
            getUserByEmail() {
                fetch(`http://localhost:8082/api/users/`, {
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
            }
        },

        created() {
            localStorage.setItem('currTeamId', 1)
            this.socket = getManageTeamWebsocket()
            this.socket.onmessage = (event) => {
                console.log(event.data)
            }
            this.getParticipantsForTeam()
        }
    }
</script>

<template>
    <div class="manage-team">
            <div class="manage-team-navbar">
                <div class="teamName">Команда {{ teamName }}</div>
                <div class="manage-team-start">
                    <div class="manage-team-users" @click="getParticipantsForTeam">Участники</div>
                    <div class="manage-team-requests" @click="getPendingRequestsForTeam">Ожидающие запросы</div>
                    </div>
            </div>
            <div class="all-users">
                <input placeholder="Введите почту участника..." v-model="userAddEmail">
                <button @click="addUserForTeam">Добавить участника</button>
                <div class="owners">
                    <div class="owners-title">Администраторы</div>
                    <div class="owner" v-for="admin in admins" :key="admin.id" @click="deleteUserFromTeam(admin)">
                        <div class="img-owner">
                            <img src="" alt="IMAGE">
                        </div>
                        <div class="name-owner">{{ admin.role }}</div>
                    </div>
                </div>
                <div class="users">
                    <div class="users-title">Участники</div>
                    <div class="user" v-for="user in users" :key="user.id" @click="deleteUserFromTeam(user)">
                        <div class="img-user">
                            <img src="" alt="IMAGE">
                        </div>
                        <div class="name-user">{{ user.role }}</div>
                    </div>
                </div>
                </div>
            </div>
</template>

<style scoped>

    .owners {
        height: fit-content;
        width: 100%;
    }

    .users {
        height: fit-content;
        width: 100%;
    }

    .owner {
        display: flex;
        height: 7vh;
    }

    .user {
        display: flex;
        height: 7vh;
    }

    .manage-team {
        width: 100%;
        height: 95vh;
        background-color: white;
    }

    .manage-team-navbar {
        width: 100%;
        height: 7vh;
        border-bottom: 2px solid lightgray;
        display: flex;
        flex-direction: column;
    }

    .teamName {
        /* margin-bottom: 5%; */
        font-weight: bold;
        font-size: 20px;
    }
    
    .manage-team-start {
        width: 40%;
        /* align-self: flex-start; */
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .manage-team-users {
        text-align: center;
    }

    .channel-navbar-start {
        width: 40%;
        /* align-self: flex-start; */
        display: flex;
        justify-content: space-between;
    }

    .team-img {
        width: fit-content;
    }

    .channel-name {
        width: fit-content;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: large;
    }

    .img {
        padding-left: 5px;
    }

    .channel-posts {
        width: fit-content;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .channel-files {
        width: fit-content;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .channel-navbar-end {
        width: 30%;
        /* align-self: flex-end; */
        display: flex;
        justify-content: space-around;
    }
</style>