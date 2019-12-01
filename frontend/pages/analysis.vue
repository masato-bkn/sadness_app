<template>
  <div class="container-fluid" style="background-color: #a4ded6;">
    <div class="row" style="height: 850px;">
      <div class="col-md-7 col-sm-12">
          <Top/>      
      </div>
      <div class="col-md-5">
        <transition name="rank">
          <Rank ref="rank" v-if="isShowRank"/>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import Top from '~/components/top.vue';
import Rank from '~/components/rank.vue';

export default {
  components: {
    Rank,
    Top
  },
  computed: {
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
    }
  }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/_index.scss";
</style>