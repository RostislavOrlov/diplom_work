<script>
// import { getWebsocket } from '@/websocket';
import MyNavbar from './MyNavbar.vue';
import MyTeamContentNavbar from './MyTeamContentNavbar.vue';
import MyTeamInfo from './MyTeamInfo.vue';
import { getWebsocket } from '../websocket'
import MyPostContainer from './MyPostContainer.vue';
import MyFileContainer from './MyFileContainer.vue';
import MyConfContainer from './MyConfContainer.vue';
import MyParticipantContainer from './MyParticipantContainer.vue';
import MyPendReqContainer from './MyPendReqContainer.vue';

    export default {
    data() {

        return {
            replyNotClicked: true,
            showMoreOptions: false,
            manageTeam: false,
            name: localStorage.getItem('currTeamName'),
            teamDescription: localStorage.getItem('currTeamDescription'),
            channelName: "Общий",
            postsEnabled: true,
            filesEnabled: false,
            confsEnabled: false,
            participantsEnabled: false,
            pendingRequestsEnabled: false
        };
    },
    components: { MyNavbar, MyTeamInfo, MyTeamContentNavbar, MyPostContainer, 
        MyFileContainer, MyConfContainer, MyParticipantContainer, MyPendReqContainer },

    methods: {
    
        // getPostsForTeam() {
        //     let websocket = getWebsocket()
        //     console.log("TEAMMMMMMMMMMMMMMMMMM ID ", this.$route.params.id)
        //     websocket.send(JSON.stringify({'payload': {'request': 'getPostsForTeam', 'params': {'team_id': this.$route.params.id}}}))
        // },

        createPost() {
            // let websocket = getWebsocket()
            // websocket.send(JSON.stringify({'payload': {'request': 'createPostForTeam', 'params': {
            //     'team_id': this.$route.params.id,
            //     'team_member_creator_id': 2,
            //     'text': 'test post',
            //     'img_ref': '',
            //     'file_ref': '',
            //     'audio_ref': '',
            //     'video_ref': '',
            // }}}))
            this.$router.push({path: '/teams/team/createPost'})
        },

        editPost() {
            // let websocket = getWebsocket()
            // websocket.send(JSON.stringify({'payload': {'request': 'editPostForTeam', 'params': {
            //     'post_id': 1,
            //     'text': 'test post2',
            //     'img_ref': '',
            //     'file_ref': '',
            //     'audio_ref': '',
            //     'video_ref': '',
            // }}}))

            this.$router.push({path: '/teams/team/editPost'})
        },

        deletePost() {
            let websocket = getWebsocket()
            websocket.send(JSON.stringify({'payload': {'request': 'deletePostForTeam', 'params': {
                'post_id': 1
            }}}))
        },

        enablePosts() {
            console.log("enablePosts in MyTeam")
            this.postsEnabled = true
            this.filesEnabled = false
            this.confsEnabled = false
            this.participantsEnabled = false
            this.pendingRequestsEnabled = false
        },

        enableFiles() {
            console.log("enableFiles in MyTeam")
            this.postsEnabled = false
            this.filesEnabled = true
            this.confsEnabled = false
            this.participantsEnabled = false
            this.pendingRequestsEnabled = false
        },
    
        enableConfs() {
            console.log("enableConfs in MyTeam")
            this.postsEnabled = false
            this.filesEnabled = false
            this.confsEnabled = true
            this.participantsEnabled = false
            this.pendingRequestsEnabled = false
        },

        enableParticipants() {
            console.log("enableParticipants in MyTeam")
            this.postsEnabled = false
            this.filesEnabled = false
            this.confsEnabled = false
            this.participantsEnabled = true
            this.pendingRequestsEnabled = false
        },

        enablePendingRequests() {
            console.log("enablePendingRequests in MyTeam")
            this.postsEnabled = false
            this.filesEnabled = false
            this.confsEnabled = false
            this.participantsEnabled = false
            this.pendingRequestsEnabled = true
        }

    },

    created() {
        // this.connectWebsocket()
        // let testF = () => {
        //     console.log("SUCCESSFULL")
        // }
        // let websocket = getWebsocket()
        // websocket.addEventListener(getTestEvent(), testF)
        console.log("USER USERNAME", localStorage.getItem('userName'))
        console.log("USER EMAIL", localStorage.getItem('userEmail'))
    }
}

    // function changeMoreOptionsStatus() {
    //     if(showMoreOptions) {
    //         showMoreOptions = false
    //     } else {
    //         showMoreOptions = true
    //     }
    // }

</script>

<template>
    <MyNavbar/>
    <div class="team-container">
        <MyTeamInfo :name="name" :teamDescription="teamDescription"/>
        <div class="team-content">
            <MyTeamContentNavbar channelName="Общий" :createPost="createPost" :editPost="editPost" :deletePost="deletePost" 
            @enablePosts="enablePosts()" @enableFiles="enableFiles()" @enableConfs="enableConfs()"
            @enableParticipants="enableParticipants()" @enablePendingRequests="enablePendingRequests()"/>
            <MyPostContainer v-if="postsEnabled"/>
            <MyFileContainer v-if="filesEnabled"/>
            <MyConfContainer v-if="confsEnabled"/>
            <MyParticipantContainer v-if="participantsEnabled"/>
            <MyPendReqContainer v-if="pendingRequestsEnabled"/>

            <!-- <MyCommentContainer :replyNotClicked="false"/> -->
        </div>
        </div>
</template>

<style scoped>

    .input {
        width: 100%;
        height: 5vh;
        border: 2px solid lightgray;
    }

    .comment-input {
        /* align-self: flex-end; */
        height: 15vh;
        width: 70%;
        background-color: purple;
        display: flex;
        flex-direction: column;
    }

    .post-comment-container {
        height: fit-content;
        justify-content: space-between;
    }

    .comment-container-owner {
        overflow-y: scroll;
        scrollbar-width: none;
        height: 30vh;
        display: flex;
        flex-direction: column;
        /* align-items: center; */
    }

    .comment-container {
        display: flex;
        flex-direction: column;
    }

    .comment-details {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        padding-bottom: 5%;
        padding-top: 2%;
        padding-left: 2%;
    }

    .comment-content {
        height: fit-content;
        width: 100%;
        word-wrap: break-word;
        padding-bottom: 2%;
    }

    .team-container {
        display: flex;
        justify-content: center;
        padding-top: 2px;
    }

    .team-info {
        width: 25%;
        height: 95vh;
        background-color: bisque;
        display: flex;
        flex-direction: column;
        /* align-items: center; */
    }

    .team-content {
        width: 65%;
        height: 95vh;
        background-color: white;
    }

    .manage-team {
        width: 65%;
        height: 95vh;
        background-color: white;
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
        height: fit-content;
        width: 100%;
    }

    .team-name {
        flex-grow: 3;
        height: 5vh;
        font-weight: bold;
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

    .team-content-navbar {
        width: 100%;
        height: 7vh;
        border-bottom: 2px solid lightgray;
        display: flex;
    }

    .manage-team-navbar {
        width: 100%;
        height: 7vh;
        border-bottom: 2px solid lightgray;
        display: flex;
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

    .post-container, .post-comment-container {
        display: flex;
        flex-direction: column;
        width: 80%;
        /* background-color: green; */
        height: 88vh;
        overflow-y: scroll;
        scrollbar-width: none;
        align-items: center;
    }

    .post, .post-comment {
        display: flex;
        flex-direction: column;
        background-color: yellow;
        width: 70%;
        height: fit-content;
        margin: 15px;
    }

    .post-details, .post-comment-details {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        padding-top: 8px;
        
    }

    .post-content, .post-comment-post-content {
        height: fit-content;
        word-wrap: break-word;
        padding-top: 20px;
        padding-left: 10px;
        border-bottom: 2px solid lightgray;
    }

    .post-date-time, .post-comment-post-date-time {
        padding-left: 8px;
    }

    .post-comments {
        height: 5vh;
        display: flex;
        align-items: center;
        padding-left: 20px;
    }

    .reply {
        width: 100%;
        background-color: greenyellow;
        height: 5vh;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        /* padding-left: 20px; */
    }

</style>