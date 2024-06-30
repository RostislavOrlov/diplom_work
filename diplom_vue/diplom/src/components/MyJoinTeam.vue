<script>
    import MyNavbar from './MyNavbar.vue';
    import { getJoinTeamWebsocket, initJoinTeamWebsocket, getPreferredTeam } from '@/websocket';
    export default {
        data() {
            return {
                isApplyClicked: false,
                teamId: 0,
                name: '', 
                description: ''
            }
        },

        components: {
            MyNavbar
        },

        methods: { 
            getTeamByReference() {
                this.isApplyClicked = true
                let websocket = getJoinTeamWebsocket()
                websocket.send(JSON.stringify({'payload': {'request': 'getTeamByReference', 'params': {'team_code': this.teamCode}}}))
                setTimeout(() => {
                    let team = getPreferredTeam()
                    this.teamId = team.id
                    this.name = team.name
                    this.description = team.description
                }, 2000);
            },
        //     applyJoinTeam() {
        //         fetch(`http://localhost:8000/teams/${localStorage.getItem('userId')}`, {
        //                     method: 'GET',
        //                     headers: {
        //                         "Content-Type": "application/json"
        //                     },
        //                 })
        //                 .then(response => response.json())
        //                 .then(data => {
        //                     console.log(data);
        //                     const dataJson = JSON.parse(data['result'])
        //                     this.teams = dataJson['teams']
        //                 })
        // },   
            applyJoinTeam() {
                let websocket = getJoinTeamWebsocket()
                websocket.send(JSON.stringify({'payload': {'request': 'applyJoinTeam', 'params': {'user_id': Number(localStorage.getItem('userId')), 
                'username': localStorage.getItem('userName'), 'email': localStorage.getItem('userEmail'), 'team_id': this.teamId}}}))
            }
    },

        created() {
            initJoinTeamWebsocket()
        }
    }
</script>

<template>
    <MyNavbar/>
    <div class="join-team-container">
        <div class="title">Вступить в команду</div>
        <div class="code-container">
            <div>Код</div>
            <input v-model="teamCode">
        </div>
        <button @click="getTeamByReference">Вступить</button>
        <div v-if="isApplyClicked" class="preferred-team">
            <div class="text">Вы хотите вступить в команду:</div>
            <div class="name">{{ name }}</div>
            <button @click="applyJoinTeam">Подать заявку</button>
        </div>
    </div>
</template>

<style scoped>
    .preferred-team {
        top: 0;
        left: 0;
        width: 50%;
        height: 50%;
        background-color: lightgreen;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

</style>