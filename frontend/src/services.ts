import { API_URL } from "./constants";
import { User } from './types';
import { generateLoginParams, getToken } from "./utils";

export const login = (data: FormData): Promise<number> => {
    return fetch(`${API_URL}/token`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: generateLoginParams(data)
    })
        .then((response) => response.status)
}

export const getCurrentUser = (): Promise<User> => {
    return fetch(`${API_URL}/users/me`, {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        }
    })
        .then((response) => response.json())
}
