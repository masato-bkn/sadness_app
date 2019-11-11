import createPersistedState from "vuex-persistedstate";

export default ({ store }) => {
  window.onNuxtReady(() => {
    // ユーザー情報をローカルストレージに保存
    console.log(store.state)
    createPersistedState({
      paths: [
        "user",
      ]})(store);
  });
};
