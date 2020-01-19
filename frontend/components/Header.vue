<template>
  <div>
    <nav class="navbar navbar-light bg-light">
      <div>
        <i
          id="heder-icon"
          class="far fa-frown-open fa-2x fa-flip-vertical title"
        />
        <span class="header-title title">THE SADNESS</span>
      </div>
      <div class="icon-position">
        <button
          v-show="Object.keys(this.$store.state.user.user).length == 0"
          id="user"
          type="button"
          class="btn rounded-circle p-0 header-option"
          title="ログイン"
          @click="login"
        >
          <i class="fab fa-twitter header-option-icon" />
        </button>
        <button
          v-show="Object.keys(this.$store.state.user.user).length != 0"
          id="user"
          data-toggle="modal"
          data-target="#userPostImageModal"
          type="button"
          class="btn rounded-circle p-0 header-option"
          title="投稿画像"
          @click="isClickYourImage = !isClickYourImage"
        >
          <img :src="this.$store.state.user.user.icon" class="me-icon" />
        </button>
        <button
          type="button"
          class="rank btn rounded-circle p-0 header-option"
          data-toggle="tooltip"
          title="ランキング"
          @click="showRank"
        >
          <i class="far fa-list-ol header-option-icon" />
        </button>
        <button
          v-show="Object.keys(this.$store.state.user.user).length != 0"
          type="button"
          class="btn rounded-circle p-0 header-option"
          data-toggle="tooltip"
          title="ログアウト"
          @click="logout"
        >
          <i class="fas fa-sign-out-alt header-option-icon" />
        </button>
      </div>
    </nav>

    <!-- マイページモーダ ル -->
    <div
      v-if="Object.keys(this.$store.state.user.user).length != 0"
      id="userPostImageModal"
      class="modal fade"
      data-backdrop="true"
      tabindex="-1"
      role="dialog"
      aria-labelledby="userPostImageModal"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-scrollable" role="document">
        <Images />
      </div>
    </div>
  </div>
</template>

<script>
import firebase from "firebase"
import Images from "~/components/Images.vue"
import { default as trace } from "~/common/log.js"

const provider = new firebase.auth.TwitterAuthProvider()

export default {
  components: {
    Images
  },
  data() {
    return {
      //ユーザー投稿画像表示
      isClickYourImage: false,
      // 削除ボタン押下
      isDelete: false
    }
  },
  computed: {
    // ログインユーザー
    user() {
      return this.$store.state.user.user
    }
  },
  mounted() {
    // twitter認証初期設定
    this.initAuth()
  },
  methods: {
    /**
     * FireBase認証 初期化
     */
    initAuth() {
      let firebaseConfig = {
        apiKey: process.env.FB_APIKEY,
        authDomain: process.env.FB_AUTHDOMEIN,
        databaseURL: process.env.FB_DATABASEURL,
        projectId: process.env.FB_PROJECTID,
        storageBucket: process.env.FB_STOREAGEBUCKET,
        messagingSenderId: process.env.FB_MESSAGING_SENDERID,
        appId: process.env.FB_APPID
      }
      // FireBase初期化
      if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig)
      }
    },
    /**
     * twitter認証でtwitterアカウント取得
     */
    login() {
      firebase
        .auth()
        .signInWithPopup(provider)
        .then(fbResult => {
          trace(fbResult)
          //ユーザー情報取得
          this.$axios
            .get(`${process.env.GET_USER}/${fbResult.user.uid}`)
            .then(dbResult => {
              trace(dbResult)

              // ユーザーの投稿画像取得
              this.$store.dispatch("user/getUserImages", {
                userId: fbResult.user.uid
              })

              // ユーザー情報が更新されているか判定
              const isUpdateUser = this.isUpdateUser(fbResult, dbResult)

              //更新されていたらDBのユーザー情報を更新する
              if (isUpdateUser) {
                this.$store.dispatch("user/updateUser", {
                  id: fbResult.user.uid,
                  displayName: fbResult.additionalUserInfo.profile.name,
                  username: fbResult.additionalUserInfo.username,
                  icon: fbResult.additionalUserInfo.profile.profile_image_url
                })
              }

              // ユーザー情報をstoreに格納
              this.$store.commit("user/setUser", {
                id: fbResult.user.uid,
                displayName: fbResult.additionalUserInfo.profile.name,
                username: fbResult.additionalUserInfo.username,
                icon: fbResult.additionalUserInfo.profile.profile_image_url
              })
            })
            .catch(res => {
              trace(res)
              // ユーザー登録
              this.$store.dispatch("user/createUser", {
                id: fbResult.user.uid,
                displayName: fbResult.additionalUserInfo.profile.name,
                username: fbResult.additionalUserInfo.username,
                icon: fbResult.additionalUserInfo.profile.profile_image_url
              })
            })
            .catch(err => {
              trace(err)
            })
        })
    },
    /**
     * ログアウト
     */
    logout() {
      firebase
        .auth()
        .signOut()
        .then(res => {
          trace(res)
          // 認証用トークンをlocalStorageから削除
          this.$store.commit("user/setUser", {})
          this.$store.commit("user/setImages", {})
        })
        .catch(err => {
          trace(err)
        })
    },
    /**
     * ユーザー情報が更新されているか確認
     */
    isUpdateUser(fb, db) {
      if (
        fb.additionalUserInfo.profile.name != db.data.displayName ||
        fb.additionalUserInfo.username != db.data.username ||
        fb.user.photoURL != db.data.icon
      ) {
        return true
      }

      return false
    },
    /**
     * ランキング一覧を表示する
     */
    showRank() {
      this.$store.commit(
        "event/setIsShowRank",
        !this.$store.state.event.isShowRank
      )
    }
  }
}
</script>
<style lang="scss" scoped>
@import "~assets/scss/header.scss";
@import "~assets/scss/images.scss";
</style>
