export type LoginRequest = {
    email: string;
    password: string;
};

export type LoginResponse = {
    access_token: string;
    refresh_token: string;
    expires_in: number;
};

export type RegisterRequest = {
    email: string;
    password: string;
}

export type RegisterResponse = {
    id: string;
    email: string;
    created_at: string;
}