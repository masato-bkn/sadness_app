import axios from "axios"
import { default as trace } from "~/common/log.js"

export const state = () => ({
  // 解析後画像情報
  images: []
})

export const mutations = {
  // 解析後画像情報 セッター
  setImages(state, images) {
    state.images = images
  }
}

export const actions = {
  /**
   * 画像解析
   */
  async analizeImage({ commit }, { fileName: fileName }) {
    return await axios
      .get(process.env.ANALIZE_IMAGE, { params: { image: fileName } })
      .then(res => {
        // 解析失敗
        if (res.data.code != 1) {
          throw res
        }
        commit("setImages", res.data.result)
      })
      .catch(err => {
        trace(err)
        throw err
      })
  }
}
