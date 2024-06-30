<script>
import MyTeamInfo from './MyTeamInfo.vue';
import MyNavbar from './MyNavbar.vue';
import MyManageTeam from './MyManageTeam.vue';

export default {
    data() {
        return {
            name: localStorage.getItem('currTeamName')
        }
    },
    components: { MyTeamInfo, MyNavbar, MyManageTeam }
}


</script>

<template>
    <MyNavbar />
    <div class="team-container">
        <MyTeamInfo :name="name"/>
        <div class="team-content">
            <MyManageTeam />
        </div>
</div>
</template>

<style scoped>
    .team-container {
        display: flex;
        justify-content: center;
        padding-top: 2px;
    }

    .team-content {
        width: 65%;
        height: 95vh;
        background-color: white;
    }
</style>