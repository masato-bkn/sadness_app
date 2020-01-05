<template>
  <div class="modal-container">
    <div class="modal-outer">
      <div class="modal-content">
        <div>
          <div class="modal-header">
            <div id="userPostImageModal" class="modal-title">
              <i class="fad fa-images" />
              <span class="title">{{ user.displayName }}さんの画像 </span>
            </div>
          </div>
          <div class="modal-body">
            <div class="row">
              <div v-for="image in images" :key="image.id">
                <div class="col-md-3 col-sm-6">
                  <img
                    :src="S3URL + image.name"
                    alt=""
                    class="image"
                    data-toggle="tooltip"
                    data-placement="bottom"
                    :title="image.score + '点'"
                  />
                  <button
                    v-if="isDelete"
                    type="button"
                    class="del-btn btn rounded-circle p-0 header-option"
                    @click="deleteImage(image.id)"
                  >
                    <i class="fas fa-times" />
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div>
              <button
                type="button"
                class="btn is-del-btn"
                @click="isDelete = !isDelete"
              >
                <i class="fas fa-trash-alt" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 削除
      isDelete: false,
      // 解析後画像格納バケットURL
      S3URL: process.env.S3URL
    }
  },
  computed: {
    // ログインユーザー
    user() {
      return this.$store.state.user.user
    },
    // ログインユーザー投稿画像
    images() {
      return this.$store.state.user.images
    }
  },
  mounted() {
    $('[data-toggle="tooltip"]').tooltip()
  },
  updated() {
    $('[data-toggle="tooltip"]').tooltip()
  },
  methods: {
    /**
     * 画像削除
     */
    deleteImage(id) {
      this.$store.dispatch("user/deleteUserImage", { id: id })
    }
  }
}
</script>
>

<style lang="scss" scoped>
@import "~assets/scss/myPicture.scss";
.modal {
  display: block;
}
</style>
