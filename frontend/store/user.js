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
    { id: id, username: username}
  ) {
    await this.$axios
      .post(process.env.CREATE_USER, {
        id: id,
        username: username
      })
      .then(res => {
        trace(res)

        // storeにログイン情報を登録
        commit("setUser", {
          id: id,
          username: username
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
