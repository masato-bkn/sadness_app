<template>
<div class="post-container">
    <div class="post-outer">
        <div class="post-content">
            <div class="post-header">
              <div class="post-title"><i class="fad fa-flask-potion"></i><span>画像を投稿する</span></div>
            </div>
            <div class="post-body">
                <div v-if="!isThumbnail">
                    <div class="post-border"
                         :class="[{'drag': isDrag == 'new'}]"
                         @dragover.prevent="checkDrag($event, 'new', true)"
                         @dragleave.prevent="checkDrag($event, 'new', false)"
                         @drop.prevent="resize">
                        <div class="contents">
                            <i class="fal fa-plus-square"></i>
                            <p class="text-main">ファイルをドラッグ&ドロップする。</p>
                            <p class="text-sub">または、コンピュータから
                                <label class="text-info" >ファイル
                                    <input @change="resize" style="display: none" type="file" accept="image/*">
                                </label>を選択する
                            </p>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <div class="post-border">
                        <canvas ref="thumbnail" class="thunail" :class="[{'vertically-long': isVerticallyLong, 'horizontally-long': isHorizontallyLong}]"></canvas>
                    </div>
                </div>
            </div>
            <div class="post-footer">
                <button class="btn reset-btn" @click="resetImage">Reset</button>                
                <button class="btn submit-btn" @click="submitImage">Submit</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import {mapState} from 'vuex';
import { config } from 'aws-sdk';
import { Promise, resolve, reject } from 'q';
import {uploadToS3} from '~/common/s3.js';
import {resizeCanvas} from '~/common/image.js';

export default {
    data(){
        return {
            isThumbnail: false,
            isDrag: true,
            isVerticallyLong: false,
            isHorizontallyLong: false,
            image : {
                name :"",
                data : "",
                encodeData : "",
            }
        }
    },
    methods: {
        /**
        * 画像がドラッグされているか判定 
        */
        checkDrag(e, key, status) {
            if (status && e.dataTransfer.types == "text/plain") {
                return false
            }
            this.isDrag = status ? key : false
        },
        /**
        * 画像をリセットする 
        */        
        resetImage () {
            this.image = {}
            
            // TODO　こんなにフラグ作っていいのか。。
            this.isThumbnail = false
            this.isDrag = false
            this.isVerticallyLong = false,
            this.isHorizontallyLong = false
        },
        /**
        * 画像表示領域に貼り付けられた画像をリサイズ
        */
        resize(e) {

            console.log("★")
            console.log(e)
            console.log("★")
            
            this.image.data = (e.type == "change") ? e.target.files[0] : e.dataTransfer.files[0]

            const image = new Image()
            const reader =  new FileReader()

            reader.readAsDataURL(this.image.data)
            
            reader.onload = (e) => {
                this.isThumbnail = true
                image.src = e.target.result

                this.image.encodeData = e.target.result.replace(/^data:\w+\/\w+;base64,/, '')

                image.onload = () => {
                    if (image.height > image.width) {
                        this.isVerticallyLong = true
                    } else {
                        this.isHorizontallyLong = true
                    }
                    
                    this.makeThumbnail(image)
                    this.$store.commit('image/setTargeImageData',image)
                }
            }
        },
        /**
        *  画像をcanvasに描画
        */
        makeThumbnail(image) {
            const canvas = this.$refs.thumbnail
            resizeCanvas(canvas,image,330)
        },
        /**
        * 画像解析 
        */
        submitImage() {
            // ログイン判定
            if (Object.keys(this.$store.state.user.user).length == 0){
                this.$store.commit("event/setMessage","ログインしてください")
                this.$store.commit("event/setCategory","ERROR")
                return
            }
            
            // 画像のS3uploadが成功したら解析スタート
            uploadToS3(this.image.data, this.image.data.name, process.env.ANALIZE_BUCKET)
            .then((result)=>{
                // 画像解析api呼び出し
                this.$store.dispatch("image/getImages",{fileName: result.key, fileData: this.image.encodeData})
                .then((result) =>{
                    if (result.data.result.code == 2) {
                        // 画像から顔が認識できなかった場合、親コンポーネントのdialogでエラー内容を表示
                        this.$store.commit("event/setMessage",result.data.result.message)
                        this.$store.commit("event/setCategory","ERROR")
                    }
                })
            })
            .catch((error)=> {
                // エラーメッセージ出力
                console.log(error)
            })
        },
        /**
        * 画像をS3にuploadする 
        */
        postImage() {
            const aws = require("aws-sdk")

            const params = {
                Body: this.image.data,
                Bucket: process.env.BUCKET,
                Key: this.image.data.name, // TODO /日付/ファイル名
            }
            const s3 = new aws.S3()
            aws.config.update({
                region: process.env.AWS_S3_REGION,
                secretAccessKey:process.env.AWS_SECRET_ACCESS_KEY,
                accessKeyId: process.env.AWS_ACCESS_KEY
                })
            return new Promise((resolve, reject)=>{
                s3.upload(params, (err, data) => {
                    if(err){
                        reject(err)
                    } else {
                        resolve(data)
                    }
                })
            })
        }
    },
    computed: {
      ...mapState({
        user(){
          return this.$store.state.user.user
        }
      })
    }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/post.scss";
@import "~assets/scss/icon.scss";
</style>