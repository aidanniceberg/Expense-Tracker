import { createContext, useState, ReactNode, useEffect } from 'react';
import { login as generateToken, getCurrentUser } from './services';
import { User } from './types';
import { getToken } from './utils';

interface AuthContextProps {
    children: ReactNode
}

type AuthContextType = {
    user?: User;
    token: string;
    isAuthenticated: boolean;
    login: (username: string, password: string) => void;
}

export const AuthContext = createContext<AuthContextType>({} as AuthContextType);

function AuthContextProvider({ children }: AuthContextProps) {
    const [user, setUser] = useState<User>();
    const [token, setToken] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const currentToken = getToken();
        if (currentToken !== null) {
            setToken(currentToken);
            getCurrentUser(currentToken)
                .then((user) => {
                    setUser(user);
                    setIsAuthenticated(true);
                });
        }
    }, []);

    const login = async (username: string, password: string) => {
        await generateToken(username, password)
            .then((currentToken) => {
                setToken(currentToken.access_token)
                getCurrentUser(currentToken.access_token)
                    .then((user) => {
                        setUser(user)
                    })
                setIsAuthenticated(true);
            });
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                isAuthenticated,
                login
            }}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContextProvider;
