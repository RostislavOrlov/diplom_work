<script>
    import MyNavbar from './MyNavbar.vue';
    // import { ref } from 'vue';

    // const teamName = ref('');
    // const teamDescription = ref('');

    export default {
        data() {
            return {
                teamName: '',
                teamDescription: '',
            }
        },

        components: {
            MyNavbar
        },

        methods: {
            createTeam() {
                console.log("STORE USER ID2 ", localStorage.getItem('userId'))
                var curr = localStorage.getItem('userId')
                fetch(`http://localhost:8000/teams/users/${curr}`, {
                  method: 'POST',
                  headers: {
                    "Content-Type": "application/json"
                  },
                  body: JSON.stringify({
                    name: this.teamName,
                    description: this.teamDescription, 
                    img_profile_ref: '',
                    owner_username: localStorage.getItem('userName')
                })
                })
                .then(response => response.json())
                .then(data => {
                  console.log(data);
                  const obj = JSON.parse(data['result'])
                  localStorage.setItem('userTeams', obj['name'])
                  console.log("LOCAL STORAGE: ", localStorage.getItem('userTeams'))
              })
              .catch(error => {
                console.error(error);
              })
      }
        }
    }

    // var socket = null;

    // function createTeam() {
    //     socket = new WebSocket('ws://localhost:8000/ws/teams')
    //     socket.onopen = () => {
    //         console.log("Соединение установлено")
    //     }
    //     socket.onmessage = (event) => {
    //         console.log(event.data)
    //     }
    // }

</script>

<template>
    <MyNavbar/>
    <div class="create-team-container">
        <div class="title">Создать команду</div>
        <div class="team-name">
            <div class="name">Название</div>
            <div class="name-input">
                <input placeholder="Название..." v-model="teamName">
            </div>
        </div>
        <div class="team-desc">
            <div class="desc">Описание</div>
            <div class="desc-input">
                <input placeholder="Описание..." v-model="teamDescription">
            </div>
        </div>
        <button @click="createTeam()">Создать</button>
    </div>
</template>

