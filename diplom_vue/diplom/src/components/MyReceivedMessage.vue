<script setup>
import { defineProps } from 'vue';

    defineProps({
        text: String,
        sendingTime: Date,
        messageClickListener: Function,
        profilePhoto: String,
        senderName: String,
    })
</script>

<template>
    <div class="received-message">
        <div class="received-message-header">
            <img class="profile-photo" :src="profilePhoto" alt="Profile Photo">
            <div class="sender-name">{{ senderName }}</div>
        </div>
                {{ text }}
                <!-- <div class="received-sending-time">{{ sendingTime.getHours().toString() + ":" + sendingTime.getMinutes().toString()}}</div> -->
            </div>
</template>

<style scoped>
    .received-message {
        background-color: #e6e6e6;
        color: #333;
        border-radius: 0.5em;
        padding: 10px;
        align-self: flex-start;
        width: 35%;
    }

    .received-message .received-sending-time {
        font-size: 12px;
        color: #5d5d5d;
        align-self: flex-end;
        /* align-items: flex-end; */
    }

    .received-sending-time {
        align-items: flex-end;
    }

    .received-message-header {
        display: flex;
        align-items: center;
    }

    .sender-name {
        font-size: medium;
        font-style: italic;
    }

</style>