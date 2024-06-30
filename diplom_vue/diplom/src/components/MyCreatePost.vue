<template>
    <MyNavbar />
    <div class="team-container">
        <MyTeamInfo :name="name" :team-description="teamDescription"/>
        <div class="post">
            <div class="navbar-post">
                <div class="title">Новый пост</div>
            </div>
            <div class="content">
                <input type="textarea" class="content2" v-model="postContent">
            </div>
            <div class="content-input">
                <button @click="createPost">Отправить</button>
            </div>
        </div>
        </div>
</template>

<script>
    import { getCreatePostWebsocket } from '@/websocket';
    // import { reloadPosts } from './MyPostContainer.vue'
    import MyNavbar from './MyNavbar.vue';
    import MyTeamInfo from './MyTeamInfo.vue';

    export default {

        data() {
        return {
            name: localStorage.getItem('currTeamName'),
            postContent: '',
            socket: null
        }
    },

        computed: {
            teamDescription() {
                return localStorage.getItem('currTeamDescription')
            }
        },

        components: { MyNavbar, MyTeamInfo },

        methods: {
            createPost() {
                this.socket.send(JSON.stringify({
                    'payload': {'request': 'createPostForTeam', 'params': {
                        'team_id': localStorage.getItem('currTeamId'),
                        'team_member_creator_id': Number(localStorage.getItem('userId')),
                        'team_member_creator_username': localStorage.getItem('userName'),
                        'text': this.postContent,
                        'img_ref': '',
                        'file_ref': '',
                        'audio_ref': '',
                        'video_ref': '',
                    }}
                }))
            }
        },

        created() {
            // initCreatePostWebsocket()
            this.socket = getCreatePostWebsocket()
            this.socket.onmessage = (event) => {
                if(event.data != 'test') {
                    console.log("FROM ON MESSAGE", event.data)
                    const dataJson = JSON.parse(event.data)
                    // console.log("DATAJSON", dataJson)
                    // reloadPosts(dataJson['params'])
                    this.$emit('post', dataJson['params'])
                    // this.$router.back()
                }
            }
            console.log("CREATE POST COMPONENT")
        }
    }
</script>

<style scoped>
    .team-container {
        display: flex;
        justify-content: center;
        padding-top: 2px;
    }

    .post {
        width: 65%;
        height: 95vh;
        background-color: white;
        display: flex;
        flex-direction: column;
    }

    .navbar-post {
        width: 100%;
        height: 10vh;
        border-bottom: 2px solid lightgray;
        text-align: center;
        display: flex;
        justify-content: flex-start;
        align-items: center;
    }

    .title {
        width: 30%;
        font-size: 35px;
        font-weight: bold;
    }

    .content {
        height: 70vh;
        width: 100%;
    }

    .content-input {
        height: 15vh;
        width: 100%;
    }

    .content2 {
        height: 100%;
        width: 100%;
        border: 0;
        vertical-align: top;
        /* resize: none; */
    }

    .content2:focus {
        outline: none;
    }

</style>
