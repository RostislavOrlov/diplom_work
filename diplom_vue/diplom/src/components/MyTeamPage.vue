<script>
    // import { ref } from 'vue';
    import MyNavbar from './MyNavbar.vue';
    import { initTeamPageWebsocket } from '../websocket'    
    import MyProfileDetails from './MyProfileDetails.vue';

    export default {
        
        data() {
            return {
                teams: [],
                // userId: this.$store.getters.userId
            }
        },
        methods: {
            getAllTeamsForUser() {
                console.log("STORE USER ID ", localStorage.getItem('userId'))
                var curr = localStorage.getItem('userId')
                // fetch(`http://192.168.1.123:8000/teams/${curr}`, {
                    fetch(`http://localhost:8000/teams/${curr}`, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const dataJson = JSON.parse(data['result'])
                    this.teams = dataJson['teams']
                })
                // getTeamsForUser()
            },

            toTeam(team) {
                localStorage.setItem('currTeamId', team.id)
                localStorage.setItem('currTeamName', team.name)
                localStorage.setItem('currTeamDescription', team.description)
                console.log("описание", localStorage.getItem('currTeamDescription'))
                this.$router.push({path: `/teams/${team.id}`, query: {name: team.name}})
            },
        },

        created() {
            setTimeout(() => {
                this.getAllTeamsForUser();
            }, 2000);
            initTeamPageWebsocket()
            console.log("Юзернейм", localStorage.getItem('userName'))
            console.log("USER EMAIL", localStorage.getItem('userEmail'))
        },
        components: {
            MyNavbar,
            MyProfileDetails
        }
    }

    // const teams = ref([
    //     {
    //         id: 1,
    //         name: "Первая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 2,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 3,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 4,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 5,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 6,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 7,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 8,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 9,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 10,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 11,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 12,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 13,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 14,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 15,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 16,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 17,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 18,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 19,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    //     {
    //         id: 20,
    //         name: "Вторая Команда",
    //         imgSrc: ""
    //     },
    // ])

        // const teams = ref(localStorage.getItem('userTeams'))

        // var e = ref(localStorage.getItem('userTeams'))

    // function goToTeam(team) {
    //     this.$router.push(`/teams/${team.id}`)
    // }
    // this.$router.push(`/teams/${team.id}`)
    // this.$router.push({ name: `/teams/${team.id}`, params: {team: team}})
</script>

<template>
    <MyNavbar />
    <MyProfileDetails/>
        <div class="user-teams">
        <div class="padding-container">
            <div class="team-input-container">
                <input placeholder="Поиск..." class="team-input">
        </div>
            <div class="button-create-team">
                <button @click="this.$router.push(`/teams/create`)">Создать команду</button>
                <button @click="this.$router.push(`/teams/join`)">Вступить в команду</button>
            </div>
        </div>
        <div class="wrapper">
        <div class="user-teams-team" v-for="team in teams" :key="team.id">
            <div class="user-team-img">
                <img :src="team.imgSrc" alt="IMAGE">
            </div>
            <div class="user-team-name" @click="toTeam(team)">{{ team.name }}</div>
        </div>
    </div>
    </div>
</template>

<style scoped>
    .user-teams {
        width: 100%;
        height: 95vh;
        /* background-color: lightgreen; */
        background-color: white;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .padding-container {
        width: 80%;
        height: 5vh;
        display: flex;
        align-items: center;
    }

    .team-input-container {
        flex-grow: 2;
    }

    .team-input {
        width: 70%;
    }

    .button-create-team {
        flex-grow: 2;
        display: flex;
        justify-content: flex-start;
    }

    .wrapper {
        width: 80%;
        height: fit-content;
        background-color: antiquewhite;
        overflow-y: scroll;
        scrollbar-width: none;
    }

    .user-teams-team {
        width: 100%;
        height: 5vh;
        display: flex;
        /* padding-bottom: 5%; */
        align-items: center;
        border: 1px solid lightgray;
        border-radius: 5%;
    }

    .user-team-img {
        flex-grow: 1;
    }

    .user-team-name {
        flex-grow: 3;
    }
</style>