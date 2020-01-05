<template>
  <div class="background">
    <div
      id="eventModal"
      class="modal fade"
      data-backdrop="static"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
      v-on="dialog()"
    >
      <div class="modal-dialog" role="document">
        <eventDialog />
      </div>
    </div>
    <TheHeader />
    <main class="contents">
      <nuxt />
    </main>
  </div>
</template>

<script>
import TheHeader from "~/components/common/TheHeader"
import eventDialog from "~/components/common/Dialog"

export default {
  components: {
    TheHeader,
    eventDialog
  },
  methods: {
    /**
     * モーダル表示
     */
    dialog() {
      if (this.$store.state.event.category != "") {
        $("#eventModal").modal("show")
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~assets/scss/index.scss";
</style>
