<template>
  <div> 
    <div class="rank-container">
      <ul class="rank-list">
        <li class="rank-header"></li>          
          <li class="rank-section" v-for="(image,index) in this.images" :key="index"> 
          <div>
            <img class="image" :src="S3URL+image.name" alt="">
            <div>
              <span class="badge badge-info">{{image.score}}点</span>
              <span style="position: absolute; top: 4px; left: 135px; font-size:14px;"><a :href="TWITTER + image.user.username" style="color: rgb(33, 37, 41); text-decoration: none;"><span style="font-size: 15px;">{{image.user.displayname}}</span></a> さん</span>
            </div>
            <span class="rank-text">{{image.comment}}</span>
            <span style="position: absolute; bottom: 6px; right: 10px; font-size:12px;">{{image.created_at.substr(0,10)}}</span>
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
</div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      images: [],
      next: "",
      previous: "",
      TWITTER: process.env.TWITTER,
      S3URL : process.env.S3URL
    }
  }
  ,created() {
    this.getImgesList()
  },
  methods: {
    getImgesList(trangitionURL=""){
      
      let url = "http://localhost:8000/api/imageList"

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
      
      // TODO 画像情報取得関数を共通化する 
      let res = axios.get(url)
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