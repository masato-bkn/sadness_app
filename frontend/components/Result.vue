<template>
  <div class="result-container">
    <div class="result-outer">
      <div class="result-content">
        <div class="result-header">
          <h5 class="reult-title">
            <i class="fad fa-flask-potion" /><span>採点結果</span>
          </h5>
        </div>
        <div class="reuslt-body">
          <div class="result-border">
            <span class="result-text">
              <span v-if="image.score >= 80" class="good-score">
                Great Sadness !!
              </span>
              <span v-else-if="image.score >= 40" class="good-score">
                Good Sadness !
              </span>
              <span v-else class="bad-score"> Bad Sadness... </span>
            </span>
            <div class="result-block">
              <canvas
                ref="thumnail"
                :width="0"
                :height="0"
                class="result-img"
              />
              <div class="result-score-block">
                <span class="score-text">その悲しみ</span>
                <span
                  class="socre"
                  :class="[image.score >= 40 ? 'good-score' : 'bad-score']"
                >
                  {{ image.score }}点
                </span>
              </div>
            </div>
            <div class="comment-block form-group">
              <p class="comment-label">
                Comment:
              </p>
              <input
                v-model="comment"
                type="text"
                class="form-control"
                :class="[alertMessage != '' ? 'commentAlert' : '']"
              />
              <p v-if="alertMessage != ''" class="text-danger alert-text">
                {{ alertMessage }}
              </p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <a class="btn ok-btn" @click="registImage">Ok</a>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { trimCanvasToSquare } from "~/common/image.js"
import { default as trace } from "~/common/log.js"

export default {
  props: {
    // 解析済みの画像
    image: {
      type: Object,
      required: true,
      default: null
    },
    originalImage: HTMLImageElement // ユーザー投稿画像 元データ
  },
  data() {
    return {
      // コメント
      comment: "",
      // アラートメッセージ
      alertMessage: ""
    }
  },
  computed: {
    // ログインユーザー
    user() {
      return this.$store.state.user.user
    }
  },
  /* eslint-disable  no-unused-vars */
  watch: {
    // コメント入力アラート設定
    comment(value, oldValue) {
      if (value.length > 20) {
        this.alertMessage = "20文字に収めてください。"
        return
      }
      // コメント0文字アラート表示後にコメントが入力された時にアラートを空にする
      if (value.length >= 0) {
        this.alertMessage = ""
        return
      }
    }
  },
  /* eslint-disable  no-unused-vars */
  mounted() {
    // 解析した画像をリサイズしてcanvasに描画
    let canvas = this.$refs.thumnail
    trimCanvasToSquare(
      canvas,
      this.originalImage,
      this.image.boundingBox,
      160,
      160
    )
  },
  methods: {
    /**
     * 画像登録
     */
    async registImage() {
      // コメント未入力または文字数が20文字以上の場合にアラートを表示する。
      if (this.comment.length == 0) {
        this.alertMessage = "コメントを入力してください。"
        return
      }
      if (this.comment.length > 20) {
        return
      }
      let fileName = this.getCurrentTime() + ".png"
      await this.$axios
        .post(`${process.env.REGIST_IMAGE}/`, {
          user: this.user.id,
          name: fileName,
          score: this.image.score,
          comment: this.comment
        })
        .then(res => {
          trace(res)

          // 画像をS3にアップロードする。
          this.$axios
            .post(process.env.S3_UPLOAD, {
              data: this.$refs.thumnail
                .toDataURL("image/jpeg")
                .replace(/^data:\w+\/\w+;base64,/, ""),
              name: fileName,
              bucket: process.env.SADNESS_BUCKET
            })
            .then(res => {
              trace(res)
              this.$store.commit("event/setMessage", "登録完了しました !!")
              this.$store.commit("event/setCategory", "SUCCESS")

              // ユーザ投稿画像一覧更新
              this.$store.dispatch("user/getUserImages", {
                userId: this.user.id
              })
            })
        })
        .catch(err => {
          trace(err)
        })
    },
    /**
     * 現在時刻取得（yyyymmddhhmmss）
     */
    getCurrentTime() {
      let now = new Date()
      let time =
        "" +
        now.getFullYear() +
        this.padZero(now.getMonth() + 1) +
        this.padZero(now.getDate()) +
        this.padZero(now.getHours()) +
        this.padZero(now.getMinutes()) +
        this.padZero(now.getSeconds())
      return time
    },
    /**
     * 先頭ゼロ付加
     */
    padZero(num) {
      return (num < 10 ? "0" : "") + num
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~assets/scss/result.scss";
</style>
