  <template>
  <div class="container-fluid" style="background-color: #a4ded6;">
    <div class="row" style="height: 850px;">
      <div class="col-md-7 col-sm-12">
        <Post v-if="images.length == 0"
          @post-image="setOriginalImage"/>
        <Option v-else-if="images.length >= 2 & selected == false"
          :originalImage="originalImage"
          @image-selection-complete="setSelected"
          @select-image="setSelectedImage"
          />
        <Result v-else
          :image="selectedImage == '' ? images[0] : selectedImage"
          :originalImage="originalImage"
          />
      </div>
      <transition name="rank">
        <div class="col-md-5" v-if="isShowRank">
          <Rank/>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import Rank from "~/components/Rank.vue";
import Post from "~/components/Post.vue";
import Result from "~/components/Result.vue";
import Option from "~/components/Option.vue";


export default {
  components: {
    Rank,
    Post,
    Result,
    Option
  },
  data () {
    return {
      selected: false,　// 画像選択完了
      originalImage: "", // ユーザー投稿画像
      selectedImage: "" // 選択した画像
    }
  },
  computed: {
    // 解析した画像
    images(){
      return this.$store.state.analysis.images
    },
    // ランキング表示
    isShowRank() {
      return this.$store.state.event.isShowRank
    }
  },
  beforeMount() {
    // スマホ表示の場合にランキングは初回非表示にする
    this.resizeWindow()
    window.addEventListener("resize", this.resizeWindow)
  },
  methods: {
    /**
     * ウィンドウサイズによってランキングの表示非表示を切り替える
     */
    resizeWindow() {
      if (window.innerWidth < 400){
        this.$store.commit("event/setIsShowRank",false)
      } else {
        this.$store.commit("event/setIsShowRank",true)
      }
    },
    /**
     * ユーザー投稿画像 セッター
     */
    setOriginalImage(originalImage){
      this.originalImage = originalImage
    },
    /**
     * 画像選択完了 セッター
     */
    setSelected(){
      this.selected = true
    },
    /**
     * 選択した画像 セッター
     */
    setSelectedImage(selectedImage) {
      this.selectedImage = selectedImage
    }
  }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/_index.scss";
</style>