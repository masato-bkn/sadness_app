<template>
<div class="result-container">
    <div class="result-outer">
        <div class="result-content">
            <div class="result-header">
                <h5 class="reult-title"><i class="fad fa-flask-potion"></i><span>採点結果</span></h5>
            </div>
            <div class="reuslt-body">
                <div class="result-border">
                    <span class="result-text">Good Sadness !!</span>
                    <div class="result-block">
                        <canvas ref="thumnail" :width="0" :height="0" class="result-img"></canvas>
                        <div class="result-score-block">            
                            <span class="score-text">その悲しみ</span>
                            <span class="socre">{{this.image.score}}点 !!</span>
                        </div>

                    </div>
                    <div class="comment-block form-group">
                        <p class="comment-label">Comment:</p>
                            <input v-model="comment" type="text" class="form-control" :class="{commentAlert : commentAlert}">
                        <p v-if="commentAlert" class="text-danger alert-text">25文字におさめてください。。。</p>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <a class="btn ok-btn" @click="registImage">ok</a>
            </div>
        </div>
    </div>
</div>
</template>
<script>
import {mapState} from 'vuex';
import axios from 'axios'
import {uploadToS3} from '~/common/s3.js';
import {trimCanvasToSquare} from '~/common/image.js';

export default {
    props: [
        "originalImage",
        "image"
        ],
    data(){
        return {
            comment: ""
        }
    },
    methods: {
        /**
        画像登録 
        */
        async registImage(){
            const res = await this.$axios.post(
                "http://localhost:8000/api/image/",
                {
                    user: this.user.id,
                    name: this.image.file, // ファイル名 + timestampがいい??
                    score: this.image.score,
                    comment: this.comment
                    },
                    {
                        headers: { // TOD0 これいる??
                            'Content-Type': 'multipart/form-data',
                            'Content-type': 'application/json'
                        }
                    }
                )
                .then((res) => {
                    // 画像をS3にアップロードする。
                    uploadToS3(
                        this.dataURItoBlob(this.$refs.thumnail.toDataURL("image/jpeg")),
                        this.image.file,
                        process.env.SADNESS_BUCKET
                    ).then((res) => {
                        this.$store.commit("event/setMessage","登録完了しました !!")
                        this.$store.commit("event/setCategory","SUCCESS")

                        // ユーザ投稿画像一覧更新
                        this.$store.dispatch('user/getUserImages',{userId : this.user.id})
                    })
                })
                .catch((err) => {
                    console.log(err)
                }   
            )
        },
        /*
        * コピペしたソースなので要解析 
        */
        dataURItoBlob(dataURI) {
            let binary = atob(dataURI.split(',')[1]);
            let array = [];
            for(var i = 0; i < binary.length; i++) {
                array.push(binary.charCodeAt(i));
            }
            return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
        }},
        mounted() {
            // 解析した画像(canvas)をリサイズ
            let canvas = this.$refs.thumnail
            trimCanvasToSquare(canvas,this.originalImage,this.image.boundingBox,160,160)
    },
    computed: {
        commentAlert(){
            return this.comment.length > 20
        },
        ...mapState({
            user(){
                return this.$store.state.user.user
            },
        })
    }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/result.scss";
@import "~assets/scss/icon.scss";
</style>