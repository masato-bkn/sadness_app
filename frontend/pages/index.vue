  <template>
  <div class="container-fluid" style="background-color: #a4ded6;">
    <div class="row" style="height: 850px;">
      <div class="col-md-7 col-sm-12">  
        <Post v-if="images.length == 0"
          @setOriginalImage="setOriginalImage"/>
        <Option v-else-if="images.length >= 2 & selected == false"
          :originalImage="originalImage"
          @selectDone="setSelected"
          @setSelectedImage="setSelectedImage"
          />
        <Result v-else
          :image="selectedImage == '' ? images[0] : selectedImage"
          :originalImage="originalImage"
          />
      </div>
      <div class="col-md-4" >
        <Rank ref="rank"/>
      </div>
      <!--  デバッグ用　-->
      <!-- {{$store.state}} -->
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import Rank from '~/components/rank.vue';
import Post from '~/components/post.vue';
import Result from '~/components/result.vue';
import Option from '~/components/option.vue';


export default {
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
    }
  },
  components: {
    Rank,
    Post,
    Result,
    Option
  },
  methods: {
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