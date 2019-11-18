import Vuex from "vuex";
import axios from "axios";

export const state = () => ({
  user: {}
});

export const mutations = {
  setUser(state, user) {
    state.user = user;
  }
};

export const actions = {
  /*
  * ユーザー情報取得 
  */
  async updateUser({commit},{ id: id, username: username, photoURL: photoURL, displayName: displayName }){        
    const res = await this.$axios
    .put("http://localhost:8000/api/user/create", {
        id: id,
        username: username,
        icon: photoURL,
        displayname:displayName
      })
      .then(res => {
        console.log(res);
      })
      .catch(err => {
        console.log(err);
      })
  },
  /*
  * ユーザー情報登録
  */
  async createUser({commit},{ id: id, username: username, photoURL: photoURL, displayName: displayName }) {
    const res = await this.$axios
      .post("http://localhost:8000/api/user/create", {
        id: id,
        username: username,
        icon: photoURL,
        displayname:displayName
      })
      .then(res => {
        console.log(res);
      })
      .catch(err => {
        console.log(err);
      });
  }
};
