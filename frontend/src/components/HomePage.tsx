import { useContext } from 'react';
import { AuthContext } from '../AuthContext';

function HomePage() {
    const authContext = useContext(AuthContext);

    return <h1>Hi, {authContext.user?.username}</h1>
}

export default HomePage;
