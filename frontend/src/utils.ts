import { ACCESS_TOKEN_KEY } from "./constants";


export const getCookies = (): { [key: string]: string } => {
    const cookiesArray = document.cookie.split(';');
    let cookies: { [key: string]: string } = {};
    cookiesArray.forEach((cookie) => {
        const pair = cookie.split('=');
        cookies[pair[0]] = pair[1];
    });
    return cookies;
}

export const getToken = (): string | null => {
    const cookies = getCookies();
    if (ACCESS_TOKEN_KEY in cookies) {
        return cookies[ACCESS_TOKEN_KEY];
    } else {
        return null;
    }
}
