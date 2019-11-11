<template>
  <div style="background-color: rgb(164, 222, 214); height: 825px;">
    <div v-on="dialog()">
      <div class="modal fade" v-on="showModal()" data-backdrop="static" id="eventModal" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <eventDialog />
        </div>        
      </div>
    </div>

    <TheHeader />
    <main class="contents">
      <nuxt />
    </main>
  </div>
</template>

<script>
import TheHeader from "~/components/common/TheHeader";
import eventDialog from "~/components/common/dialog";

export default {
  components: {
    TheHeader,
    eventDialog
  },
  methods:{
    showModal(){
      // $('#eventModal').modal('show')
    },
    dialog(){
      if (this.$store.state.event.category != "") {
        $('#eventModal').modal('show')
      }
    } 
}}
</script>

<style lang="scss" scoped></style>