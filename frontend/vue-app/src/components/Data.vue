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
import GeneralData from '@/components/data/GeneralData'
import DataType from '@/components/data/DataType'
export default {
  components: {
    GeneralData,
    DataType
  },
  data() {
    return {
      miband: this.$session.get('miband'),
      hr_key: false,
      connectStatus: '',
      gdkey: false,
      miband_db_host: this.$api_hosts['miband_db_api'],
      miband_db_port: this.$api_ports['miband_db_api'],
      miband_host: this.$api_hosts['miband_api'],
      miband_port: this.$api_ports['miband_api']
    }
  },
  created() {
    var miband = this.miband
    if(miband==undefined) {
      this.getBandInfo().then((bandinfo)=>{
        this.$session.set('miband', bandinfo)
      })
    }
  },

  methods: {
    async getBandInfo() {
      const userid = this.$session.get('user').id
      try {
          const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/getbandbyuser/${userid}`)
          const result = await response.json()
          return result
      } catch (error) {
          // do something with `error`
      }
    },

    async disconnectApiCall() {
      try {
          const response = await fetch(`http://${this.miband_host}:${this.miband_port}/band/disconnect`)
          const result = await response.json()
          console.log(result)
          return result
      } catch (error) {
          // do something with `error`
      }
    },

    async connectApiCall(mac_add, auth_key) {
      try {
          const response = await fetch(`http://${this.miband_host}:${this.miband_port}/band/connect`, {
          method: 'POST',
          body: JSON.stringify({
              'mac_add': mac_add,
              'auth_key': auth_key
              }),
          headers: { 'Content-type': 'application/json; charset=UTF-8' },
          })
          const result = await response.json()
          if(result['connect-result']=='succeeded') {
            return result['band-info']
          }
          else return false
      } catch (error) {
          console.error(error)
      }
    },

    reconnect() {
      var miband = this.miband
      this.disconnectApiCall().then(
        this.connectApiCall(miband.mac_address, miband.auth_key).then((result)=>{
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
