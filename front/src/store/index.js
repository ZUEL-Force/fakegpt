import { createStore } from 'vuex'
import user from "@/store/modules/user";
import app from "@/store/modules/app";
import getters from "@/store/getters";
export default createStore({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    user,
    app
  },
  getters
})
