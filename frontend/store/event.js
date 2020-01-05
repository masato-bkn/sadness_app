export const state = () => ({
  // イベントメッセージ
  message: "",
  // イベントカテゴリー
  category: "",
  // ランキング表示
  isShowRank: false
})

export const mutations = {
  // イベントメッセージ セッター
  setMessage(state, message) {
    state.message = message
  },
  // イベントカテゴリー セッター
  setCategory(state, category) {
    state.category = category
  },
  // ランキング表示 セッター
  setIsShowRank(state, isShowRank) {
    state.isShowRank = isShowRank
  }
}
