import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    is_sp_authenticated: false,
    token: '',
    isLoading: false
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
      } else {
          state.token = ''
          state.isAuthenticated = false
      } 
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
        state.token = token
        state.isAuthenticated = true
    },  
    removeToken(state) {
        state.token = ''
        state.isAuthenticated = false
        localStorage.removeItem("token")
        localStorage.removeItem("username")
        localStorage.removeItem("userid")
    }
  },
  actions: {
  },
  modules: {
  }
})
