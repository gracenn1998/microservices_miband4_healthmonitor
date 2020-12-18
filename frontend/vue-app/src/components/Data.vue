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
              <GeneralData :key='gdkey'/>
            </b-tab>
            <b-tab title="Step Counts" lazy>
              <DataType :type="'steps'" />
            </b-tab>
            <b-tab title="Heart Rate" lazy>
              <DataType :type="'hr'" />
            </b-tab>
        </b-tabs>
      </b-card>
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
          if(result) {
            this.connectStatus='OK'
            this.gdkey = !this.gdkey
          }
          else {
            this.connectStatus='ERROR'
          }
        })
      )
      this.connectStatus='PENDING'
    }
  }
}
</script>
