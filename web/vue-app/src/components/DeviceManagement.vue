<template>
    <div>
        <b-card title="My device">
            <b-button v-if="$session.get('miband')==undefined" 
                variant="outline-primary" class="w-100" 
                @click="enterAddBandMode"
            >+ Add Miband</b-button>
            <pair-device-form v-if="addBandMode" 
                @exit-add-band-mode="exitAddBandMode"
                @update-list-display="updateListDisplay"
                @service-error="$bvModal.show('service-error-modal')"
            />
            <device-list class="mt-1" :key="listkey"
                @unpair-band="removeBand"
                @update-list-display="updateListDisplay"
            />
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

import PairDeviceForm from '@/components/device/PairDeviceForm'
import DeviceList from '@/components/device/DeviceList'

export default {
    components: { 
        PairDeviceForm,
        DeviceList
    },
    created() {
        //get data if not stored in session yet
        if(this.$session.get('miband')==undefined) {
            const userid = this.$session.get('user').id

            miband_db.getUserBandInfo(userid).then((result)=>{
                if(result['status-code']==200) {
                    this.$session.set('miband', result['response-data']['band-info'])
                    this.$emit('update-list-display')
                }
            })
        }
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

        removeBand() {
            const band_id = this.$session.get('miband').id
            miband_conn.disconnectApiCall()
            miband_db.unpairBandDbApiCall(band_id).then((result)=>{
                if(result['status-code']==200) {
                    this.$session.remove('miband')
                    this.updateListDisplay()
                }
                else if(result['status-code']==500) {
                    this.$bvModal.show('service-error-modal')
                }

            })
        }
    }
}
</script>