import NavigationBar from "./NavigationBar";
import Select from "react-select";
import { useContext, useEffect, useState } from "react";
import { User } from "../types";
import { getUsers as fetchUsers, createGroup } from "../services";
import { AuthContext } from "../AuthContext";

type SelectOption = {
    value: string;
    label: string;
}

function CreateGroupPage() {
    const authContext = useContext(AuthContext);
    const [name, setName] = useState('');
    const [members, setMembers] = useState<Array<number>>([]);
    const [memberOptions, setMemberOptions] = useState<Array<SelectOption>>([]);
    const [errorMessage, setErrorMessage] = useState('Error creating group. Please try again.');
    const [displayErrorMessage, setDisplayErrorMessage] = useState(false);

    const getUsers = async (token: string): Promise<Array<User>> => {
        return await fetchUsers(token);
    }

    const handleSubmit = async () => {
        setDisplayErrorMessage(false);
        try {
            if (name === '') {
                throw new Error('Group name must be provided');
            }
            await createGroup(authContext?.token, name, members);
            window.location.href = 'http://localhost:3000/home';
        } catch (e) {
            setDisplayErrorMessage(true);
        }
    }

    useEffect(() => {
        if (!authContext.isLoading) {
            getUsers(authContext?.token)
                .then((users) => {
                    const options = users.map((user) => {
                        return { value: user.id.toString(), label: `${user.first_name} ${user.last_name}` }
                    });
                    setMemberOptions(options);
                });
        }
    }, [authContext?.isLoading])

    return (
        <>
            <NavigationBar />
            <div className='content-wrapper'>
                <h1 className='header'>Create Group</h1>
                <label className='form-label'>Name</label>
                <input type='text' className='form-input-text' onChange={(e) => { setName(e.target.value) }} />
                <label className='form-label'>Add Members</label>
                <div className='form-input-wrapper'>
                    <Select
                        options={memberOptions}
                        isMulti
                        styles={{
                            control: (baseStyles, state) => ({
                                ...baseStyles,
                                borderColor: '#2d3a3a',
                                width: '320px',
                                boxSizing: 'border-box',
                                color: '#2d3a3a',
                            }),
                        }}
                        onChange={
                            (e) => {
                                setMembers(e.map((member) => parseInt(member.value)));
                            }
                        }
                    />
                </div>
                <div className='btn btn-create' onClick={handleSubmit}>Create</div>
                {displayErrorMessage && <p className='msg-error'>{errorMessage}</p>}
            </div>
        </>
    )
}

export default CreateGroupPage;
