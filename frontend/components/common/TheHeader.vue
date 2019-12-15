<template>
  <div>
    <nav class="navbar navbar-light bg-light">
      <div>
        <nuxt-link to="/" class="icon-link">
          <i class="far fa-frown-open fa-2x fa-flip-vertical title" id="heder-icon"></i>
          <span class="header-title title">THE SADNESS</span>
        </nuxt-link>
      </div>
      <div class="icon-position">
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
          data-target="#userPostImageModal"
          type="button"
          id="user"
          class="btn rounded-circle p-0 header-option"
          title="投稿画像"
          @click="isClickYourImage = !isClickYourImage"
          >
          <img :src="this.$store.state.user.user.icon" class="me-icon">
        </button>
        <button
          type="button"
          class="rank btn rounded-circle p-0 header-option"
          data-toggle="tooltip"
          title="ランキング"
          @click="showRank"          
          >
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
    <div v-if="Object.keys(this.$store.state.user.user).length != 0" class="modal fade　modal-dialog-scrollable" data-backdrop="true" id="userPostImageModal" tabindex="-1" role="dialog" aria-labelledby="userPostImageModal" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable" role="document">
        <UserPostedImages />
      </div>
    </div>

  </div>
</template>

<script>
import {mapState, mapActions} from "vuex";
import firebase from "firebase"
import UserPostedImages from "~/components/modal/UserPostedImages.vue";

export default {
    components: {
      UserPostedImages
    },
    data () {
        return {
          //ユーザー投稿画像表示
          isClickYourImage: false,
          // 削除ボタン押下
          isDelete: false
        }
    },
    computed: {
      // ログインユーザー
      user(){
          return this.$store.state.user.user
      }
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
      /**
       * twitter認証でtwitterアカウント取得
       */
      login(){
        const provider = new firebase.auth.TwitterAuthProvider()
        firebase.auth().signInWithPopup(provider).then((result)=>{     
          //ユーザー情報取得
          this.$axios.get(`${process.env.GET_USER}/${result.user.uid}`)
          .then(
            (res) => {
              // storeにログイン情報を登録
              this.$store.commit("user/setUser",{
                  id : result.user.uid,
                  username: result.additionalUserInfo.username,
                  icon : result.user.photoURL,
                  displayName: result.user.displayName
                }
              )
              // ユーザーの投稿画像取得
              this.$store.dispatch("user/getUserImages",{userId : result.user.uid})

              // ユーザー情報が更新されているか判定
              const isUpdateUser = this.isUpdateUser(
                result.additionalUserInfo.username,
                result.user.photoURL,
                result.user.displayName
              )
              //更新されていたらDBのユーザー情報を更新する
              if(isUpdateUser){
                this.$axios.put(`${GET_USER}/${result.user.uid}/update`)
              }
            }
          )
          .catch( (res) =>             
            {
              // ユーザー登録
              this.$store.dispatch("user/createUser",{ id : result.user.uid,username: result.additionalUserInfo.username, photoURL: result.user.photoURL, displayName: result.user.displayName})
              // storeにログイン情報を登録
              this.$store.commit("user/setUser",{ id : result.user.uid, username: result.additionalUserInfo.username, icon : result.user.photoURL, displayName: result.user.displayName})
            }
        ).catch((err) => { 
          console.log(err)
          })
      })},
      /** 
       * ログアウト
       */
      logout(){
        firebase.auth().signOut().then((res) => {
          // 認証用トークンをlocalStorageから削除
          this.$store.commit("user/setUser", {});
        }).catch((err) => {
          console.log(err)
        });
      },
      /**
       * ユーザー情報が更新されているか確認
       */
      isUpdateUser(username, photoUrl, displayName) {
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
      /**
       * ランキング一覧を表示する 
       */
      showRank() {
        this.$store.commit("event/setIsShowRank",!this.$store.state.event.isShowRank)
      }
    },
    mounted () {
      // twitter認証初期設定
      this.initAuth()
    }
}
</script>
<style lang="scss" scoped>
@import "~assets/scss/header.scss";
@import "~assets/scss/myPicture.scss";
</style>

