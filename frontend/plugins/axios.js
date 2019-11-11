import Vue from "vue";

export default function({ $axios }) {
  $axios.onRequest(config => {
    const token = localStorage.getItem("access");

    // 認証用トークンがあればリクエストヘッダに乗せる
    if (token) {
      config.headers.common["Authorization"] = "JWT " + token;
    }
  });
}
