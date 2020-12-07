<template>
    <div>
        <div>
            <b-form inline class="d-flex justify-content-between">
                <b-form-datepicker id="example-datepicker" v-model="datevalue" class="mb-2 w-50"></b-form-datepicker>
                
                <div>
                    Hour range:
                    <b-form-spinbutton inline wrap min="0" max="23" v-model="hourvalue"></b-form-spinbutton>
                    <b-button class="ml-1" variant="success" @click="createChartData(hourvalue)">v</b-button>
                    <b-button class="ml-1" @click="removeHourRange">x</b-button>
                </div>
                
            </b-form>
        </div>

        <div v-if="getDataStatus === 'PENDING'">
            <b-alert variant="info" show>Getting data...</b-alert>
        </div>
        
        <b-skeleton-wrapper :loading="getDataStatus === 'PENDING'">
            <template #loading>
                <b-card>
                <b-skeleton width="85%"></b-skeleton>
                <b-skeleton width="55%"></b-skeleton>
                <b-skeleton width="70%"></b-skeleton>
                </b-card>
            </template>
            <div class="h-50">
                <DataChart :key="chartkey" :data="data" :labels="labels" :type="type"/>
            </div>
        </b-skeleton-wrapper>
    </div>
</template>


<script>
import DataChart from '@/components/data/DataChart'


var today = new Date()

export default {
    components: { DataChart },
    props: ['type'],
    data(){
        return {
            activitydata: {},
            wholedayData: {},
            hourData: {},
            labels: [],
            data: [],
            mode: -1,
            datevalue: today.getFullYear() + '-' + String(today.getMonth()+1) + '-' + today.getDate(),
            hourvalue: null,
            chartkey: false,
            getDataStatus: '',
            miband_host: this.$api_hosts['miband_api'],
            miband_port: this.$api_ports['miband_api'],
            miband_db_host: this.$api_hosts['miband_db_api'],
            miband_db_port: this.$api_ports['miband_db_api'],
            lastGetDataTime: null
        }
    },
    mounted(){
        if(this.lastGetDataTime==null){
            this.lastGetDataTime = new Date()
            this.addDataFromLastTimestampDb().then(()=>{
                this.getDatabyDateDb(this.datevalue)
                
            })
        }
        else {
            var now = new Date()
            var diff = now - this.lastGetDataTime
            if(diff >= 4*60*60*1000) {
                this.lastGetDataTime = now
                this.addDataFromLastTimestampDb().then(()=>{
                    this.getDatabyDateDb(this.datevalue)
                })
            }

        }
        this.getDatabyDateDb(this.datevalue)
        this.generateDataSet()
    },

    watch: {
        datevalue: function() {
            this.getDatabyDateDb(this.datevalue)
        },
        getDataStatus: function() {
            if(this.getDataStatus=='OK') {
                this.generateDataSet()
                this.createChartData()                    
            }
        },
        data: function() {
            this.chartkey = !this.chartkey
        },
    },

    methods: {
        generateDataSet() {
            var logs = this.activitydata
            var hourData = {}

            for(var i in logs) {
                var timestamp = logs[i].timestamp
                var tmp = new Date(timestamp)
                var hour = tmp.getHours()
                var minute = tmp.getMinutes()
                // dataOfHour["asd"] = "asd"
                if(hourData[String(hour)]==undefined){
                    hourData[String(hour)] = {}
                    if(this.type=='hr'){
                        hourData[String(hour)]['sum'] = 0
                        hourData[String(hour)]['valid-cnt']=0
                    }
                    else if (this.type=='steps'){
                        hourData[String(hour)]['sum'] = 0
                    }
                }
                var hr = logs[i].heartrate
                var steps = logs[i].steps
                hourData[String(hour)][String(minute)] = this.type=='hr'? hr : steps
                if(this.type=='hr'&& hr!=255){
                    hourData[String(hour)]['sum']+=hr
                    hourData[String(hour)]['valid-cnt']++
                }
                else if(this.type=='steps') {
                    hourData[String(hour)]['sum']+=steps
                }
            }

            var wholedayData = {}
            for(var h=0; h<24; h++){
                if(hourData[h]!=undefined)
                    wholedayData[h] = this.type=='hr'? Math.round(hourData[h]['sum']/hourData[h]['valid-cnt'])
                                                     : hourData[h]['sum']
                else  wholedayData[h] = undefined
            }
            this.wholedayData = wholedayData
            this.hourData = hourData
        },

        createChartData(mode) {
            this.labels = []
            this.data = []
            var h
            if(mode==null) {
                for(h=0; h<24; h++) {
                    this.labels.push(String(h)+':00')
                    this.data.push(this.wholedayData[h])
                }
            }
            else {
                h = mode
                var minute
                for(var m=0; m<60; m++) {
                    if (String(m).length<2) {
                        minute = '0'+String(m)
                    }
                    else minute = m
                    this.labels.push(String(h)+':'+String(minute))
                    if(this.hourData[h]!=undefined){
                        var bpm = this.hourData[h][m]
                        if(bpm==255)
                            bpm = null
                        this.data.push(bpm)
                    }
                        
                }
            }

        },

        async addLogsDb(logs) {
            const band_id = this.$session.get('miband').id
            const user_id = this.$session.get('user').id
            try {
                const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/${band_id}/${user_id}/logs`, {
                method: 'POST',
                body: JSON.stringify(logs),
                headers: { 'Content-type': 'application/json; charset=UTF-8' },
                })
                const result = await response.json()
                if(result['add-logs-result']=='succeeded'){
                    return true
                }
                else return false
            } catch (error) {
                console.error(error)
            }
        },

        async getDataByTimeApiCallDb(start, end) {
            const userid = this.$session.get('user').id
            const params = 'start='+start + '&end='+end
            try {
                const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/users/${userid}/logs/get-by-time?${params}`)
                
                const result = await response.json()
                if(result['get-logs-result']==='succeeded')
                    return result['logs']
                return false
            } catch (error) {
                // do something with `error`
            }
        },

        getDatabyDateDb(inputdatestr) {
            var date = new Date(inputdatestr)
            var day, month, year, datestr, startstr, endstr
            day = date.getDate()
            month = date.getMonth()+1
            year = date.getFullYear()
            datestr = day + '.' + month + '.' + year
            startstr = datestr + ' - 0:00'
            endstr = datestr + ' - 23:59'
            this.getDataByTimeApiCallDb(startstr, endstr).then((result)=>{
                this.activitydata  = result 
                this.getDataStatus = "OK"
            })
            this.getDataStatus = "PENDING"

        },

        async getLastFetchingDataTimestampDb() {
            const bandid = this.$session.get('miband').id
            try {
                const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/${bandid}/last-fetch-time`)
                const result = await response.json()
                if(result['get-timestamp-result']=='succeeded'){
                    return result['last-fetch-timestamp']
                }
                else return false
            } catch (error){
                console.log(error)
            }
        },
        
        async getDataFromLastTimestampMiband(){
            const lastTsStr = await this.getLastFetchingDataTimestampDb()
            var lastTs
            if(lastTsStr==''){
                lastTs = new Date()
            }
            else {
                lastTs = new Date(lastTsStr)           
            }

            const logs = await this.getDataMibandFrom(lastTs)
            return logs
        },

        async addDataFromLastTimestampDb() {
            const logs = await this.getDataFromLastTimestampMiband()
            if(logs) {
                if(Object.entries(logs).length!=0){
                    var laststr = Object.keys(logs)[Object.keys(logs).length-1]
                    await this.addLogsDb(logs)
                    this.setLastFetchingDataTimestampDb(laststr)
                }
            }
            
        },

        generateApiTimeStr(timestamp) {
            var result, datestr, timestr, d, M, y, h, m
            d = timestamp.getDate()
            M = timestamp.getMonth()+1
            y = timestamp.getFullYear()
            h = timestamp.getHours()
            m = timestamp.getMinutes()
            if(m<10) {
                m = '0'+m
            }
            datestr = d + '.' + M + '.' + y
            timestr = h + ':' + m
            result = datestr + ' - ' + timestr
            return result
        },

        async getDataMibandFrom(timestamp) {
            var start, end
            start = this.generateApiTimeStr(timestamp)
            end = this.generateApiTimeStr(new Date())
            const params = 'start='+start + '&end='+end
            try {
                const response = await fetch(`http://${this.miband_host}:${this.miband_port}/band/activitydata?${params}`)
                const result = await response.json()
                if(result['log-data-result']=='succeeded'){
                    return result['logs']
                }
                else return false
            }
            catch (error) {
                console.log(error);
            }
            
        },

        async setLastFetchingDataTimestampDb(last){
            const bandid = this.$session.get('miband').id
            try{
                const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/${bandid}/last-fetch-time`, {
                method: 'POST',
                body: JSON.stringify({
                    'last': last
                    }),
                headers: { 'Content-type': 'application/json; charset=UTF-8' },
                })
                const result = response.json()
                if(result['set-timestamp-result']=='succeeded') {
                    return true
                }
                return false
            }
            catch (error) {
                console.log(error)
            }
        },

        removeHourRange(){
            this.hourvalue = null
            this.createChartData()
        }
    }
}
</script>