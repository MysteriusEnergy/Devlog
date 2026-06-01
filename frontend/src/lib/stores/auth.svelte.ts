class AuthStore {
    accessToken = $state<string | null>(null);
    refreshToken = $state<string | null>(null);

    get isAuthenticated() {
        return Boolean(this.accessToken);
    }

    load() {
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    setTokens(accessToken: string, refreshToken: string) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);

        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
    }

    clear() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        this.accessToken = null;
        this.refreshToken = null;
    }
}

export const auth = new AuthStore();