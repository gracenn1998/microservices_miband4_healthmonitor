import {miband_db_api_host as miband_db_host, miband_db_api_port as miband_db_port} from './ApiConfig.js'

export async function pairNewBandDtbApiCall(uid, miband) {
    var result = {}
    var bodydata = {}
    for (var key in miband) {
      bodydata[key] = miband[key]
    }
    bodydata['user_id'] = uid
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands`, {
        method: 'POST',
        body: JSON.stringify(
            bodydata
            ),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function pairAvailableBandDtbApiCall(uid, miband, bid) {
    var result = {}
    var bodydata = {}
    for (var key in miband) {
      bodydata[key] = miband[key]
    }
    bodydata['user_id'] = uid
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/${bid}/update-new-user`, {
        method: 'PUT',
        body: JSON.stringify(
            bodydata
            ),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function getBandBySerial(serial) {
    var result = {}
    const params = 'serial='+serial
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/find-by-serial?${params}`)
        result['status-code'] = response.status
            if(result['status-code']==200) {
                result['response-data'] = await response.json()
            }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}


export async function getUserBandInfo(uid) {
    var result = {}
    const params = '?user_id='+uid
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/find-by-userid${params}`)
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function getUserLogByTimeDbApiCall(uid, start, end) {
    var result = {}
    const params = 'start='+start + '&end='+end
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/users/${uid}/logs/get-by-time?${params}`)
        
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function getLastFetchingDataTimestampDbApiCall(bid) {
    var result = {}
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/${bid}/last-fetch-time`)
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function setLastFetchingDataTimestampDbApiCall(bid, last){
    var result = {}
    try{
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/${bid}/last-fetch-time`, {
        method: 'POST',
        body: JSON.stringify({
            'last': last
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}


export async function addLogsDbApiCall(uid, bid, logs) {
    var result = {}
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/${bid}/${uid}/logs`, {
        method: 'POST',
        body: JSON.stringify(logs),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function unpairBandDbApiCall(bid) {
    var result = {}
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/bands/${bid}/unpair`)
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}

export async function deleteUserLogsApiCall(uid) {
    var result = {}
    try {
        const response = await fetch(`http://${miband_db_host}:${miband_db_port}/v1/users/${uid}/logs`, {
            method: 'DELETE'
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.log(error)
        result['status-code'] = 500
    }

    return result
}