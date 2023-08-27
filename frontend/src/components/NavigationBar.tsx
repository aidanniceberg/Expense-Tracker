import { useContext } from 'react';
import { AuthContext } from '../AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faReceipt } from '@fortawesome/free-solid-svg-icons';

function NavigationBar() {
    const authContext = useContext(AuthContext);

    return (
        <div id='nav'>
            <div id='nav-wrapper'>
                <a href='/home' id='logo-wrapper'>
                    <FontAwesomeIcon id='logo' icon={faReceipt} rotation={90} style={{ color: "#2d3a3a" }} />
                </a>
                <div>
                    <h3 className='nav-text'>Hi, {authContext.user?.first_name}</h3>
                </div>
            </div>
        </div>
    )
}

export default NavigationBar;
