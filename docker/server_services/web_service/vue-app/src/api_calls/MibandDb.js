import {miband_db_api_host as miband_db_host, miband_db_api_port as miband_db_port} from './ApiConfig.js'

export async function pairNewBandDtbApiCall(uid, miband) {
    const bodydata = {}
    for (var key in miband) {
      bodydata[key] = miband[key]
    }
    bodydata['user_id'] = uid
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands`, {
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
}

export async function pairAvailableBandDtbApiCall(uid, miband) {
    const band_id = miband.id
    const bodydata = {}
    for (var key in miband) {
      bodydata[key] = miband[key]
    }
    bodydata['user_id'] = uid
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands/${band_id}/update-new-user`, {
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
}

export async function getBandBySerial(serial) {
  const params = 'serial='+serial
  try {
    const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands/find-by-serial?${params}`)
    const result = await response.json()
    if(result['get-band-result']=='succeeded'){
      return result['band-info']
    }
    else return false
  }
  catch (error){
    console.log(error)
  }
}


export async function getUserBandInfo(uid) {
    const params = '?user_id='+uid
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands/find-by-userid${params}`)
        const result = await response.json()
        if(result['get-band-result']=='succeeded'){
        return result['band-info']
        }
        return false
    } catch (error) {
        // do something with `error`
    }
}

export async function getUserLogByTimeDbApiCall(uid, start, end) {
    const params = 'start='+start + '&end='+end
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/users/${uid}/logs/get-by-time?${params}`)
        
        const result = await response.json()
        if(result['get-logs-result']==='succeeded')
            return result['logs']
        return false
    } catch (error) {
        // do something with `error`
    }
}

export async function getLastFetchingDataTimestampDbApiCall(bid) {
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands/${bid}/last-fetch-time`)
        const result = await response.json()
        if(result['get-timestamp-result']=='succeeded'){
            return result['last-fetch-timestamp']
        }
        else return false
    } catch (error){
        console.log(error)
    }
}

export async function setLastFetchingDataTimestampDbApiCall(bid, last){
    try{
        const response = await fetch(`http://${this.miband_db_host}:${this.miband_db_port}/bands/${bid}/last-fetch-time`, {
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
}


export async function addLogsDbApiCall(uid, bid, logs) {
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands/${bid}/${uid}/logs`, {
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
}

export async function unpairBandDbApiCall(bid) {
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/bands/${bid}/unpair`)
        const result = await response.json()

        // do something with `data`
        if(result['unpair-band-result']=="succeeded")
            return true
        else return false
    } catch (error) {
        // do something with `error`
    }
}

export async function deleteUserLogsApiCall(uid) {
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/users/${uid}/logs`, {
            method: 'DELETE'
        })
        const result = await response.json()
        if(result['delete-result']=='succeeded') {
            return true
        }
        return false
    }
    catch (error) {
        console.log(error)
    }
}