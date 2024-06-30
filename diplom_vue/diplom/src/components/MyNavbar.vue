<template>
    <div class="navbar">
      <!-- <div class="navbar-item" @click="navigateTo('profile')">
        <router-link to="/profile">
          <i class="fas fa-user">profile</i>
        </router-link>
      </div> -->
      <div class="navbar-item" @click="navigateTo('chat')">
        <router-link to="/chats">
          <i class="fas fa-comments">chats</i>
        </router-link>
      </div>
      <!-- <div class="navbar-item" @click="navigateTo('notifications')">
        <router-link to="/notifications">
          <i class="fas fa-bell">notifications</i>
        </router-link>
      </div> -->
      <div class="navbar-item" @click="navigateTo('teams')">
        <router-link to="/teams">
          <i class="fas fa-users">teams</i>
        </router-link>
      </div>
      <!-- <div class="navbar-item" @click="navigateTo('tasks')">
        <router-link to="/tasks">
        <i class="fas fa-tasks">tasks</i>
        </router-link>
      </div> -->
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      navigateTo(page) {
        // Здесь вы можете выполнить необходимые действия при нажатии на иконку
        // Например, перенаправление пользователя на соответствующую страницу
        console.log("Navigating to " + page);
      },
    }
  }
  </script>
  
  <style scoped>
  /* .navbar {
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 50px;
    background-color: #f2f2f2;
  }
  
  .navbar-item {
    cursor: pointer;
  }
  
  .navbar-item i {
    font-size: 20px;
  } */

  .navbar {
    display: flex;
    justify-content: space-around;
    background-color: bisque;
    /* height: 5vh; */
  }

  .navbar-item {
    cursor: pointer;
  }

  </style>
  