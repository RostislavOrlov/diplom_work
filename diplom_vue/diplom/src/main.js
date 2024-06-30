import App from './App.vue'
import { createApp } from 'vue'
import { createStore } from 'vuex'
import { createRouter, createWebHistory } from 'vue-router'
import MyRegistration from './components/MyRegistration.vue'
import MyAuthentication from './components/MyAuthentication.vue'
import MyTeamPage from './components/MyTeamPage.vue'
import MyTeam from './components/MyTeam.vue'
import MyCreateTeam from './components/MyCreateTeam.vue'
import MyJoinTeam from './components/MyJoinTeam.vue'
import MyTeamPendingReq from './components/MyTeamPendingReq.vue'
import MyManageTeam from './components/MyManageTeam.vue'
import MyCreatePost from './components/MyCreatePost.vue'
import MyEditPost from './components/MyEditPost.vue'
import MyCreateConference from './components/MyCreateConference.vue'
import MyConference from './components/MyConference.vue'
import MyChat from './components/MyChat.vue'
import MyChatPage from './components/MyChatPage.vue'
import MyWaitingHall from './components/MyWaitingHall.vue'
import MyProfileDetails from './components/MyProfileDetails.vue'
// import MyPostContainer from './components/MyPostContainer.vue'
import { initTeamPageWebsocket } from './websocket'

const routes = [
    { path: '/register', component: MyRegistration },
    { path: '/auth', component: MyAuthentication },
    { path: '/teams', component: MyTeamPage },
    { path: '/teams/:smth', component: MyTeam },
    { path: '/teams/create', component: MyCreateTeam },
    { path: '/teams/join', component: MyJoinTeam },
    { path: '/teams/:id/pend', component: MyTeamPendingReq },
    // { path: '/teams/team/manageTeam', component: MyManageTeamContainer },
    { path: '/teams/team/manageTeam', component: MyManageTeam },
    { path: '/teams/team/createPost', component: MyCreatePost },
    { path: '/teams/team/editPost', component: MyEditPost },
    { path: '/teams/team/conf/create', component: MyCreateConference },
    { path: '/teams/team/conf/:id', component: MyConference },
    { path: '/chats', component: MyChatPage },
    { path: '/chats/:id', component: MyChat },
    { path: '/conf/waiting_hall', component: MyWaitingHall },
    { path: '/profile', component: MyProfileDetails },
    // { path: '/teams/:id', component: MyPostContainer },
];

const router = createRouter({
    routes,
    history: createWebHistory()
})

router.beforeEach((to, from, next) => {
    if(to.path == '/') {
        next('/auth');
    } else {
        next();
    }
})

var userId = 0

const store = createStore({
    actions: {
        auth(ctx, payload) {
        
            // fetch("http://192.168.1.123:8082/api/auth/signin", {
              fetch("http://localhost:8082/api/auth/signin", {
              method: 'POST',
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
              username: payload['username'],
            //   email: payload['email'],
              password: payload['password'],
            //   role: payload['role'],
            })
            })
            .then(response => response.json())
            .then(data => {
              console.log(data);
            //   this.$store.commit('setUserId', data['id'])
            ctx.commit('setUserId', data['id'])
            // ctx.commit('setUserUsername', data['username'])
            ctx.commit('setUserEmail', data['email'])
            console.log("FROM AUTH ", store.getters.userId)
            userId = store.getters.userId
            console.log("USER ID ", userId)
            localStorage.setItem('userId', data['id'])
            localStorage.setItem('userName', data['username'])
            localStorage.setItem('userEmail', data['email'])
          })
          .catch(error => {
            console.error(error);
          })
        //   this.$store.commit('setUserId', userId)
          setTimeout(() => {
            ctx.commit('setUserId', userId)
            console.log("FROM AUTH2 ", store.getters.userId)
            initTeamPageWebsocket()
            router.push({path: '/teams'})
          }, 4000)
          
          
          }
    },
    state: {
        user_id: 0,
        username: '',
        userEmail: ''
    },
    getters: {
        userId(state) {
            return state.user_id
        },
        userName(state) {
          return state.username
      },
      userEmail(state) {
        return state.userEmail
    }
    },
    mutations: {
        setUserId(state, userId) {
            state.user_id = userId
        },
        setUserName(state, username) {
          state.username = username
      },
      setUserEmail(state, userEmail) {
        state.userEmail = userEmail
      }
    }
})

const app = createApp(App)

app.use(router).use(store).mount('#app')