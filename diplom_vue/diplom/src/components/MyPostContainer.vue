<script>
    import { getPostWebsocket } from '@/websocket';
    import MyCreatePost from './MyCreatePost.vue'
    import MyEditPost from './MyEditPost.vue';
    export default {
        data() {
            return {
            socket: null,
            replyNotClicked: true,
            createPostConst: false,
            editPostConst: false,
            currPostText: '',
            currPostId: 0,
            posts: [
                // {
                //     id: 1,
                //     postImgSrc: "",
                //     postOwnerName: "Petrov Ivan",
                //     postDate: "08.02.2023",
                //     postContent: "aorgsjapsrojsprojfnapsorjnfaporsnfprojnfpaornparjngrjngparojngpaorjngaprojngpronjgpaenjrtgpaetgnjagnjpoeteganojptgaeonjp",
                //     postCommentCount: 4
                // },
                // {
                //     id: 2,
                //     postImgSrc: "",
                //     postOwnerName: "Petrov Ivan",
                //     postDate: "08.02.2023",
                //     postContent: "aorgsjapsrojsprojfnapsorjnfaporsnfprojnfpaornparjngrjngparojngpaorjngaprojngpronjgpaenjrtgpaetgnjagnjpoeteganojptgaeonjp",
                //     postCommentCount: 5
                // },
                // {
                //     id: 3,
                //     postImgSrc: "",
                //     postOwnerName: "Petrov Ivan",
                //     postDate: "08.02.2023",
                //     postContent: "aorgsjapsrojsprojfnapsorjnfaporsnfprojnfpaornparjngrjngparojngpaorjngaprojngpronjgpaenjrtgpaetgnjagnjpoeteganojptgaeonjp",
                //     postCommentCount: 5
                // },
                // {
                //     id: 4,
                //     postImgSrc: "",
                //     postOwnerName: "Petrov Ivan",
                //     postDate: "08.02.2023",
                //     postContent: "aorgsjapsrojsprojfnapsorjnfaporsnfprojnfpaornparjngrjngparojngpaorjngaprojngpronjgpaenjrtgpaetgnjagnjpoeteganojptgaeonjp",
                //     postCommentCount: 5
                // },
                // {
                //     id: 5,
                //     postImgSrc: "",
                //     postOwnerName: "Petrov Ivan",
                //     postDate: "08.02.2023",
                //     postContent: "aorgsjapsrojsprojfnapsorjnfaporsnfprojnfpaornparjngrjngparojngpaorjngaprojngpronjgpaenjrtgpaetgnjagnjpoeteganojptgaeonjp",
                //     postCommentCount: 5
                // },
            ]
        };
    },

    // computed: {
    //     orderedPosts() {
    //         return this.posts.sort((a, b) => a.postDate - b.postDate)
    //     }
    // },

    components: { MyCreatePost, MyEditPost },

    methods: {
        reloadPosts2(post) {
            console.log("ОЧЕРЕДНОЙ ПОСТ2", post)
            console.log("ПОСТЫ", this.posts)
    },
        createPost() {
            this.createPostConst = true
            // this.socket.send(JSON.stringify({
            //         'payload': {'request': 'createPostForTeam', 'params': {
            //             'team_id': localStorage.getItem('currTeamId'),
            //             'team_member_creator_id': localStorage.getItem('userId'),
            //             'text': "test test2",
            //             'img_ref': '',
            //             'file_ref': '',
            //             'audio_ref': '',
            //             'video_ref': '',
            //         }}
            //     }))
        },
        editPost(post) {
            this.editPostConst = true
            this.currPostText = post.text
            this.currPostId = post.post_id
            console.log(post)
            console.log("this.currPostText", this.currPostText)
            console.log("this.currPostId", this.currPostId)
        },
        editPostReload(post) {
            console.log(post)
            // var curr_post = this.posts.find(currPost => currPost.post_id == post.post_id)
            this.posts.map(currPost => {
                if(currPost.post_id == post.post_id) {
                    currPost.text = post.text
                }
                return post
            })
            // curr_post.postContent = post.text
            // this.posts.push(
            //     {
            //         // id: 6,
            //         post_id: curr_post.post_id,
            //         postImgSrc: curr_post.img_ref,
            //         postOwnerName: curr_post.team_member_creator_id, // потом поменять на никнейм
            //         postDate: "08.02.2024",
            //         postContent: curr_post.postContent,
            //         postCommentCount: 0
            //     }
            // )
            this.editPostConst = false
        },

        deletePost(post) {
            this.socket.send(JSON.stringify({
                'payload': {'request': 'deletePostForTeam', 'params': {
                    'post_id': post.post_id
                }
            }
            }))
        },
        deletePostReload(post) {
            this.posts = this.posts.filter(currPost => currPost.post_id != post.post_id)
        },

        reloadPosts(post) {
            this.createPostConst = false
            console.log("ОЧЕРЕДНОЙ ПОСТ", post)
            this.posts.push(
                {
                    // id: 6,
                    post_id: post.post_id,
                    postImgSrc: post.img_ref,
                    postOwnerName: post.team_member_creator_id, // потом поменять на никнейм
                    postDate: "08.02.2024",
                    postContent: post.text,
                    postCommentCount: 0
                }
            )
        }
},

    created() {
        // localStorage.setItem('currTeamId', 1)
        this.socket = getPostWebsocket()
            this.socket.onmessage = (event) => {
                console.log("FROM ON MESSAGE (POST WEBSOCKET)", event.data)
                const dataJson = JSON.parse(event.data)
                console.log("DATAJSON (POST WEBSOCKET)", dataJson)
                if(dataJson['request'] == 'createPostForTeam') {
                    this.reloadPosts(dataJson['params'])
                }
                else if(dataJson['request'] == 'deletePostForTeam') {
                    this.deletePostReload(dataJson['params'])
                }
                else if(dataJson['request'] == 'getPostsForTeam') {
                    this.posts = dataJson['params']['posts']
                }
            }
            setTimeout(() => {
                this.socket.send(JSON.stringify({
                'payload': {'request': 'getPostsForTeam', 'params': {
                    'team_id': Number(localStorage.getItem('currTeamId'))
                }
            }
            }))
            }, 3000);
            
    }
 }
    
</script>

<template>
    <div class="post-container" v-if="replyNotClicked & createPostConst == false & editPostConst == false">
        <!-- <button @click="createPost">Создать пост</button> -->
                <div class="post" v-for="post in posts" :key="post.post_id" @click="editPost(post)"> <!--@click="deletePost(post)"-->
                    <div class="post-details">
                        <div class="member-img">
                            <img src="" alt="IMAGE">
                        </div>
                        <div class="member-name">{{ post.team_member_creator_username }}</div>
                        <div class="post-date-time">{{ post.postDate }}</div>
                </div>
                    <div class="post-content">{{ post.text }}</div>
                    <div class="post-comments">комментариев: {{ post.postCommentCount }}</div>
                    <div class="reply" @click="replyNotClicked = false">Ответить</div>
                    
                </div>
        </div>
        <MyCreatePost v-if="createPostConst == true" @post="reloadPosts"/>
        <MyEditPost v-if="editPostConst == true" :text="currPostText" :post_id="currPostId" @editPost="editPostReload"/>
</template>

<style scoped>
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
        background-color: rgb(245, 245, 245);
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
        border-bottom: 2px solid rgb(140, 140, 140);
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
        background-color: rgb(245, 245, 245);
        border-top: 2px solid rgb(140, 140, 140);
        height: 5vh;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        /* padding-left: 20px; */
    }
</style>
