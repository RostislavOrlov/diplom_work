<script>
    export default {
        data() {
            return {
                myChannelName: this.channelName
            }
        },

        props: ['channelName', 'createPost', 'editPost', 'deletePost'],

        methods: {
            addTest2User() {
                // var curr2 = localStorage.getItem('currTeamId')
                fetch(`http://localhost:8000/teams/1/users/test2`, {
                    method: 'POST',
                    // mode: 'no-cors',
                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        id: 3, 
                        username: 'test2',
                        team_id: 1
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    //const dataJson = JSON.parse(data['result'])
                    //console.log("СПАРСИЛОСЬ")
                    const user = data['result']
                    console.log(user)
                    // this.users = dataJson['users']
                })
            },
            toCreateConf() {
                this.$router.push('/teams/team/conf/create')
            },
            toPosts() {
                this.$emit('enablePosts')
            },
            toFiles() {
                this.$emit('enableFiles')
            },
            toConfs() {
                this.$emit('enableConfs')
            },
            toParticipants() {
                this.$emit('enableParticipants')
            },
            toPendingRequests() {
                this.$emit('enablePendingRequests')
            }
        }
    }
</script>

<template>
    <div class="team-content-navbar">
                <div class="channel-navbar-start">
                    <div class="team-img">
                        <!-- <img :src="imgSrc" alt="IMAGE" class="img"> -->
                    </div>
                    <!-- <div class="channel-name">{{ myChannelName }}</div> -->
                    <div class="channel-posts" @click="toPosts()">Публикации</div>
                    <!-- <div class="channel-files" @click="toFiles()">Файлы</div> -->
                    <div class="channel-confs" @click="toConfs()">Конференции</div>
                    <div class="channel-participants" @click="toParticipants()">Участники</div>
                    <div class="channel-pending-requests" @click="toPendingRequests()">Ожидающие запросы</div>
                    </div>
                <div class="channel-navbar-end">
                    <button @click="createPost()">Создать пост</button>
                    <button @click="toCreateConf()">Создать конференцию</button>
                    <!-- <button @click="editPost()">Редактировать пост</button>
                    <button @click="deletePost()">Удалить пост</button> -->
                    <!-- <button @click="addTest2User">Добавить участника</button> -->
                    <!-- <button @click="this.$router.push({path: '/teams/team/conf/create'})">Зайти в конференцию</button> -->
                    <div class="more"></div>
                    <div class="start-conf"></div>
                    <div class="channel-info"></div>
                </div>
                <!-- <button class="button-conf">Создать собрание</button> -->
            </div>
</template>

<style scoped>
    .team-content-navbar {
        width: 100%;
        height: 7vh;
        border-bottom: 2px solid lightgray;
        display: flex;
    }

    .channel-navbar-start {
        width: 80%;
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

    .channel-confs {
        width: fit-content;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .channel-participants {
        width: fit-content;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .channel-pending-requests {
        width: fit-content;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .channel-navbar-end {
        width: 20%;
        /* align-self: flex-end; */
        display: flex;
        justify-content: space-around;
    }
</style>