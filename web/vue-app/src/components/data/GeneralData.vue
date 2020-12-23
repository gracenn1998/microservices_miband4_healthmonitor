<template>
    <div>
        <div class="d-flex d-flex justify-content-end mb-2">
            <b-button @click="getGeneralData" variant="light">🔄</b-button>
        </div>
        
        <b-list-group v-if="generaldata">
            <b-list-group-item class="d-flex justify-content-between align-items-center">
                <h5>Steps count</h5>
                <b-avatar :text="String(generaldata['steps'])" size="4em" variant="success"></b-avatar>
            </b-list-group-item>

            <b-list-group-item class="d-flex justify-content-between align-items-center">
                <h5>Burned fat</h5>
                <b-avatar :text="String(generaldata['fat_burned'])" size="4em" variant="success"></b-avatar>
            </b-list-group-item>

            <b-list-group-item class="d-flex justify-content-between align-items-center">
                <h5>Burned calories</h5>
                <b-avatar :text="String(generaldata['calories'])" size="4em" variant="success"></b-avatar>
            </b-list-group-item>

            <b-list-group-item class="d-flex justify-content-between align-items-center">
                <h5>Travelled distance in meter(s)</h5>
                <b-avatar :text="String(generaldata['meters'])" size="4em" variant="success"></b-avatar>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
import * as miband_conn from '@/api_calls/MibandConnection.js'

export default {
    data() {
        return {
            generaldata: null,
        }
    },
    mounted() {
        if(this.$session.get('miband')!=undefined) {
            this.getGeneralData()
        }
    },
    methods: {
        getGeneralData() {
            miband_conn.getGeneralDataApiCall().then((result)=>{
                if(result['status-code']==200) {
                    var data = result['response-data']['stepinfo']
                    if(data) {
                        this.generaldata = data
                    }
                }
                else if(result['status-code']==500) {
                    this.$emit('service-error')
                }
                
            })
        },
    }
}
</script>