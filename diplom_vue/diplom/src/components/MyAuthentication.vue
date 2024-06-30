<template>
    <div class="authentication-container">
      <h1>Авторизация</h1>
      <!-- <form @submit.prevent="this.$store.dispatch('auth', {
        username: this.username,
        // email: this.email,
        password: this.password,
        // role: this.role,
      })"> -->
      <form @submit.prevent="this.auth({
        username: this.username,
        password: this.password,
      })">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
        <br><br>
        <label for="password">Password:</label>
        <input type="text" id="password" v-model="password" required>
        <br><br>
        <button type="submit">Авторизоваться</button>
      </form>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex'
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        role: ['user']
      }
    },
    methods: mapActions(["auth"]),

      // auth(this.username, this.email, this.password, this.role)
      // auth() {
        
      //   var userId = 0
      //   fetch("http://localhost:8082/api/auth/signin", {
      //     method: 'POST',
      //     headers: {
      //       "Content-Type": "application/json"
      //     },
      //     body: JSON.stringify({
      //     username: this.username,
      //     email: this.email,
      //     password: this.password,
      //     role: this.role,
      //   })
      //   })
      //   .then(response => response.json())
      //   .then(data => {
      //     console.log(data);
      //     this.$store.commit('setUserId', data['id'])
      //     console.log("FROM AUTH ", this.$store.getters.userId)
      //     userId = this.$store.getters.userId
      // })
      // .catch(error => {
      //   console.error(error);
      // })
      // this.$store.commit('setUserId', userId)
      // console.log("FROM AUTH2 ", this.$store.getters.userId)
      // this.$router.push({path: '/teams'})
      // }
    
  }
  </script>
  
  <style scoped>
  h1 {
    color: black;
  }

  .registration-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  </style>
  