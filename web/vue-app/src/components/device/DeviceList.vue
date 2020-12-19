<template>
  <div>
    <b-card v-if="$session.get('miband')!=undefined">
      <div class="card-header d-flex justify-content-between">
        <h4>Miband</h4>
        <div>
          <!-- <b-button 
            v-b-tooltip.hover title="Edit"
            v-b-modal.confirm-remove-modal
            variant="outline-primary"
          >📝</b-button> -->
          <b-button  class="ml-2"
            v-b-tooltip.hover title="Unpair"
            v-b-modal.confirm-remove-modal
            variant="outline-danger"
          >✖️</b-button>
        </div>
        

        <b-modal id="confirm-remove-modal" hide-footer title="Confirmation">
          <div class="d-block text-center">
            <h4>Do you really want to unpair this device?</h4>
          </div>
          <div class="d-flex justify-content-end">
            <b-button class="mt-3 mr-3"  @click="$bvModal.hide('confirm-remove-modal')">Cancel</b-button>
            <b-button class="mt-3 mr-4" variant="danger" @click="emitAndCloseModal()">Unpair</b-button>
          </div>
          
        </b-modal>
      </div>

      <b-list-group horizontal>
        <b-list-group-item class="w-25">MAC</b-list-group-item>
        <b-list-group-item class="w-75">{{miband.mac_address}}</b-list-group-item>
      </b-list-group>
      <b-list-group horizontal>
        <b-list-group-item class="w-25">Key</b-list-group-item>
        <b-list-group-item class="w-75">{{miband.auth_key}}</b-list-group-item>
      </b-list-group>
      

    </b-card>
  </div>
  
</template>

<script>

export default {
  data() {
    return {
      miband: this.$session.get('miband'),
    }
  },
  methods: {
    emitAndCloseModal() {
      this.$emit('unpair-band')
      this.$bvModal.hide('confirm-remove-modal')
    },
  }
}
</script>