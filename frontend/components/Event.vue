<template>
  <div class="modal-container">
    <div class="modal-content">
      <div
        class="modal-body"
        :class="[category == 'ERROR' ? 'alert-danger' : 'alert-info']"
      >
        <i v-if="category == 'ERROR'" class="far fa-kiss icon-potition" />
        <i
          v-if="category == 'SUCCESS'"
          class="fas fa-check-circle icon-potition"
        />
        <span class="modal-message">
          {{ message }}
          <button
            style="display: inline;"
            type="button"
            class="close"
            data-dismiss="alert"
            aria-label="Close"
            @click="resetModal"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    // メッセージ
    message() {
      return this.$store.state.event.message
    },
    // イベントカテゴリー
    category() {
      return this.$store.state.event.category
    }
  },
  methods: {
    /**
     * モーダルを閉じる
     */
    resetModal() {
      // モーダルを閉じる
      $("#eventModal").modal("hide")
      this.$store.commit("event/setMessage", "")
      this.$store.commit("event/setCategory", "")

      // modalを閉じた後に、画像投稿画面が表示されるようにここでimageを空にする。
      this.$store.commit("analysis/setImages", [])
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~assets/scss/event.scss";
</style>
