<template>
    <b-card title="My device">
        <b-button v-if="$session.get('miband')==undefined" 
            variant="outline-primary" class="w-100" 
            @click="enterAddBandMode"
        >+ Add Miband</b-button>
        <pair-device-form v-if="addBandMode" 
            @exit-add-band-mode="exitAddBandMode"
            @update-list-display="updateListDisplay"
        />
        <device-list class="mt-1" :key="listkey"
            @unpair-band="removeBand"
            @update-list-display="updateListDisplay"
        />
    </b-card>
</template>

<script>
import PairDeviceForm from '@/components/device/PairDeviceForm'
import DeviceList from '@/components/device/DeviceList'

export default {
    components: { 
        PairDeviceForm,
        DeviceList
    },
    data() {
        return {
            addBandMode: false,
            listkey: false,
            miband_db_host: this.$api_hosts['miband_db_api'],
            miband_db_port: this.$api_ports['miband_db_api'],
            miband_host: this.$api_hosts['miband_api'],
            miband_port: this.$api_ports['miband_api']
        }
    },
    methods: {
        enterAddBandMode() {
            this.addBandMode = true
        },
        exitAddBandMode() {
            this.addBandMode = false
        },

        updateListDisplay() {
            this.listkey = !this.listkey
        },

        async unpairBandDbApiCall() {
            const bandid = this.$session.get('miband').id
            try {
                const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/${bandid}/unpair`)
                const result = await response.json()

                // do something with `data`
                if(result['unpair-band-result']=="succeeded")
                    return true
                else return false
            } catch (error) {
                // do something with `error`
            }
        },

        async disconnectApiCall() {
            try {
                const response = await fetch(`http://${this.miband_host}:${this.miband_port}/band/disconnect`)
                const result = await response.json()
                return result
            } catch (error) {
                // do something with `error`
            }
        },

        removeBand() {
            // need delete all logs
            this.disconnectApiCall()
            this.unpairBandDbApiCall().then(()=>{
                this.$session.remove('miband')
                this.updateListDisplay()
            })
        }
    }
}
</script>