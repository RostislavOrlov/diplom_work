<script>
    export default {
        props: ["messageTextFinal", "messageSenderNameFinal", "messageReadListener", "isReaded"]
    }
</script>

<template>
<div class="userMessage">
    <div class="senderDetails">
        <div class="senderImg">
            <img src="" alt="IMG">
        </div>
        <div class="senderName">{{ messageSenderNameFinal }}</div>
    </div>
    <div class="messageTextFinal">{{ messageTextFinal }}</div>
    <div class="messageDateFinal">10:00</div>
    <div class="isReaded" v-if="isReaded">прочитано</div>
</div>
</template>

<style scoped>
.userMessage {
    display: flex;
    flex-direction: column;
    /* width: 35%; */
    width: fit-content;
    max-width: 50%;
    height: fit-content;
    background-color: rgb(10, 192, 77);
    border-radius: 1.5vh;
    color: white;
    align-self: flex-end;
    margin-bottom: 2vh;
    margin-right: 2vh;
}

.senderDetails {
    display: flex;
    justify-content: flex-start;
    padding-top: 2vh;
    padding-left: 2vh;
    padding-bottom: 2vh;
    padding-right: 2vh;
}

.senderImg {

}

.senderName {
    padding-left: 5px;
    font-weight: bold;
    font-style: italic;
}

.messageTextFinal {
    word-wrap: break-word;
    height: fit-content;
    /* width: 100%; */
    margin: 1vh;
    margin-right: 2vh;
    padding-right: 2vh;
    /* border-bottom: 1px solid green; */
}

.messageDateFinal {
    align-self: flex-end;
    width: 100%;
    height: 3vh;
    color: white;
    text-align: end;
    margin-right: 1vh;
    margin-left: 1vh;
    margin-bottom: 0.5vh;
    margin-top: 1vh;
}

.isReaded {
    align-self: flex-end;
    width: 100%;
    height: 3vh;
    color: white;
    text-align: end;
    margin-right: 1vh;
    margin-left: 1vh;
    margin-bottom: 1vh;
    margin-top: 0.5vh;
}

</style>