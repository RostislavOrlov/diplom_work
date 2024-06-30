<script>
    export default {
        data() {
            return {
                confs: [
                    {
                        meeting_id: 1,
                        confTheme: 'test conf',
                        waiting_hall: true
                    },
                    {
                        meeting_id: 2,
                        confTheme: 'test conf 2',
                        waiting_hall: false
                    }
                ],
            }
        },
        methods: {
            fetchConfs() {
                fetch(`http://localhost:8086/api/v1/meetings/` + localStorage.getItem('currTeamId'), {
                    method: 'GET',
                    // mode: 'no-cors',
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                .then(response => response.json())
                .then(data => {
                    console.log("CONFERENCIES", data);
                    this.confs = data['meetings']
                    console.log("CONFS", this.confs)

                })
            },

            joinConf(conf) {
                console.log("join conf with id", conf.id)
                localStorage.setItem('currMeetingId', conf.id)
                localStorage.setItem('user_registrant_username', conf.user_registrant_username)
                // if(conf.waiting_hall == true && conf.user_registrant_id != Number(localStorage.getItem('userId'))) {
                if(conf.user_registrant_id != Number(localStorage.getItem('userId'))) {
                    this.$router.push('/conf/waiting_hall')
                }

            }
        },
        created() {
            this.fetchConfs()
        }
    }
</script>

<template>
        <div class="conf-container">
            <div class="conf" v-for="conf in confs" :key="conf.meeting_id" @click="joinConf(conf)">
                <div class="conf-theme">{{ conf.theme }}</div>
            </div>
        </div>
</template>

<style scoped>
    .conf-container {
        display: flex;
        flex-direction: column;
        width: 80%;
        height: 88vh;
        overflow-y: scroll;
        scrollbar-width: none;
        align-items: center;
    }

    .conf {
        display: flex;
        flex-direction: column;
        background-color: rgb(245, 245, 245);
        width: 70%;
        height: fit-content;
        margin: 15px;
    }
</style>