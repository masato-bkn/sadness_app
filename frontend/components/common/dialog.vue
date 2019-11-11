<template>
    <div class="modal-container">
        <div class="modal-content">
            <div class="modal-body" :class="[category == 'ERROR' ? 'alert-danger': 'alert-info']">
                
                <!-- <i class="far fa-kiss" id="heder-icon"></i> -->
                <div class="dialog-text">
                    <span>{{message}}
                        <button style="display: inline;" type="button" class="close" data-dismiss="alert" aria-label="Close" @click="resetDialog"><span aria-hidden="true">&times;</span></button>
                    </span>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
    computed: {
        message(){
            return this.$store.state.event.message
        },
        category(){
            return　this.$store.state.event.category
        }
    },
    methods: {
        /**
        モーダルを閉じる 
        */
        resetDialog(){
            // eventを初期化
            this.$store.commit("event/setMessage","")
            this.$store.commit("event/setCategory","")
            // モーダルを閉じる
            $('#eventModal').modal('hide')            
        }
    }
}
</script>

<style lang="scss" scoped>
@import "~assets/scss/eventModal.scss";
</style>
