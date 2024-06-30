<script>
    export default {
        data() {
            return {
            myName: this.name,
            myShowMoreOptions: false,
            myManageTeam: false,
            myTeamDescription: this.teamDescription
        }
        },

        props: ['name', 'teamDescription'],

        created() {
            console.log(localStorage.getItem('currTeamDescription'))
        }
    }
</script>

<template>
    <div class="team-info">
            <div class="button-back">
                <!-- <div class="back-title">Назад</div> -->
            </div>
            <div class="team-img">
                <!-- <img src="" alt="Team-Image" class="team-img-media"> -->
            </div>
            <div class="team-name-and-more">
                <div class="team-name">Название команды: {{ myName }}</div>
                <div class="team-desc">Описание команды: {{ myTeamDescription }}</div>
                <!-- <div class="team-more" @click="myShowMoreOptions = true">больше</div> -->
                <div v-if="myShowMoreOptions && myManageTeam == false" class="more-options"> <!-- v-if="showMoreOptions && manageTeam == false" -->
                    <div class="content">
                        <div class="content-container">
                            <div class="e1" @click="this.$router.push({path: '/teams/team/manageTeam'})">Управление командой</div> <!--@click="manageTeam = true"-->
                            <div class="e2">Добавить участника</div>
                            <div class="e3">Добавить канал</div>
                            <div class="e4">Получить ссылку на команду</div>
                            <div class="e5">Выйти из группы</div>
                            <!-- <div class="e6">Удалить группу</div> -->
                        </div>
                        <button @click="myShowMoreOptions = false">Закрыть</button> <!--@click="showMoreOptions = false"-->
                    </div>
                </div>
            </div>
            <div class="team-channels"></div>
        </div>
</template>

<style scoped>
    .team-info {
        width: 25%;
        height: 95vh;
        background-color: bisque;
        display: flex;
        flex-direction: column;
        /* align-items: center; */
    }

    .buttton-back {
        display: flex;
        justify-content: flex-start;
        width: 95%;
        height: 5vh;
    }

    .back-title {
        width: fit-content;
        height: 100%;
        padding-left: 5px;
    }

    .team-img {
        width: 100%;
        height: 10vh;
        display: flex;
        justify-content: flex-start;
        padding-top: 10px;
    }

    .team-img-media {
        padding-left: 5px;
    }

    .team-name-and-more {
        display: flex;
        flex-direction: column;
        height: fit-content;
        width: 100%;

    }

    .team-name {
        flex-grow: 3;
        height: 5vh;
        margin-bottom: 7%;
        padding-left: 7%;
        font-weight: bold;
        text-align: center;
        display: flex;
        justify-content: flex-start;
        border-bottom: 2px solid rgb(134, 26, 2);
    }

    .team-desc {
        height: 5vh;
        margin-top: 7%;
        margin-left: 7%;
        font-weight: bold;
        text-align: start;
        display: flex;
        justify-content: flex-start;
    }

    .team-more {
        flex-grow: 1;
        height: 5vh;
    }

    .more-options {
        position: fixed;
        top: 0;
        left: 0;
        width: 25%;
        height: 25%;
        /* background-color: aquamarine; */
        /* display: flex; */
        justify-content: center;
        align-items: center;
    }

    .content {
        background-color: white;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }

    .content-container {
        display: flex;
        flex-direction: column;
        height: fit-content;
        width: 100%;
    }

    .e1, .e2, .e3, .e4, .e5 {
        border: 2px solid lightgray;
    }
</style>