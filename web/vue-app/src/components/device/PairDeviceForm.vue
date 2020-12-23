<template>
  <div>
    <b-card-title class="text-center mt-2">
      <div v-if="pairingStatus === 'OK'">
        <b-alert variant="success" show>Pairing succeeded</b-alert>
      </div>
      <div v-if="pairingStatus === 'ERROR'">
        <b-alert variant="danger" show>Pair failed. Please check data correctness or data format</b-alert>
      </div>
      <div v-if="pairingStatus === 'PENDING'">
        <b-alert variant="info" show>Pairing...</b-alert>
      </div>
      <div v-if="pairingStatus === 'DTB'">
        <b-alert variant="info" show>Adding to database</b-alert>
      </div>
      <div v-if="pairingStatus === 'UNAVAILABLE'">
        <b-alert variant="warning" show>Pair failed. This band is paired by another account.</b-alert>
      </div>
      
      <b-skeleton-wrapper :loading="pairingStatus === 'PENDING' || pairingStatus === 'DTB'">
        <template #loading>
        <b-card>
          <b-skeleton width="85%"></b-skeleton>
          <b-skeleton width="55%"></b-skeleton>
          <b-skeleton width="70%"></b-skeleton>
        </b-card>
      </template>
      <b-form @submit.prevent="addBand" v-if="pairingStatus !== 'OK'">
          <b-form-group 
            label="MAC address"
            :invalid-feedback="invalidMACadd"
            :state="macaddState"
          >
            <b-form-input class="w-100 mb-1"
              :state="macaddState"
              v-model="miband.mac_address"
              required
              placeholder="Example: a1:c2:3d:4e:f5:6a"
            ></b-form-input>
          </b-form-group>

          <b-form-group 
            label="Authentic key"
            :invalid-feedback="invalidAuthkey"
            :state="authkeyState"
          >
            <b-form-input class="w-100 mb-1"
              :state="authkeyState"
              v-model="miband.auth_key"
              required
              placeholder="Example: 8fa9b42078627a654d22beff985655db"
            ></b-form-input>
          </b-form-group>
          <div>
              <b-button @click="addBand(miband.mac_address, miband.auth_key)" variant="outline-success" class="mr-1">➕</b-button>
              <b-button @click="$emit('exit-add-band-mode')" variant="outline-danger">✖️</b-button>
          </div>
      </b-form>
      </b-skeleton-wrapper>
    </b-card-title>
  </div>
</template>

<script>
import * as miband_conn from '@/api_calls/MibandConnection.js'
import * as miband_db from '@/api_calls/MibandDb.js'

export default {
  computed: {
    macaddState() {
      var regex = /^(([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}[,]?)+$/i;
      
      if(this.miband.mac_address=='') {
        return null
      }
      return regex.test(this.miband.mac_address)
    },
    authkeyState() {
      if(this.miband.auth_key=='') {
        return null
      }
      return this.miband.auth_key.length == 32
    },
    invalidMACadd() {
      if (this.miband.mac_address.length >= 17) {
        return  'Please check your format. Example: a1:b2:c3:d4:e5:f6'
      }
      return null
    },
    invalidAuthkey() {
      if (this.miband.auth_key.length > 0) {
        return  'Authentic key length is 32. Example: 8fa9b42078627a654d22beff985655db'
      }
      return null
    },
  },
  data() {
    return {
      miband: {
          mac_address: 'E3:07:72:26:D4:6B',
          auth_key: '2f20ba44fdcf54ca0c2c37cad1f85487'
      },
      pairingStatus: null,
    }
  },
  methods: {
    async addBand(mac_add, auth_key) {
      //reset error msg
      this.pairingStatus = null

      const user_id = this.$session.get('user').id

      if(this.macaddState && this.authkeyState) {
        this.pairingStatus = 'PENDING'
        var result = await miband_conn.connectApiCall(mac_add, auth_key)
        
        if(result['status-code']==200) {
          var connectBand = result['response-data']['band-info']
          if(connectBand) {
            for(var key in connectBand) {
              this.miband[key] = connectBand[key]
            }
            var result2 =  await miband_db.getBandBySerial(connectBand['serial'])

            if(result2['status-code']==204) { //no band with given serial found
              
              
              this.pairingStatus = 'DTB'


              var result3 = await miband_db.pairNewBandDtbApiCall(user_id, this.miband)
              if(result3['status-code']==200) {
                this.$session.set('miband', result3['response-data']['band-info'])
                //finished
                this.pairingStatus = 'OK'
                this.$emit('update-list-display')
              }

              else if(result3['status-code']==500) {
                miband_conn.disconnectApiCall()
                this.pairingStatus = ''
                this.$emit('service-error')
              }
            }

            else if(result2['status-code']==200) { //band with given serial found
              var dbBand = result2['response-data']['band-info']

              if(dbBand.user_id) { //uid exist -> band is pair by that uid -> unable to pair
                this.pairingStatus = 'UNAVAILABLE'
              }

              else { //this band is currently free
                this.pairingStatus = 'DTB'
                
                var result4 = await miband_db.pairAvailableBandDtbApiCall(user_id, this.miband, dbBand.id)
                if(result4['status-code']==200) {
                  this.$session.set('miband', result4['response-data']['band-info'])
                  //finished
                  this.pairingStatus = 'OK'
                  this.$emit('update-list-display')
                }
                else if(result4['status-code']==500) {
                  miband_conn.disconnectApiCall()
                  this.pairingStatus = ''
                  this.$emit('service-error')
                }
                
              }
            }

            else if(result['status-code']==500) {
              miband_conn.disconnectApiCall()
              this.pairingStatus = ''
              this.$emit('service-error')
            }

          } else { //pair failed
            this.pairingStatus = 'ERROR'
          }
          
        }
        else if(result['status-code']==500) {
          this.$emit('service-error')
        }
        
      }
      
    },
  }
}
</script>