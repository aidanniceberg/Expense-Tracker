import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import LoginPage from './LoginPage';
import HomePage from './HomePage';
import AuthContextProvider from '../AuthContext';
import CreateGroupPage from './CreateGroupPage';
import GroupPage from './GroupPage';

function Router() {
    return (
        <AuthContextProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Navigate to='/login' />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/home" element={<HomePage />} />
                    <Route path="/groups/:id" element={<GroupPage />} />
                    <Route path="/groups/create" element={<CreateGroupPage />} />
                    <Route path="*" element={<h1>Page Not Found</h1>} />
                </Routes>
            </BrowserRouter>
        </AuthContextProvider>
    );
}

export default Router;
