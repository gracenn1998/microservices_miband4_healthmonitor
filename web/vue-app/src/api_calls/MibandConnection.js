import {miband_api_host as miband_host, miband_api_port as miband_port} from './ApiConfig.js'

export async function connectApiCall(mac_add, auth_key) {
    var result = {}
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/connect`, {
        method: 'POST',
        body: JSON.stringify({
            'mac_add': mac_add,
            'auth_key': auth_key
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    } catch (error) {
        console.error(error)
        result['status-code'] = 500
    }

    return result
}

export async function disconnectApiCall() {
    var result = {}
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/disconnect`)
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    } catch (error) {
        console.error(error)
        result['status-code'] = 500
    }
    
    return result
}

export async function getDataMibandFrom(start, end) {
    var result = {}
    const params = 'start='+start + '&end='+end
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/activitydata?${params}`)
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    } catch (error) {
        console.error(error)
        result['status-code'] = 500
    }
    
    return result
}

export async function getGeneralDataApiCall() {
    var result = {}
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/general`)
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    } catch (error) {
        console.error(error)
        result['status-code'] = 500
    }

    return result
}