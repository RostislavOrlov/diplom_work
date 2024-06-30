<template>
    <div class="registration-container">
      <h1>Регистрация</h1>
      <form @submit.prevent="register">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
        <br><br>
        <label for="username">Email:</label>
        <input type="text" id="email" v-model="email" required>
        <br><br>
        <label for="password">Password:</label>
        <input type="text" id="password" v-model="password" required>
        <br><br>
        <button type="submit">Register</button>
      </form>
      <p v-if="registered">Registration successful!</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        // registered: false
        role: ['user']
      }
    },
    methods: {
      register() {
        // event.preventDefault();

        // const userData = {
        //   username: this.username,
        //   email: this.email,
        //   password: this.password,
        //   role: this.role,
        // }
        
        fetch("http://localhost:8082/api/auth/signup", {
          method: 'POST',
          // mode: 'no-cors',
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role,
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
      })
      .catch(error => {
        console.error(error);
      })
      }
    }
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
  