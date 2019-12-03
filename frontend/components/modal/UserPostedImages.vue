<template>
<div class="modal-container">
  <div class="modal-outer">
    <div class="modal-content">
        <div>
          <div class="modal-header">
            <div class="modal-title" id="exampleModalLabel">
                <i class="fad fa-images fa-2x"></i>
              <span class="title">{{this.user.displayName}}さんの画像 </span>
            </div>
          </div>
          <div class="modal-body"> 
              <div class="row">
                <div v-for="image in images" :key="image.id">
                  <div class="col-md-3 col-sm-6">
                    <img :src="S3URL+image.name"  alt="" class="image" data-toggle="tooltip" data-placement="bottom" :title='image.score + "点"'>
                    <button v-if="isDelete" @click="deleteImage(image.id)" type="button" class="del-btn btn rounded-circle p-0 header-option">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              </div>
          </div>
          <div class="modal-footer">
            <div>
              <button @click="isDelete = !isDelete" type="button" class="btn is-del-btn"><i class="fas fa-trash-alt"></i></button>  
            </div>
          </div>
        </div>
      </div>
  </div>
</div>
</template>

<style scoped>
  .modal{
    display: block;
  }
</style>

<script>
import {mapState, } from 'vuex';

export default {
  data () {
    return {
      isDelete: false,
      S3URL: process.env.S3URL
    }
  },
  mounted(){
    $('[data-toggle="tooltip"]').tooltip()
  },
  computed: {
    ...mapState({
      user(){
        return this.$store.state.user.user
      },
      images(){
        return this.$store.state.user.images       
      }
    })
  },
  methods: {
    // 画像削除
    deleteImage (id) {
        this.$store.dispatch('user/deleteUserImage',{id:id})
    },
  }
}
</script>>

<style　lang="scss" scoped>
@import "~assets/scss/_index.scss";
@import "~assets/scss/myPicture.scss";
.modal{
    display: block;
}
</style>
