import Vuex from "vuex";

export const state = () => ({
    message: "",
    category: "",
    isShowRank: false
  });

export const mutations = {
    setMessage(state, message) {
      state.message = message;
    },
    setCategory(state, category){
        state.category = category
    },
    setIsShowRank(state, isShowRank) {
      state.isShowRank = isShowRank
    }
}
