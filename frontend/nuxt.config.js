// 環境変数
require('dotenv').config();

// AWS
const AWS_ACCESS_KEY = process.env.AWS_ACCESS_KEY
const AWS_SECRET_ACCESS_KEY = process.env.AWS_SECRET_ACCESS_KEY
const AWS_S3_REGION = process.env.AWS_S3_REGION
const ANALIZE_BUCKET = process.env.ANALIZE_BUCKET
const SADNESS_BUCKET = process.env.SADNESS_BUCKET
const S3URL = process.env.S3URL

// twitter
const TWITTER = process.env.TWITTER

// FireBase
const FB_APIKEY = process.env.FB_APIKEY
const FB_AUTHDOMEIN = process.env.FB_AUTHDOMEIN
const FB_DATABASEURL = process.env.FB_DATABASEURL
const FB_PROJECTID = process.env.FB_PROJECTID
const FB_STOREAGEBUCKET = process.env.FB_STOREAGEBUCKET
const FB_MESSAGING_SENDERID = process.env.FB_MESSAGING_SENDERID
const FB_APPID = process.env.FB_APPID

export default {
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    script: [
      { src: "https://code.jquery.com/jquery-3.3.1.slim.min.js"},
      { src: "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"},
      { src: "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"},
      { src: "https://kit.fontawesome.com/00512c614f.js"}
    ],
    link: [
      { rel: "stylesheet", href: "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"},
      { rel: "stylesheet", href: "https://use.fontawesome.com/releases/v5.6.1/css/all.css"}
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  devModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://bootstrap-vue.js.org/docs/
    'bootstrap-vue/nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/proxy'
  ],
  axios: {
    prefix: '/api',
  },
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      pathRewrite: {
        '^/api': '/'
      }
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
      config.node = {
        fs: "empty"
      };
    }
  },
  env: {
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_REGION,
    ANALIZE_BUCKET,
    SADNESS_BUCKET,
    S3URL,
    TWITTER,
    FB_APIKEY,
    FB_AUTHDOMEIN,
    FB_DATABASEURL,
    FB_PROJECTID,
    FB_STOREAGEBUCKET,
    FB_MESSAGING_SENDERID,
    FB_APPID
  },
  plugins: [
    '~/plugins/axios',
    '~/plugins/localStorage'
  ]
}

module.exports = {
  modules: ['@nuxtjs/style-resources'],
  styleResources: {
    scss: [
      '~/assets/scss/_index.scss',
      '~/assets/scss/rank.scss',
      '~/assets/scss/post.scss',
      '~/assets/scss/result.scss',      
      '~/assets/scss/option.scss',      
      '~/assets/scss/icon.scss',
      '~/assets/scss/myPicture.scss',
      '~/assets/scss/eventModal.scss',
    ]
  }
}