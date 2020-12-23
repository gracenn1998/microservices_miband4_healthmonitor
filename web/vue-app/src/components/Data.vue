<template>
    <div class="w-50 mx-auto mt-3">
        <b-card no-body >
          <b-button @click="reconnect" variant="primary">Reconnect</b-button>
          <div v-if="connectStatus === 'ERROR'">
            <b-alert variant="danger" show>Error happened while connecting. Please try again or refresh your Bluetooth connection</b-alert>
          </div>
          <div v-if="connectStatus === 'PENDING'">
            <b-alert variant="info" show>Connecting...</b-alert>
          </div>
          <b-tabs card>
            <b-tab title="General Information" active lazy> 
              <GeneralData :key='gdkey' 
              @service-error="$bvModal.show('service-error-modal')"
              />
            </b-tab>
            <b-tab title="Step Counts" lazy>
              <DataType :type="'steps'" @service-error="$bvModal.show('service-error-modal')" />
            </b-tab>
            <b-tab title="Heart Rate" lazy>
              <DataType :type="'hr'" @service-error="$bvModal.show('service-error-modal')"/>
            </b-tab>
        </b-tabs>
      </b-card>

      <b-modal id="service-error-modal" title="Server Error">
          <div class="d-block text-center">
              <h5>Some error happened...</h5>
              <h1>🛠️</h1>
              <h5>Please try again later</h5>
          </div>
      </b-modal>
    </div>
</template>

<script>
import * as miband_conn from '@/api_calls/MibandConnection.js'
import * as miband_db from '@/api_calls/MibandDb.js'

import GeneralData from '@/components/data/GeneralData'
import DataType from '@/components/data/DataType'

export default {
  components: {
    GeneralData,
    DataType
  },
  data() {
    return {
      hr_key: false,
      connectStatus: '',
      gdkey: false,
    }
  },
  created() {
    //get data if not stored in session yet
    if(this.$session.get('miband')==undefined) {
      const userid = this.$session.get('user').id

      miband_db.getUserBandInfo(userid).then((bandinfo)=>{
        if(bandinfo){
          this.$session.set('miband', bandinfo)
          this.$emit('update-list-display')
        }
      })
    }
  },

  methods: {
    reconnect() {
      var miband = this.$session.get('miband')
      miband_conn.disconnectApiCall().then(
        miband_conn.connectApiCall(miband.mac_address, miband.auth_key).then((result)=>{
          if(result['status-code']==200) {
            var band = result['response-data']['band-info']
            if(band) {
              this.connectStatus='OK'
              this.gdkey = !this.gdkey
            }
            else {
              this.connectStatus='ERROR'
            }
          }
          else if(result['status-code']==500) {
              this.$bvModal.show('service-error-modal')
              this.connectStatus = ''
          }
        })
      )
      this.connectStatus='PENDING'
    }
  }
}
</script>
