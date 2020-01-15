import createPersistedState from "vuex-persistedstate"

export default ({ store }) => {
  window.onNuxtReady(() => {
    // ユーザー情報をローカルストレージに保存
    createPersistedState({
      paths: ["user"]
    })(store)
  })
}
