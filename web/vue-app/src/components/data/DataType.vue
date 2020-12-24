<template>
    <div>
        <div>
            <div class="d-flex d-flex justify-content-end mb-2">
                <b-button @click="getAndUpdateNewData" variant="light">🔄</b-button>
            </div>

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
import * as miband_conn from '@/api_calls/MibandConnection.js'
import * as miband_db from '@/api_calls/MibandDb.js'

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
        }
    },
    mounted(){
        this.addDataFromLastTimestampDb().then(()=>{
            this.getDatabyDateDb(this.datevalue)
        })

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
        getAndUpdateNewData() {
            this.addDataFromLastTimestampDb().then(()=>{
                this.getDatabyDateDb(this.datevalue)
            })

            this.getDatabyDateDb(this.datevalue)
            this.generateDataSet()
        },

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

        getDatabyDateDb(inputdatestr) {
            var today = new Date(inputdatestr)
            var startTs, endTs, startstr, endstr
            //start = todays' 0:00
            startTs = new Date(today.getFullYear(), today.getMonth(), today.getDate())
            //end = todays's 23:59
            endTs = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59)
            //convert ts to str
            startstr = this.generateApiUTCTimeStr(startTs)
            endstr = this.generateApiUTCTimeStr(endTs)

            const user_id = this.$session.get('user').id
            
            miband_db.getUserLogByTimeDbApiCall(user_id, startstr, endstr).then((result)=>{
                if(result['status-code']==200) {
                    this.activitydata  = result['response-data']['logs']
                    this.getDataStatus = "OK"
                }
                else if(result['status-code']==500) {
                    this.$bvModal.show('service-error-modal')
                    this.getDataStatus = ''
                }

            })
            this.getDataStatus = "PENDING"

        },

        async getLastFetchingDataTimestampDb() {
            const band_id = this.$session.get('miband').id
            const result = await miband_db.getLastFetchingDataTimestampDbApiCall(band_id)

            var lastTs = null
            if(result['status-code']==200) {
                var lastTsStr = result['response-data']['last-fetch-timestamp']
                if(lastTsStr) {
                    if(lastTsStr==''){
                        lastTs = new Date()
                    }
                    else {
                        lastTs = new Date(lastTsStr)           
                    }
                }
            }
            else if(result['status-code']==500) {
                this.$emit('service-error')
            }

            return lastTs
            
            
        },

        async getDataFromLastTimestampMiband(){
            //get data from last ts to now
            var lastTs = await this.getLastFetchingDataTimestampDb()
            var logs = null

            if(lastTs) {
                var start, end
                start = this.generateApiTimeStr(lastTs)
                end = this.generateApiTimeStr(new Date())
                
                const result = await miband_conn.getDataMibandFrom(start, end)
                if(result['status-code']==200) {
                    logs = result['response-data']['logs']
                }
                else if(result['status-code']==500) {
                    this.$emit('service-error')
                }
            }
            
            return logs
        },

        async addDataFromLastTimestampDb() {
            const band_id = this.$session.get('miband').id
            const user_id = this.$session.get('user').id
            const logs = await this.getDataFromLastTimestampMiband()

            if(logs) {//if api called successfully
                if(Object.entries(logs).length!=0){ //if data read != null
                    var laststr = Object.keys(logs)[Object.keys(logs).length-1]
                    
                    //save dtb in utc timestamp
                    this.convertLogsToUTC(logs)
                    
                    var add_result = await miband_db.addLogsDbApiCall(user_id, band_id, logs)
                    if(add_result['status-code']==200) {
                        // const timestamp = this.generateTimestampFromApiStr(laststr)
                        // const utcStr = this.generateApiUTCTimeStr(timestamp)

                        // miband_db.setLastFetchingDataTimestampDbApiCall(band_id, utcStr)
                    }
                    else if(add_result['status-code']==500) {
                        this.$emit('service-error')
                    }
                }
            }
            
        },

        convertLogsToUTC(logs) {
            for(var ts in logs) {
                var timestamp = this.generateTimestampFromApiStr(ts)
                var apiUTCStr = this.generateApiUTCTimeStr(timestamp)
                logs[apiUTCStr] = logs[ts]
                delete logs[ts]
            }
        },

        generateApiUTCTimeStr(timestamp) {
            var result, datestr, timestr, d, M, y, h, m
            d = timestamp.getUTCDate()
            M = timestamp.getUTCMonth()+1
            y = timestamp.getUTCFullYear()
            h = timestamp.getUTCHours()
            m = timestamp.getUTCMinutes()
            if(m<10) {
                m = '0'+m
            }
            datestr = d + '.' + M + '.' + y
            timestr = h + ':' + m
            result = datestr + ' - ' + timestr
            return result

        },

        generateApiTimeStr(timestamp) {
            var result, datestr, timestr, d, M, y, h, m
            d = timestamp.getDate()
            //api string: real month 1-12| Date month system 0-11: 0: Jan, 1: Feb,...
            //--> +1
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

        generateTimestampFromApiStr(timestr) {
            // dd.MM.yyyy - hh.mm
            var result, d, M, y, h, m
            d = timestr.slice(0,2)
            //api string: real month | Date month system 0-11: 0: Jan, 1: Feb,...
            //--> -1
            M = parseInt(timestr.slice(3,5)) - 1
            y = timestr.slice(6,10)
            h = timestr.slice(13,15)
            m = timestr.slice(16,18)
            result = new Date(y, M, d, h, m)
            return result
        },

        removeHourRange(){
            this.hourvalue = null
            this.createChartData()
        }
    }
}
</script>