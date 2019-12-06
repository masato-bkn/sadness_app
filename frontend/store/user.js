import Vuex from "vuex";
import axios from "axios";

export const state = () => ({
  // ログインユーザー
  user: {}, 
  // ログインユーザー投稿画像
  images : []
});

export const mutations = {
  // ログインユーザー セッター
  setUser(state, user) {
    state.user = user;
  },
  // ログインユーザー投稿画像 セッター
  setImages(state, images) {
    state.images = images;
  },
};

export const actions = {
  /**
   * ユーザー情報登録
   */
  async createUser({commit},{ id: id, username: username, photoURL: photoURL, displayName: displayName }) {
    const res = await this.$axios
      .post(process.env.CREATE_USER, {
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
  },
  /**
   * ログインユーザー投稿画像取得
   */
  async getUserImages ({commit},{userId : userId}){
    const res = await axios
    .get(`${process.env.GET_USER_POSTED_IMAGES}/${userId}/imageList`)
    .then(res => {
      commit("setImages", res.data.results);
    })
    .catch(err => {
      console.log(err);
      return;
    });
  },
  /**
   * 画像削除
   */
 deleteUserImage(context, { id: id }) {
   this.$axios
   .delete(`${process.env.DELETE_IMAGE}/${id}/delete`)
   .then(response => {
     let images = this.state.user.images;
     images = images.filter(image => {
       return image.id !== id;
      });
      context.commit("setImages", images);
    })
    .catch(err => {
      console.log(err);
    })
  }
};
