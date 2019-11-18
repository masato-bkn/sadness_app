<template>
  <div style="background-color: rgb(164, 222, 214); height: 825px;">    
    <!-- イベントモーダル-->
    <div>
      <div class="modal fade" id="eventModal" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <eventDialog />
        </div>        
      </div>
    </div> 
    <TheHeader/>
    <main class="contents">
      <nuxt/>
    </main>
  </div>
</template>

<script>
import TheHeader from "~/components/common/TheHeader";
import eventDialog from "~/components/common/dialog";
import Mypage from "~/components/modal/mypage";

export default {
  components: {
    TheHeader,
    eventDialog,
    Mypage
  },
  methods:{
    showModal(){
      $('#eventModal').modal('show')
    },
    dialog(){
      if (this.$store.state.event.category != "") {
        $('#eventModal').modal('show')
      }
    }
}}
</script>

<style lang="scss" scoped></style>