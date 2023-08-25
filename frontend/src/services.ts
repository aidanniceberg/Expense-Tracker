import { API_URL } from "./constants";
import { AuthToken, User } from './types';

export const login = (username: string, password: string): Promise<AuthToken> => {
    return fetch(`${API_URL}/token`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw Error(`Encountered a ${response.status} error: ${response.json()}`)
            }
        });
}

export const getCurrentUser = (token: string): Promise<User> => {
    return fetch(`${API_URL}/users/me`, {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw Error(`Encountered an HTTP error: ${response.status}: ${response.json()}`)
            }
        });
}
