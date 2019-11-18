import Vuex from "vuex";
import axios from "axios";

export const state = () => ({
  // 画像一覧
  images: []
});

export const mutations = {
  setImages(state, images) {
    state.images = images;
  }
};

export const actions = {
  async getRankImages ({commit}){
    const res = await axios
    .get(`http://localhost:8000/api/imageList`)
    .then(res => {
      commit("setImagesByUser", res.data.results);
    })
  }
};
