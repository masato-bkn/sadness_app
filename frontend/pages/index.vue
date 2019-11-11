  <template>
  <div class="container-fluid" style="background-color: #a4ded6;">
    <div class="row" style="height: 850px;">
      <div class="col-md-7 col-sm-12">  
        <Post   v-if="images.length == 0"/>
        <Option v-else-if="images.length >= 2 & !resultFlag" @registerDone="setResultFlag"/>
        <Result v-else/>
      </div>
      <div class="col-md-4" >
        <Rank/>
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
      resultFlag: false
    }
  },
  computed: {
    ...mapState({
      images(){
        return this.$store.state.image.images
      }
    })
  },
  components: {
    Rank,
    Post,
    Result,
    Option
  },
  methods: {
    setResultFlag(){
      this.resultFlag = true
    }
  }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/_index.scss";
</style>