<template>
    <div v-if="generaldata">
        <div class="d-flex d-flex justify-content-end mb-2">
            <b-button @click="getGeneralData" variant="light">🔄</b-button>
        </div>
        
        <b-list-group>
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
                <h5>Travelled distance</h5>
                <b-avatar :text="String(generaldata['meters'])" size="4em" variant="success"></b-avatar>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<script>
const miband_host='192.168.11.122'
const miband_port='5001'
export default {
    // props: ['generaldata'],
    data() {
        return {
            generaldata: null
        }
    },
    created() {
        if(this.$session.get('miband')!=undefined) {
            this.getGeneralData()
        }
    },
    methods: {
        async getGeneralDataApiCall() {
        try {
            const response = await fetch(`http://${miband_host}:${miband_port}/getsteps`)
            const result = await response.json()
            if(result['get-step-result']==='succeeded')
                return result['stepinfo']
            return false
        } catch (error) {
            // do something with `error`
        }
      },

      getGeneralData() {
        this.getGeneralDataApiCall().then((result)=>{
            if(result) {
                this.generaldata = result
            }
          })
      },
    }
}
</script>