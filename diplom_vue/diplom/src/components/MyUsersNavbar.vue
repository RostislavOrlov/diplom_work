<template>
    <div class="users-window-navbar">
            <div class="users-window-navbar-title-and-cancel">
                <div class="users-window-navbar-title">Участники</div>
                <div class="users-window-navbar-cancel">K</div>
            </div>
            <div class="users-window-navbar-functions">
                <div class="users-window-navbar-copy-link">
                    <div class="users-window-navbar-copy-link-img">
                        <img src="" alt="1">
                    </div>
                    <div class="users-window-navbar-copy-link-title">Скопировать код</div>
                </div>
                <div class="users-window-navbar-add-users">
                    <div class="users-window-navbar-add-users-img">
                        <img src="" alt="2">
                    </div>
                    <div class="users-window-navbar-add-users-title">Добавить участников</div>
                </div>
                <div class="users-window-navbar-user-permissions">
                    <div class="users-window-navbar-user-permissions-img">
                        <img src="" alt="3">
                    </div>
                    <div class="users-window-navbar-user-permissions-title">Доступы участников</div>
                </div>
            </div>
        </div>
</template>

<style scoped>
.users-window-navbar {
        display: flex;
        flex-direction: column;
        background-color: rgb(235, 229, 229);
        height: 30vh;
        width: 100%;
    }

    .users-window-navbar-title-and-cancel {
        display: flex;
    }

    .users-window-navbar-title {
        font-size: 20px;
        /* align-self: center; */
        text-align: center;
        width: 95%;
    }

    .users-window-navbar-cancel {
        font-size: 20px;
        align-self: flex-end;
        width: 5%;
    }

    .users-window-navbar-functions {
        display: flex;
        justify-content: space-around;
        height: 30vh;
        padding-top: 15%;
        /* align-items: center; */
    }

    .users-window-navbar-copy-link {
        background-color: plum;
        width: 15vh;
        height: 15vh;
        display: flex;
        flex-direction: column;
        text-align: center;
        
    }
 
    .users-window-navbar-add-users {
        background-color: yellow;
        width: 15vh;
        height: 15vh;
        display: flex;
        flex-direction: column;
        text-align: center;
    }

    .users-window-navbar-user-permissions {
        background-color: yellowgreen;
        width: 15vh;
        height: 15vh;
        display: flex;
        flex-direction: column;
        text-align: center;
    }

</style>