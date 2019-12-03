<template>
<div class="option-container">
    <div class="option-outer">
            <div class="option-content">
                <div class="option-header">
                    <h5 class="optopn-title" id="label1"><i class="fad fa-flask-potion"></i><span>どの顔を採点します?</span></h5>
                </div>
                <div class="option-body">
                    <div class="contents">
                        <div>
                            <div id="carouselExampleControls" class="carousel slide border border-secondary rounded" data-interval="false">
                                <div class="carousel-inner">
                                    <div class="carousel-item" ref='carousel' :class="{active: index == 0}" v-for="(image, index) in images" :key="index">
                                        <canvas class="canvas" ref='thumnail'></canvas>                            
                                    </div>
                                </div>
                                <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
                                    <i class="fas fa-chevron-up fa-rotate-270" aria-hidden="true"></i>
                                </a>
                                <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
                                    <i class="fas fa-chevron-up fa-rotate-90" aria-hidden="true"></i>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <a class="btn ok-btn" @click="decideFace">OK</a>
                </div>        
        </div>
    </div>
</div>

</template>

<script>
import {mapState} from 'vuex';
import {trimCanvasToSquare} from '~/common/image.js';

export default {
    props: ["originalImage"],
    mounted() {
        this.images.map((image, index)=>{
            // 解析した結果を元にcanvasから顔を切り取る
            let canvas = this.$refs.thumnail[index]
            trimCanvasToSquare(canvas,this.originalImage,image.boundingBox,230,230)
        })
    },
    computed: {
        images(){
            // 評価画像
            return this.$store.state.analysis.images
        }
    },
    methods: {
        decideFace(){
            //activeになってるアイテムのindexを取得する。
            const items = this.$refs.thumnail
            let targetItem = ""
            items.map((item,index) =>{

                // TODO ダサすぎる。。。
                if (targetItem != ""){
                    return
                }
                // classList =>
                //   0: "carousel-item"
                //   1: "active"
                if (item.offsetParent ? item.offsetParent.classList[1] == "active" : item.parentElement.classList[1] == "active"){
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

<style　lang="scss" scoped>
@import "~assets/scss/option.scss";
</style>
