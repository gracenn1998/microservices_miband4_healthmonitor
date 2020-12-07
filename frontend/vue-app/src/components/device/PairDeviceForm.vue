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
        <b-alert variant="warning" show>Pair failed. This band is in using condition.<br> 
          If you want to pair, please hard reset the band.</b-alert>
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
      miband_db_host: this.$api_hosts['miband_db_api'],
      miband_db_port: this.$api_ports['miband_db_api'],
      miband_host: this.$api_hosts['miband_api'],
      miband_port: this.$api_ports['miband_api']
    }
  },
  methods: {
    async connectBandApiCall(mac_add, auth_key) {
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

    async addNewBandDtbApiCall(miband) {
        const user_id = this.$session.get('user').id
        const bodydata = {}
        for (var key in miband) {
          bodydata[key] = miband[key]
        }
        bodydata['user_id'] = user_id
        try {
            const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands`, {
            method: 'POST',
            body: JSON.stringify(
                bodydata
                ),
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
            })
            const result = await response.json()
            if(result['add-band-result']=='succeeded') {
              return result['band-info']
            }
            else return false
        } catch (error) {
            console.error(error)
        }
    },

    async addAvailableBandDtbApiCall(miband) {
        const user_id = this.$session.get('user').id
        const band_id = miband.id
        const bodydata = {}
        for (var key in miband) {
          bodydata[key] = miband[key]
        }
        bodydata['user_id'] = user_id
        try {
            const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/${band_id}/update-new-user`, {
            method: 'PUT',
            body: JSON.stringify(
                bodydata
                ),
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
            })
            const result = await response.json()
            if(result['add-band-result']=='succeeded') {
              return result['band-info']
            }
            else return false
        } catch (error) {
            console.error(error)
        }
    },

    async getBandBySerial(serial) {
      const params = 'serial='+serial
      try {
        const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/find-by-serial?${params}`)
        const result = await response.json()
        if(result['get-band-result']=='succeeded'){
          return result['band-info']
        }
        else return false
      }
      catch (error){
        console.log(error)
      }
    },
    

    addBand(mac_add, auth_key) {
      if(this.macaddState && this.authkeyState) {
        this.connectBandApiCall(mac_add, auth_key).then((band)=>{
          if(band) {
            //save dtb
            //assign band info to miband ref
            for(var key in band) {
              this.miband[key] = band[key]
            }

            this.getBandBySerial(band['serial']).then((band)=>{
              if(!band) { //no band with same serial
                this.addNewBandDtbApiCall(this.miband).then((result)=>{
                  if(result) {
                    this.$session.set('miband', result)
                    //finished
                    this.pairingStatus = 'OK'
                    this.$emit('update-list-display')
                  }
                })
                this.pairingStatus = 'DTB'
              }
              else { //this band has been used & added into dtb before
                if(band.user_id) { //this band is currently paired by an user
                  this.pairingStatus = 'UNAVAILABLE'
                }
                else { //this band is currently free
                  this.addAvailableBandDtbApiCall(band).then((result)=>{
                    if(result) {
                      this.$session.set('miband', result)
                      //finished
                      this.pairingStatus = 'OK'
                      this.$emit('update-list-display')
                    }
                  })
                  this.pairingStatus = 'DTB'
                }
                
              }
            })
          }
          else {
            this.pairingStatus = 'ERROR'
          }
      
        })
        
        this.pairingStatus = 'PENDING'
      }
      
    }
  }
}
</script>