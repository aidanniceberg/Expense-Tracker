export type User = {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
}

export type AuthToken = {
    access_token: string;
    token_type: string;
}

export type Group = {
    id: number;
    name: string;
    author: User;
    created_date: string;
}
