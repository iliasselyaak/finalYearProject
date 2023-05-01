import { createStore } from 'vuex'

export default createStore({
  state: { // data
    token: "",
    isAuthenticated: false,
  },
  getters: { // computed properties
    isAuthenticated: (state) => state.isAuthenticated, //get the state of isAuthenticated
    token: (state) => state.token, //get the state of token
  },
  mutations: {
    initializeStore(state){ //initialize the state of the store
      if (localStorage.getItem("token")){
        state.token = localStorage.getItem("token")
        state.isAuthenticated = true
      }
      else{
        state.token = ""
        state.isAuthenticated = false
      }
    },
    setToken(state, token) { //set the token and isAuthenticated state
      state.token = token
      localStorage.setItem("token", token);
      state.isAuthenticated = true
    },
    removeToken(state) { //remove the token and isAuthenticated state
      state.token = ""
      localStorage.removeItem("token");
      state.isAuthenticated = false
    }
  },
  actions: {
  },
  modules: {
  }
})
