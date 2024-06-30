<script >
import MyNavbar from './MyNavbar.vue';

    export default {
    data() {
        return {
            theme: '',
            cbChat: false,
            startDate: new Date(),
            startTime: new Date(), //??
            isAccessCodeExists: true,
            accessCode: '',
            rbRegistrantVideo: true,
            rbUsersVideo: false,
            waitingHall: true,
            ap1: false,
            ap2: false,
            ap3: false,
        }
    },

    components: { MyNavbar },

    methods: {
        createConf() {
            fetch("http://localhost:8086/api/v1/meetings", {
          method: 'POST',
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            theme: this.theme,
            // description: this.description,
            team_id: Number(localStorage.getItem('currTeamId')),
            user_registrant_id: Number(localStorage.getItem('userId')),
            user_registrant_username: localStorage.getItem('userName'),
            user_registrant_email: localStorage.getItem('userEmail'),
            is_launched: true,
            start_date: this.startDate,
            waiting_hall: this.waitingHall,
            users_video: this.rbUsersVideo,
            registrant_video: this.rbRegistrantVideo,
            is_access_code_exists: this.isAccessCodeExists,
            access_code: this.accessCode,
            // ap1: this.ap1,
            off_participants_voice_after_entry: this.ap2,
            // ap3: this.ap3,
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log("NEW CONFERENCE", data['meeting']);
          localStorage.setItem('currMeetingId', data['meeting'].id)
          console.log("MEETING ID", Number(localStorage.getItem('currMeetingId')))
          setTimeout(() => {
            this.$router.push({path: '/teams/team/conf/' + localStorage.getItem('currMeetingId')})
        }, 2500)
      })
      .catch(error => {
        console.error(error);
      })
        }
    }
}
</script>

<template>
    <MyNavbar />
    <div class="create-conference-container">
        <div class="create-conference-title" @click="createConf()">Создать конференцию</div>
        <div class="theme-container">
        <div class="theme">Тема</div>
        <div class="theme-input-container">
            <input placeholder="Тема..." v-model="theme" class="theme-input">
        </div>
    </div>
    <div class="continuous-conference-chat">
        <!-- <div class="cb">
            <input id="chat" type="checkbox" v-model="cbChat">
        </div> -->
        <!-- <div class="cb-title">Включить чат непрерывной конференции</div> -->
    </div>
    <div class="date-time-conference">
        <div class="date-time-title">Дата и время</div>
        <div class="date-time-picker">
            <div class="date-picker">
            <input type="date" value="12.10.2023" v-model="startDate">
        </div>
        <div class="time-picker">
            <input type="time" value="12:00" v-model="startTime">
        </div>
        </div>
    </div>
    <div class="security-container">
        <div class="security-title">Безопасность</div>
        <div class="access-code">
            <!-- <div class="cb-security">
            <input id="chat2" type="checkbox" v-model="isAccessCodeExists">
            </div> -->
            <!-- <div class="access-code-title">Код доступа</div>
            <div class="access-code-input">
                <input v-model="accessCode">
            </div> -->
        </div>
        <div class="waiting-hall">
            <div class="cb-waiting-hall">
            <input id="chat3" type="checkbox" v-model="waitingHall">
            </div>
            <div class="waiting-hall-title">Зал ожидания</div>
        </div>
        <!-- <div class="video">
            <div class="title">Видеоизображение</div>
            <div class="registrant">
                Организатор:
                <div class="rb-registrant">
                    <div class="rb1-container">
                    <input type="radio" class="rb1" v-model="rbRegistrantVideo">
                    </div>
                    <div class="vkl1">
                        Вкл.
                    </div>
                </div>
            </div>
            <div class="users">
                Участники:
                <div class="rb-users">
                    <div class="rb2-container">
                    <input type="radio" class="rb2" v-model="rbUsersVideo">
                    <label>Вкл.</label>
                    </div>
                </div>
            </div>
        </div> -->
        <!-- <div class="advanced-params"> -->
            <!-- <div class="ap1">
                <input type="checkbox" v-model="ap1">
                <label>Разрешить участникам подключаться в любой момент</label>
            </div> -->
            <!-- <div class="ap2">
                <input type="checkbox" v-model="ap2">
                <label>Выключать звук участников при входе</label>
            </div> -->
            <!-- <div class="ap3">
                <input type="checkbox" v-model="ap3">
                <label>Автоматически записывать конференцию на локальный компьютер</label>
            </div> -->
        <!-- </div> -->
        <button @click="createConf">Создать конференцию</button>
    </div>
    </div>
</template>

<style scoped>
    .create-conference-container {
        display: flex;
        flex-direction: column;
        height: 70vh;
        width: 70%;
        align-items: center;
        /* align-self: center; */
        /* justify-content: flex-start; */
    }

    .create-conference-title {
        display: flex;
        justify-content: flex-start;
        width: 75%;
        font-size: 35px;
        padding-top: 5%;
        padding-bottom: 5%;
    }

    .theme-container {
        display: flex;
        flex-direction: column;
        width: 75%;
        align-items: flex-start;
    }

    .theme-input-container {
        display: flex;
        width: 100%;
    }

    .theme-input {
        width: 75%;
    }

    .continuous-conference-chat {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .date-time-conference {
        display: flex;
        flex-direction: column;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .date-time-picker {
        display: flex;
        width: 75%;
        justify-content: flex-start;
    }

    .time-picker {
        padding-left: 2%;
    }

    .security-container {
        display: flex;
        flex-direction: column;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .access-code {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .access-code-title {
        padding-left: 1%;
        padding-right: 1%;
    }

    .waiting-hall {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .waiting-hall-title {
        padding-left: 1%;
    }

    .video {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .title {
        padding-bottom: 10%;
    }
    
    .registrant {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .rb-registrant {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .rb-users {
        display: flex;
        width: 75%;
        justify-content: flex-start;
        padding-top: 2%;
    }

    .advanced-params {
        display: flex;
        flex-direction: column;
        width: 75%;
        justify-content: flex-start;
    }

</style>