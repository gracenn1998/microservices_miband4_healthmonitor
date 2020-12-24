import {user_db_api_host as user_db_host, user_db_api_port as user_db_port} from './ApiConfig.js'

export async function signinApiCall(email, password) {
    var result = {}
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/login`, {
        method: 'POST',
        body: JSON.stringify({
            'email': email,
            'password': password
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    } catch (error) {
        console.error(error)
        result['status-code']=500
    }

    return result
}

export async function getUserByEmailApiCall(email) {
    var result = {}
    const params = 'email='+email
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/find-by-email?${params}`)
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

export async function addUserApiCall(user) {
    var result = {}
    try {
        var response = await fetch(`http://${user_db_host}:${user_db_port}/users`, {
        method: 'POST',
        body: JSON.stringify(user),
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

export async function updateNameApiCall(uid, newName) {
    var result = {}
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/${uid}/fullname`, {
        method: 'PUT',
        body: JSON.stringify({
            'fullname': newName,
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        result['status-code'] = response.status
        if(result['status-code']==200) {
            result['response-data'] = await response.json()
        }
    }
    catch (error) {
        console.error(error)
        result['status-code'] = 500
    }

    return result
}

export async function deleteUserApiCall(uid) {
    var result = {}
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/${uid}`, {
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

export async function changePasswordApiCall(uid, currentPassword, newPassword) {
    var result = {}
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/${uid}/change-password`, {
        method: 'POST',
        body: JSON.stringify({
            'cur_password': currentPassword,
            'new_password': newPassword
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