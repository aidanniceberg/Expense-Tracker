import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import LoginPage from './LoginPage';
import HomePage from './HomePage';

function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to='/login' />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="*" element={<h1>Page Not Found</h1>} />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;
