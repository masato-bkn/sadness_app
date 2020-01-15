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
        <Event />
      </div>
    </div>
    <Header />
    <main class="contents">
      <nuxt />
    </main>
  </div>
</template>

<script>
import Header from "~/components/Header"
import Event from "~/components/Event"

export default {
  components: {
    Header,
    Event
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
