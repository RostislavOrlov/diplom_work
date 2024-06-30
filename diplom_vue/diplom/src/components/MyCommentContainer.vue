<script>
    export default {
        
        props: ['replyNotClicked']
    }
</script>

<template>
    <div class="post-comment-container">
            <div class="post-comment" v-if="replyNotClicked == false">
                <div class="post-comment-1">
                        <div class="post-comment-details">
                            <div class="post-comment-member-img">
                                <img src="" alt="IMAGE">
                            </div>
                            <div class="post-comment-member-name">Привет Приветов</div>
                            <div class="post-comment-post-date-time">12.12.2012</div>
                    </div>
                        <div class="post-comment-post-content"></div>
                        <div class="comment-container-owner">
                            <div class="comment-container">
                                <div class="comment-details">
                                    <div class="comment-member-img">
                                        <img src="" alt="IMAGE">
                                    </div>
                                    <div class="comment-member-name">Привет Приветов</div>
                                    <div class="comment-post-date-time">12.12.2012</div>
                            </div>
                            <div class="comment-content">dfksogjpsdofgnpdognspdothgspdtohusftphnsptohustphostpouhetpohstpohsetohunsetpho</div>
                            </div>
                    </div>
                    </div>
            </div>
            <div class="comment-input">
                <input placeholder="Написать комментарий..." class="input">
    </div>
    </div>
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
</style>