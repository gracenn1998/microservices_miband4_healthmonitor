<template>
  <div>
    <b-card v-if="$session.get('miband')!=undefined">
      <div class="card-header d-flex justify-content-between">
        <h4>Miband</h4>
        <b-button 
          v-b-tooltip.hover title="Unpair device"
          v-b-modal.confirm-remove-modal
          variant="outline-danger"
        >✖️</b-button>

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
        <b-list-group-item class="w-25">MAC address</b-list-group-item>
        <b-list-group-item class="w-75">{{miband.mac_add}}</b-list-group-item>
      </b-list-group>
      <b-list-group horizontal>
        <b-list-group-item class="w-25">Authentic key</b-list-group-item>
        <b-list-group-item class="w-75">{{miband.auth_key}}</b-list-group-item>
      </b-list-group>
      

    </b-card>
  </div>
  
</template>

<script>
const miband_db_host='192.168.11.122'
const miband_db_port='5002'

  export default {
    created() {
      if(this.$session.get('miband')==undefined) {
        this.getBandInfo().then((bandinfo)=>{
          this.$session.set('miband', bandinfo)
          this.$emit('update-list-display')
        })
      }
    },
    data() {
      return {
        miband: this.$session.get('miband')
      }
    },
    methods: {
      emitAndCloseModal() {
        this.$emit('unpair-band', this.miband)
        this.$bvModal.hide('confirm-remove-modal')
      },

      async getBandInfo() {
        const userid = this.$session.get('user').id
        try {
            const response = await fetch(`http://${miband_db_host}:${miband_db_port}/getbandbyuser/${userid}`)
            const result = await response.json()
            return result
        } catch (error) {
            // do something with `error`
        }
        },
    }
  }
</script>