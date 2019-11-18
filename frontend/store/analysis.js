import Vuex from "vuex";
import axios from "axios";

export const state = () => ({
  // 解析後画像情報
  images: [],
});

export const mutations = {
    setImages(state, images) {
      state.images = images;
    }
};

export const actions = {
    // 画像解析api呼び出し
    async analizeImage({ commit }, { fileName: fileName}) {
      return await axios
        .get("http://localhost:8000/api/analize", { params: { img: fileName } })
        .then(res => {
          if (res.data.code != 1) {
            throw res
          }
          commit("setImages", res.data.result);
        })
        .catch(err => {
          console.log(err);
          throw err
        });
    }
}