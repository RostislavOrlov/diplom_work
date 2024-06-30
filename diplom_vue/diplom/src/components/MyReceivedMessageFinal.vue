<script>
    export default {
        props: ["messageTextFinal", "messageSenderNameFinal"]
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
    </div>
    </template>
    
    <style scoped>
    .userMessage {
        display: flex;
        flex-direction: column;
        /* width: 35%; */
        width: fit-content;
        height: fit-content;
        background-color: rgb(255, 255, 255);
        border-radius: 1.5vh;
        color: white;
        align-self: flex-start;
        margin-bottom: 2vh;
        margin-left: 2vh;
        color: black
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
        color: black;
        text-align: end;
        margin: 1vh
    }
    </style>