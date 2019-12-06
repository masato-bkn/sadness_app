<template>
  <div style="background-color: rgb(164, 222, 214); height: 825px;">
      <div class="modal fade" v-on="dialog()" id="eventModal" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <eventDialog />
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
import eventDialog from "~/components/common/Dialog";

export default {
  components: {
    TheHeader,
    eventDialog
  },
  methods:{
    /**
     * モーダル表示
     */
    dialog(){
      if (this.$store.state.event.category != "") {
        $("#eventModal").modal("show")
      }
    }
  }
}
</script>

<style lang="scss" scoped></style>