<template>
  <div class="post-container">
    <div class="post-outer">
      <div class="post-content">
        <div class="post-header">
          <div class="post-title">
            <i class="fad fa-flask-potion" /><span>画像を投稿する</span>
          </div>
        </div>
        <div class="post-body">
          <div v-if="!isThumbnail">
            <div
              class="post-border border-type-dashed"
              :class="[{ drag: isDrag == 'new' }]"
              @dragover.prevent="checkDrag($event, 'new', true)"
              @dragleave.prevent="checkDrag($event, 'new', false)"
              @drop.prevent="resize"
            >
              <div class="contents">
                <i class="fal fa-plus-square" />
                <p class="text-main">
                  ファイルをドラッグ&ドロップする。
                </p>
                <p class="text-sub">
                  または、コンピュータから
                  <label class="text-info">
                    ファイル
                    <input
                      class="file-input"
                      type="file"
                      accept="image/*"
                      @change="resize"
                    />
                  </label>
                  を選択する
                </p>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="post-border border-type-solid">
              <canvas
                ref="thumbnail"
                class="thunail"
                :class="[
                  {
                    'vertically-long': isVerticallyLong,
                    'horizontally-long': isHorizontallyLong
                  }
                ]"
              />
            </div>
          </div>
        </div>
        <div class="post-footer">
          <button class="btn reset-btn" @click="resetImage">
            Reset
          </button>
          <button class="btn submit-btn" @click="submitImage">
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uploadToS3 } from "~/common/s3.js"
import { resizeCanvas } from "~/common/image.js"
import { default as trace } from "~/common/log.js"

export default {
  data() {
    return {
      // 画像がは貼り付けられているかているか
      isThumbnail: false,
      // ドラッグされているか
      isDrag: true,
      // 画像が縦長か
      isVerticallyLong: false,
      // 画像が横長か
      isHorizontallyLong: false,
      // 投稿画像情報
      image: {
        // ファイル名
        name: "",
        // drop,changeイベントで取得した画像データ
        data: "",
        // エンコードした画像データ
        encodeData: ""
      }
    }
  },
  computed: {
    // ログインユーザー
    user() {
      return this.$store.state.user.user
    }
  },
  methods: {
    /**
     * 画像がドラッグされているか判定
     */
    checkDrag(e, key, status) {
      if (status && e.dataTransfer.types == "text/plain") {
        return false
      }
      this.isDrag = status ? key : false
    },
    /**
     * 画像をリセットする
     */

    resetImage() {
      this.image = {}
      this.isThumbnail = false
      this.isDrag = false
      ;(this.isVerticallyLong = false), (this.isHorizontallyLong = false)
    },
    /**
     * 画像表示領域に貼り付けられた画像をリサイズ
     */
    resize(e) {
      this.image.data =
        e.type == "change" ? e.target.files[0] : e.dataTransfer.files[0]

      const image = new Image()
      const reader = new FileReader()

      reader.readAsDataURL(this.image.data)

      reader.onload = e => {
        this.isThumbnail = true
        image.src = e.target.result

        this.image.encodeData = e.target.result.replace(
          /^data:\w+\/\w+;base64,/,
          ""
        )

        image.onload = () => {
          if (image.height > image.width) {
            this.isVerticallyLong = true
          } else {
            this.isHorizontallyLong = true
          }
          this.makeThumbnail(image)
          // 投稿画像を親コンポーネントに渡す
          this.$emit("post-image", image)
        }
      }
    },
    /**
     *  画像をcanvasに描画
     */
    makeThumbnail(image) {
      const canvas = this.$refs.thumbnail
      resizeCanvas(canvas, image)
    },
    /**
     * 画像解析
     */
    submitImage() {
      // ログイン判定
      if (Object.keys(this.$store.state.user.user).length == 0) {
        this.$store.commit("event/setMessage", "ログインしてください")
        this.$store.commit("event/setCategory", "ERROR")
        return
      }

      // 画像選択判定
      if (this.image.data == "") {
        this.$store.commit("event/setMessage", "画像を選択してください")
        this.$store.commit("event/setCategory", "ERROR")
        return
      }

      // 画像のS3uploadが成功したら解析スタート
      uploadToS3(
        this.image.data,
        this.image.data.name,
        process.env.ANALIZE_BUCKET
      )
        .then(result => {
          this.$store
            .dispatch("analysis/analizeImage", { fileName: result.key })
            .catch(err => {
              if (err.data.code == 2) {
                // 画像から顔が認識できなかった場合、親コンポーネントのdialogでエラー内容を表示
                this.$store.commit("event/setMessage", "顔が写っていません...")
                this.$store.commit("event/setCategory", "ERROR")
              }
            })
        })
        .catch(error => {
          // エラーメッセージ出力
          trace(error)
        })
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~assets/scss/post.scss";
</style>
