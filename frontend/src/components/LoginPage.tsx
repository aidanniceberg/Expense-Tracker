import './AccountEntry.css';
import { FormEvent } from 'react';
import { login } from '../services';

function LoginPage() {
    const authenticate = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data: FormData = new FormData(event.currentTarget);
        const status: number = await login(data);

        if (status === 200) {
            window.location.href = 'http://localhost:3000/home';
        }
    }

    return (
        <div className='auth-wrapper'>
            <h1 className='auth-title'>Login</h1>
            <form onSubmit={authenticate} className='input-wrapper'>
                <label className='auth-label'>Username</label>
                <input className='auth-text-input' type='text' name='username' />
                <label className='auth-label'>Password</label>
                <input className='auth-text-input' type='password' name='password' />
                <input type='submit' className='submit' value='Log In'></input>
            </form>
        </div>
    );
}

export default LoginPage;
