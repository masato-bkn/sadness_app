import axios from "axios"
import { default as trace } from "~/common/log.js"

export const state = () => ({
  // ログインユーザー
  user: {},
  // ログインユーザー投稿画像
  images: []
})

export const mutations = {
  // ログインユーザー セッター
  setUser(state, user) {
    state.user = user
  },
  // ログインユーザー投稿画像 セッター
  setImages(state, images) {
    state.images = images
  }
}

export const actions = {
  /**
   * ユーザー情報登録
   */
  async createUser(
    { commit },
    { id: id, displayName: displayName, username: username, icon: icon }
  ) {
    await this.$axios
      .post(process.env.CREATE_USER, {
        id: id,
        username: username,
        displayName,
        icon: icon
      })
      .then(res => {
        trace(res)

        // storeにログイン情報を登録
        commit("setUser", {
          id: id,
          displayName: displayName,
          username: username,
          icon: icon
        })
      })
      .catch(err => {
        trace(err)
      })
  },
  /**
   * ユーザー情報更新
   */
  async updateUser(
    { commit },
    { id: id, displayName: displayName, username: username, icon: icon }
  ) {
    await this.$axios
      .put(`${process.env.UPDATE_USER}/${id}/update`, {
        id: id,
        username: username,
        displayName: displayName,
        icon: icon
      })
      .then(res => {
        trace(res)

        commit("setUser", {
          id: id,
          username: username,
          displayName: displayName,
          icon: icon
        })
      })
      .catch(err => {
        trace(err)
      })
  },
  /**
   * ログインユーザー投稿画像取得
   */
  async getUserImages({ commit }, { userId: userId }) {
    await axios
      .get(`${process.env.GET_USER_POSTED_IMAGES}/${userId}/imageList`)
      .then(res => {
        commit("setImages", res.data)
      })
      .catch(err => {
        trace(err)
        return
      })
  },
  /**
   * 画像削除
   */
  deleteUserImage(context, { id: id }) {
    this.$axios
      .delete(`${process.env.DELETE_IMAGE}/${id}/delete`)
      .then(res => {
        trace(res)
        let images = this.state.user.images
        images = images.filter(image => {
          return image.id !== id
        })
        context.commit("setImages", images)
      })
      .catch(err => {
        trace(err)
      })
  }
}
