import { useEffect, useState } from 'react';
import { getCurrentUser } from '../services';
import { User } from '../types';

function HomePage() {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        (async () => {
            const currentUser = await getCurrentUser();
            setUser(currentUser);
        })();
    }, []);

    return <h1>Hi, {user?.username}</h1>
}

export default HomePage;
