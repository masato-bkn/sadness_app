<template>
  <div class="option-container">
    <div class="option-outer">
      <div class="option-content">
        <div class="option-header">
          <h5 id="label1" class="optopn-title">
            <i class="fad fa-flask-potion" /><span>どの顔を採点します?</span>
          </h5>
        </div>
        <div class="option-body">
          <div class="contents">
            <div>
              <div
                id="faceImageCarousel"
                class="carousel slide border border-secondary rounded"
                data-interval="false"
              >
                <div class="carousel-inner">
                  <div
                    v-for="(image, index) in images"
                    ref="carousel"
                    :key="index"
                    class="carousel-item"
                    :class="{ active: index == 0 }"
                  >
                    <canvas ref="thumnail" class="canvas" />
                  </div>
                </div>
                <a
                  class="carousel-control-prev"
                  href="#faceImageCarousel"
                  role="button"
                  data-slide="prev"
                >
                  <i
                    class="fas fa-chevron-up fa-rotate-270"
                    aria-hidden="true"
                  />
                </a>
                <a
                  class="carousel-control-next"
                  href="#faceImageCarousel"
                  role="button"
                  data-slide="next"
                >
                  <i
                    class="fas fa-chevron-up fa-rotate-90"
                    aria-hidden="true"
                  />
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <a class="btn ok-btn" @click="selectFace">Ok</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { trimCanvasToSquare } from "~/common/image.js"

export default {
  // ユーザー投稿画像 元データ
  props: {
    originalImage: HTMLImageElement
  },
  computed: {
    // 解析画像
    images() {
      return this.$store.state.analysis.images
    }
  },
  mounted() {
    this.images.map((image, index) => {
      // 解析した結果を元に顔をcanvasに描画する
      let canvas = this.$refs.thumnail[index]
      trimCanvasToSquare(
        canvas,
        this.originalImage,
        image.boundingBox,
        230,
        230
      )
    })
  },
  methods: {
    /**
     * 顔を選択する
     */
    selectFace() {
      //activeになってるアイテムのindexを取得する。
      const items = this.$refs.thumnail
      let targetItem = ""
      items.map((item, index) => {
        if (targetItem != "") {
          return
        }

        // classList =>
        //   0: "carousel-item"
        //   1: "active"
        if (
          item.offsetParent
            ? item.offsetParent.classList[1] == "active"
            : item.parentElement.classList[1] == "active"
        ) {
          targetItem = this.images[index]
        }
      })

      // storeに選択した画像を格納する
      this.$emit("select-image", targetItem)
      this.$emit("image-selection-complete")
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~assets/scss/option.scss";
</style>
