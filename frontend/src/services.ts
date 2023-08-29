import { API_URL } from "./constants";
import { AuthToken, Group, User } from './types';

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
                throw new Error(`Encountered a ${response.status} error: ${response.json()}`)
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
                throw new Error(`Encountered an HTTP error: ${response.status}: ${response.json()}`)
            }
        });
}

export const getUsers = (token: string): Promise<Array<User>> => {
    return fetch(`${API_URL}/users`, {
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
                throw new Error(`Encountered an HTTP error: ${response.status}: ${response.json()}`)
            }
        });
}

export const getGroups = (token: string): Promise<Array<Group>> => {
    return fetch(`${API_URL}/groups`, {
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
                throw new Error(`Encountered an HTTP error: ${response.status}: ${response.json()}`)
            }
        });
}

export const createGroup = (token: string, name: string, members: Array<number>) => {
    const memberParams = members.map((member) => `members=${member}`).join('&');
    const urlParams = `name=${name}&${memberParams}`;
    return fetch(`${API_URL}/groups?${urlParams}`, {
        method: 'POST',
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
                throw new Error(`Encountered an HTTP error: ${response.status}: ${response.json()}`)
            }
        });
}

export const getGroup = (token: string, id: number): Promise<Group> => {
    return fetch(`${API_URL}/groups/${id}`, {
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
                throw new Error(`Encountered an HTTP error: ${response.status}: ${response.json()}`)
            }
        })
        .catch((e) => {
            throw new Error(`Encountered an error: ${e}`);
        })
}
