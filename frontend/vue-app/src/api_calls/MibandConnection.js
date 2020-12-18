import {miband_api_host as miband_host, miband_api_port as miband_port} from './ApiConfig.js'

export async function connectApiCall(mac_add, auth_key) {
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/connect`, {
        method: 'POST',
        body: JSON.stringify({
            'mac_add': mac_add,
            'auth_key': auth_key
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const result = await response.json()
        if(result['connect-result']=='succeeded') {
          return result['band-info']
        }
        else return false
    } catch (error) {
        console.error(error)
    }
}

export async function disconnectApiCall() {
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/disconnect`)
        const result = await response.json()
        return result
    } catch (error) {
        // do something with `error`
    }
}

export async function getDataMibandFrom(start, end) {
    const params = 'start='+start + '&end='+end
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/activitydata?${params}`)
        const result = await response.json()
        if(result['log-data-result']=='succeeded'){
            return result['logs']
        }
        else return false
    }
    catch (error) {
        console.log(error);
    }
    
}

export async function getGeneralDataApiCall() {
    try {
        const response = await fetch(`http://${miband_host}:${miband_port}/band/general`)
        const result = await response.json()
        if(result['get-step-result']==='succeeded')
            return result['stepinfo']
        return false
    } catch (error) {
        // do something with `error`
    }
}