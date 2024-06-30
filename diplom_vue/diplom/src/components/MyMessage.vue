<script>
// import { defineProps } from 'vue';

//     defineProps({
//         text: String,
//         sendingTime: Date,
//         messageClickListener: Function,
//         profilePhoto: String,
//         senderName: String,
//     })

    export default {
        props: ["text"]
    }

</script>

<template>
    <div class="my-message" @click="messageClickListener">
                {{ text }}
                <!-- <div class="sending-time">{{ sendingTime.getHours().toString() + ":" + sendingTime.getMinutes().toString() }}</div> -->
            </div>
</template>

<style scoped>
    .my-message {
        /* background-color: rgb(48, 195, 11); */
        color: #333;
        border-radius: 0.5em;
        padding: 10px;
        /* align-self: flex-end; */
        width: 35%;
        display: flex;
        flex-direction: column;
        /* justify-content: flex-end; */
    }

    .my-message .sending-time {
        font-size: 12px;
        color:  #5d5d5d;
        align-self: flex-end;
        /* align-items: flex-end; */
        
    }
</style>