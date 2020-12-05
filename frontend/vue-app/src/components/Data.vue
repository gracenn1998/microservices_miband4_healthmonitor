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
            <b-tab title="General Information" active> 
              <GeneralData :key='gdkey'/>
            </b-tab>
            <b-tab title="Step Counts">
              <StepCounts />
            </b-tab>
            <b-tab title="Heart Rate">
              <HeartRate />
            </b-tab>
        </b-tabs>
      </b-card>
    </div>
</template>

<script>
import GeneralData from '@/components/data/GeneralData'
import HeartRate from '@/components/data/HeartRate'
import StepCounts from '@/components/data/StepCounts'

const miband_db_host='192.168.11.122'
const miband_db_port='5002'
const miband_host='192.168.11.122'
const miband_port='5001'


export default {
  components: {
    GeneralData, 
    HeartRate,
    StepCounts
  },
  data() {
    return {
      miband: this.$session.get('miband'),
      hr_key: false,
      connectStatus: '',
      gdkey: false
    }
  },
  created() {
    var miband = this.miband
    if(miband==undefined) {
      this.getBandInfo().then((bandinfo)=>{
        this.$session.set('miband', bandinfo)
        this.$forceUpdate
      })
    }
  },

  methods: {
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

    async disconnectApiCall() {
      try {
          const response = await fetch(`http://${miband_host}:${miband_port}/disconnect`)
          const result = await response.json()
          console.log(result)
          return result
      } catch (error) {
          // do something with `error`
      }
    },

    async connectApiCall(mac_add, auth_key) {
      try {
          const response = await fetch(`http://${miband_host}:${miband_port}/connect`, {
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

<style scoped>

</style>
