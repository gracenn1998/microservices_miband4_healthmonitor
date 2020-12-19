import {user_db_api_host as user_db_host, user_db_api_port as user_db_port} from './ApiConfig.js'

export async function signinApiCall(email, password) {
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/login`, {
        method: 'POST',
        body: JSON.stringify({
            'email': email,
            'password': password
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const result = await response.json()
        if (result['login-result']=='succeeded') { //sign in successfully
        return result['user']
        }
        // if signin failed
        return false
    } catch (error) {
        console.error(error)
    }
}

export async function validateEmailApiCall(email) {
    const params = 'email='+email
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/find-by-email?${params}`)
        const result = await response.json()
        if (result.user!=null) {
        return false
        }
        return true
    } catch (error) {
        console.error(error)
    }
}

export async function addUserApiCall(user) {
    try {
        await fetch(`http://${user_db_host}:${user_db_port}/users`, {
        method: 'POST',
        body: JSON.stringify(user),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
    } catch (error) {
        console.error(error)
    }
}

export async function updateNameApiCall(uid, newName) {
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/${uid}/fullname`, {
        method: 'PUT',
        body: JSON.stringify({
            'fullname': newName,
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const user = await response.json()
        return user
    } catch (error) {
        console.error(error)
    }
}

export async function deleteUserApiCall(uid) {
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/${uid}`, {
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

export async function changePasswordApiCall(uid, currentPassword, newPassword) {
    try {
        const response = await fetch(`http://${user_db_host}:${user_db_port}/users/${uid}/change-password`, {
        method: 'POST',
        body: JSON.stringify({
            'cur_password': currentPassword,
            'new_password': newPassword
            }),
        headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const result = await response.json()
        if (result['change-pw-result']=='succeeded') { //sign in successfully
            return true
        }
        return false
    } catch (error) {
        console.error(error)
    }
}