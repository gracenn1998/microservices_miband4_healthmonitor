<template>
    <b-card title="My device">
        <b-button variant="outline-primary" class="w-100" @click="enterAddBandMode">+ Add device</b-button>
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

const miband_db_host='192.168.11.122'
const miband_db_port='5002'

export default {
    components: { 
        PairDeviceForm,
        DeviceList
    },
    data() {
        return {
            addBandMode: false,
            listkey: false,
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

        async removeBandDbApiCall(band) {
            const serial = band.serial
            try {
                const response = await fetch(`http://${miband_db_host}:${miband_db_port}/deleteband/${serial}`)
                const result = await response.json()

                // do something with `data`
                if(result['delete-result']=="succeeded")
                    return true
                else return false
            } catch (error) {
                // do something with `error`
            }
        },
        removeBand(band) {
            this.removeBandDbApiCall(band).then(()=>{
                this.$session.remove('miband')
                this.updateListDisplay()
            })
        }
    }
}
</script>