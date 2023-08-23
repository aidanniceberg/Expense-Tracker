import { ACCESS_TOKEN_KEY } from "./constants";


export const getCookies = (): { [key: string] : string } => {
    const cookiesArray = document.cookie.split(';');
    let cookies: { [key: string] : string } = {};
    cookiesArray.forEach((cookie) => {
        const pair = cookie.split('=');
        cookies[pair[0]] = pair[1];
    })
    return cookies;
}

export const getToken = (): string => {
    const cookies = getCookies()
    if (ACCESS_TOKEN_KEY in cookies) {
        return cookies[ACCESS_TOKEN_KEY];
    } else {
        throw Error('Access token not found');
    }
}

export const generateLoginParams = (data: FormData): string => {
    const grantType = data.get('grantType') ?? '';
    const username = data.get('username') ?? '';
    const password = data.get('password') ?? '';
    const scope = data.get('scope') ?? '';
    const clientId = data.get('clientId') ?? '';
    const clientSecret = data.get('clientSecret') ?? '';

    return `grant_type=${grantType}&username=${username}&password=${password}&scope=${scope}&client_id=${clientId}&client_secret=${clientSecret}`;
}
