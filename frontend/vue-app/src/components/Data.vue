<template>
    <div>
        <b-card>
            <vue-tabs type="pills">
                <v-tab title="General Information">
                    <Generaldata />
                </v-tab>

                <v-tab title="Step Counts">
                    Second tab content
                </v-tab>

                <v-tab title="Heart Rate">
                    Third tab content
                </v-tab>
            </vue-tabs>
        </b-card>
    </div>
</template>

<script>
import {VueTabs, VTab} from 'vue-nav-tabs/dist/vue-tabs.js'
import 'vue-nav-tabs/themes/vue-tabs.css'

import Generaldata from './data/Generaldata.vue'

export default {
    components: {
        VueTabs,
        VTab,
        Generaldata
    }    
}
</script>

<style scoped>

</style>
