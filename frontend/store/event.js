import Vuex from "vuex";

export const state = () => ({
    message: "",
    category: ""
  });

export const mutations = {
    setMessage(state, message) {
      state.message = message;
    },
    setCategory(state, category){
        state.category = category
    }
}
