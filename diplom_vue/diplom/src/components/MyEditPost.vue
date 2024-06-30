<script>
    // import MyNavbar from './MyNavbar.vue';
    // import MyTeamInfo from './MyTeamInfo.vue';
    import { getEditPostWebsocket } from '@/websocket'

    export default {

        data() {
        return {
            name: localStorage.getItem('currTeamName'),
            postContent: this.text,
            socket: null,
            postId: this.post_id
        }
    },

        methods: {
            editPost() {
                this.socket.send(JSON.stringify({
                    'payload': {'request': 'editPostForTeam', 'params': {
                        'post_id': this.postId,
                        'text': this.postContent,
                        'img_ref': '',
                        'file_ref': '',
                        'audio_ref': '',
                        'video_ref': '',
                    }}
                }))
            }
        },

        // components: { MyNavbar, MyTeamInfo },

        props: ['text', 'post_id'],

        created() {
            console.log(this.myText)
            this.socket = getEditPostWebsocket()
            this.socket.onmessage = (event) => {
                if(event.data != 'test') {
                    console.log("FROM ON MESSAGE", event.data)
                    const dataJson = JSON.parse(event.data)
                    // console.log("DATAJSON", dataJson)
                    // reloadPosts(dataJson['params'])
                    this.$emit('editPost', dataJson['params'])
                    // this.$router.back()
                }
            }
        }
    }
</script>

<template>
    <!-- <MyNavbar /> -->
    <div class="team-container">
        <!-- <MyTeamInfo :name="name"/> -->
        <div class="post">
            <div class="navbar-post">
                <div class="title">Редактировать пост</div>
            </div>
            <div class="content">
                <input type="textarea" class="content2" v-model="postContent">
            </div>
            <div class="content-input">
                <button @click="editPost">Отправить</button>
            </div>
        </div>
        </div>
</template>

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
        width: 50%;
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
