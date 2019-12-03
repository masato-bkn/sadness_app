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
      <div class="col-md-5" v-if="isShowRank">
        <transition name="rank">
          <Rank ref="rank"/>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import Rank from '~/components/Rank.vue';
import Post from '~/components/Post.vue';
import Result from '~/components/Result.vue';
import Option from '~/components/Option.vue';


export default {
  components: {
    Rank,
    Post,
    Result,
    Option
  },
  data () {
    return {
      selected: false,
      originalImage: "",
      selectedImage: ""
    }
  },
  computed: {
    images(){
      return this.$store.state.analysis.images
    },
    isShowRank() {
      return this.$store.state.event.isShowRank
    }
  },
  beforeMount() {
    // スマホ開かれてたらランキングは初回非表示にする
    this.resizeWindow()
    window.addEventListener('resize', this.resizeWindow)
  },
  methods: {
    resizeWindow() {
      if (window.innerWidth < 400){
        this.$store.commit("event/setIsShowRank",false)
      } else {
        this.$store.commit("event/setIsShowRank",true)
      }
    },
    setSelected(){
      this.selected = true
    },
    setOriginalImage(originalImage){
      this.originalImage = originalImage
    },
    setSelectedImage(selectedImage) {
      this.selectedImage = selectedImage
    }
  }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/_index.scss";
</style>