<template>
<div class="post-container">
    <div class="post-outer">
        <div class="post-content">
            <div class="post-body">

            </div>
            <div class="post-footer">
                <button class="btn reset-btn" @click="resetImage">start</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import {mapState} from 'vuex';
import { config } from 'aws-sdk';

export default {
    data(){
        return {

        }
    },
    methods: {

    },
    computed: {

    }
}
</script>

<style　lang="scss" scoped>
@import "~assets/scss/post.scss";
@import "~assets/scss/icon.scss";
</style>