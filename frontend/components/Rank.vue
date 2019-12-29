<template>
  <div class="rank-container">
    <ul class="rank-list">
      <li class="rank-header"></li>          
        <li class="rank-section" v-for="(image,index) in this.images" :key="index"> 
        <div>
          <img class="image" :src="S3URL+image.name" alt="">
          <span class="badge badge-info">{{image.score}}点</span>
          <span class="user-name"><a :href="TWITTER + image.user.username" style="color: rgb(33, 37, 41);"><span>{{image.user.displayname}}</span></a> さん</span>
          <span class="rank-text">{{image.comment}}</span>
          <span class="post-date">{{image.created_at.substr(0,10)}}</span>
        </div>
      </li>
    </ul>
    <dir class="rank-bottom-area">
      <span>
        <a @click="getImgesList('previous')" class="fas fa-chevron-circle-right fa-rotate-180 rank-prev-botton" aria-hidden="true"></a>
        <a @click="getImgesList('next')" class="fas fa-chevron-circle-right rank-next-botton" aria-hidden="true"></a>
      </span>
    </dir>
  </div>    
</template>

<script>

export default {
  data() {
    return {
      // ランキング画像
      images: [],
      //次ページURL
      next: "",
      // 前ページURL
      previous: "", 
      // twitterURL
      TWITTER: process.env.TWITTER,
      // 解析後画像格納バケットURL
      S3URL : process.env.S3URL
    }
  },
  computed: {
    // 画像削除,画像登録がされたか判定する 
    isChangeImage() {
      return this.$store.state.user.images
    }
  },
  watch: {
    //画像登録、画像削除にDBと同期する 
    isChangeImage (val,old) {
      if (this.images.length != 0) {
        this.getImgesList()
      }
    }
  },
  created() {
    // 画像ランキング取得
    this.getImgesList()
  },
  methods: {
    /**
     * 画像ランキング取得
     */
    getImgesList(trangitionURL=""){
      let url = process.env.GET_IMAGE_LIST

      if (trangitionURL == "next"){
        if (this.next == null){
          return
        }
        url = this.next 
      } else if (trangitionURL == "previous"){
        if (this.previous == null) {
          return
        }
        url = this.previous
      } 

      this.images = []
      
      this.$axios.get(url)
      .then(
        (res)=> {
          res.data.results.map((d) => {
            this.images.push(d)
          })
          this.next = res.data.next
        　this.previous = res.data.previous
        } 
      )
      .catch((err)=>{
        console.log(err)
        })
    }
  }
}
</script>

<style　lang="scss" scoped>

@import "~assets/scss/rank.scss";

</style>
