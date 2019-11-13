import Vuex from "vuex";
import axios from "axios";

export const state = () => ({
  // 解析後イメージ
  images: [], 
  // ユーザー別画像
  imagesByUser: [],
  // ランキング用イメージ
  rankImages: "",
  // オリジナル画像
  targeImageData: "",
  // 選択画像
  pickedImageData: "",
  //解析された画像のファイル名
  pickedImageName: "",
});

export const mutations = {
  setImages(state, images) {
    state.images = images;
  },
  setTargeImageData(state, targeImageData) {
    state.targeImageData = targeImageData;
  },
  setPickedImageData(state, pickedImageData) {
    state.pickedImageData = pickedImageData;
  },
  setpickedImageName(state, pickedImageName) {
    state.pickedImageName = pickedImageName;
  },
  setImagesByUser(state, imagesByUser) {
    state.imagesByUser = imagesByUser;
  }
};
export const actions = {
  async getRankImages ({commit}){
    const res = await axios
    .get(`http://localhost:8000/api/imageList`)
    .then(res => {
      commit("setImagesByUser", res.data.results);
    })
  },
  /**
  * ユーザー別画像情報取得
  */
  async getImagesByUser ({commit},{userId : userId}){
    const res = await axios
    .get(`http://localhost:8000/api/user/${userId}/imageList`)
    .then(res => {
      commit("setImagesByUser", res.data.results);
    })
    .catch(err => {
      console.log(err);
      return;
      // 解析に失敗した時の処理を記述
    });
  },
  // 画像解析api呼び出し
  async getImages({ commit }, { fileName: fileName, fileData: fileData }) {
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
  },
  /**
  * 画像削除
  */
  delete(context, { id: id }) {
    this.$axios
      .delete(`http://localhost:8000/api/image/${id}/delete`)
      .then(response => {
        let images = this.state.image.imagesByUser;

        images = images.filter(image => {
          return image.id !== id;
        });
        context.commit("setImagesByUser", images);
      })
      .catch(err => {
        console.log(err);
  })},
  setTargeImageData({ commit}, {targeImageData:targeImageData}) {
    commit("setTargeImageData", targeImageData);
  },
  async setPickedImageData({ commit }, { pickedImageData: pickedImageData }) {
    commit("setPickedImageData", pickedImageData);
  }
};
