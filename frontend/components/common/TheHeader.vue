<template>
  <div>
    <nav class="navbar navbar-light bg-light">
      <div>
        <nuxt-link to="/" class="icon-link">
          <i class="far fa-frown-open fa-2x fa-flip-vertical" id="heder-icon"></i>
          <!-- <span class="header-title">その悲しみ</span> -->
          <span class="header-title">THE SADNESS</span>
        </nuxt-link>
      </div>
      <div style="text-align: right;">
        <button
          v-show="Object.keys(this.$store.state.user.user).length == 0"
          type="button"
          id="user"
          class="btn rounded-circle p-0 header-option"
          title="ログイン"
          @click="login">
          <i class="fab fa-twitter header-option-icon"></i>
        </button>
        <button
          v-show="Object.keys(this.$store.state.user.user).length != 0"
          data-toggle="modal"
          data-target="#exampleModal"
          type="button"
          id="user"
          class="btn rounded-circle p-0 header-option"
          title="マイページ"
          @click="isClickMypage = !isClickMypage"
          >
          <img :src="this.$store.state.user.user.icon" class="me-icon">
        </button>
        <button
          type="button"
          class="btn rounded-circle p-0 header-option"
          data-toggle="tooltip"
          title="ランキング">
          <i class="far fa-list-ol header-option-icon"></i>
        </button>
        <button
          v-show="Object.keys(this.$store.state.user.user).length != 0"
          type="button"
          @click="logout"
        　class="btn rounded-circle p-0 header-option"
          data-toggle="tooltip"
          title="ログアウト">
          <i class="fas fa-sign-out-alt header-option-icon"></i>
        </button>
      </div>
    </nav>
    
    <!-- マイページモーダ ル -->
    <div v-if="Object.keys(this.$store.state.user.user).length != 0" class="modal fade　modal-dialog-scrollable" data-backdrop="true" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <Mypage />
      </div>
    </div>

  </div>
</template>

<script>
import {mapState, mapActions} from 'vuex';
import firebase from 'firebase'
import Mypage from '~/components/modal/mypage.vue';
import Rank from '~/components/rank.vue';

export default {
    components: {
      Mypage,
      Rank
    },
    data () {
        return {
            isDelete: false,
            isClickMypage: false,
            S3URL: 'https://face-bucket-mst.s3-ap-northeast-1.amazonaws.com/'
        }
    },
    computed: {
      ...mapState({
        user(){
          return this.$store.state.user.user
        },
        images(){
          return this.$store.state.image.imagesByUser       
        }
      })
    },
    methods: {
      /**
       * FireBase認証 初期化
       */
      initAuth(){
        let firebaseConfig = {
          apiKey: process.env.FB_APIKEY,
          authDomain: process.env.FB_AUTHDOMEIN,
          databaseURL: process.env.FB_DATABASEURL,
          projectId: process.env.FB_PROJECTID,
          storageBucket: process.env.FB_STOREAGEBUCKET,
          messagingSenderId: process.env.FB_MESSAGING_SENDERID,
          appId: process.env.FB_APPID
          };

          // FireBase初期化
          if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
          }
      },
      /*
      * twitter認証でtwitterアカウント取得
      */
      login(){
        const provider = new firebase.auth.TwitterAuthProvider()
        firebase.auth().signInWithPopup(provider).then((result)=>{     
          //ユーザー情報取得
          this.$axios.get(`http://localhost:8000/api/user/${result.user.uid}`)
          .then(
            (res) => {
              // storeにログイン情報を登録
              this.$store.commit('user/setUser',{
                  id : result.user.uid,
                  username: result.additionalUserInfo.username,
                  icon : result.user.photoURL,
                  displayName: result.user.displayName
                }
              )
              
              // ユーザーの投稿画像取得
              this.$store.dispatch('image/getImagesByUser',{userId : result.user.uid})
              
              // ユーザー情報が更新されているか判定
              const isUpdateUser = this.isUpdateUser(
                result.additionalUserInfo.username,
                result.user.photoURL,
                result.user.displayName
              )
              //更新されていたらDBのユーザー情報を更新する
              if(isUpdateUser){
                this.$axios.put(`http://localhost:8000/api/user/${result.user.uid}/update`)
              }
            }
          )
          .catch( (res) =>             
            {
              // ユーザー登録
              this.createUser( result.user.uid, result.additionalUserInfo.username, result.user.photoURL, result.user.displayName)
              // storeにログイン情報を登録
              this.$store.commit('user/setUser',{ id : result.user.uid, username: result.additionalUserInfo.username, icon : result.user.photoURL, displayName: result.user.displayName})
            }
        ).catch((err) => { 
          console.log("err")
          console.log(err)
          })
      })},
      /* 
      ログアウト
      */
      logout(){
        firebase.auth().signOut().then((res) => {
          // 認証用トークンをlocalStorageから削除
          // localStorage.removeItem("access");
          this.$store.commit("user/setUser", {});
        }).catch((err) => {
          console.log(err)
        });
      },
      /*
      * ユーザー情報を取得する
      */
      createUser(id, username, photoUrl, displayName){
        this.$store.dispatch("user/createUser",{
              id : id,
              username : username,
              photoURL : photoUrl,
              displayName : displayName
            })
      },
      /*
      * ユーザー情報を更新する
      */
      updateUser(){
        this.$store.dispatch('auth/updateUser',
        {
            username: this.form.username,
            email: this.form.email,
            password: this.form.password,
            twitter: this.form.twitter == "" ? this.twitter : this.form.twitter
          }
        ).then((res) => {
          console.log(res)
        }).catch((err) =>
          console.log(err)
        )
      },
      /*
      * ユーザー情報が更新されているか確認
      */
      isUpdateUser(username, photoUrl, displayName) {
        console.log(displayName)
        console.log(this.user.displayName)
        if (username != this.user.username) {
          return true
        }
        if (photoUrl != this.user.icon) {
          return true
        }
        if (displayName != this.user.displayName) {
          return true
        }
        return false
      },
      initTooltip(){

        if (this.$store.state.user) {
          // $('#user').title = this.$store.state.user.user.user.displayName
        }
      }
    },
    mounted () {
      // twitter認証初期設定
      this.initAuth()
      this.initTooltip()
    }
}
</script>
<style lang="scss" scoped>
@import "~assets/scss/icon.scss";
@import "~assets/scss/header.scss";
@import "~assets/scss/myPicture.scss";
</style>

