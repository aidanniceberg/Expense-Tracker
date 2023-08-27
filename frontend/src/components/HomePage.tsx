import { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../AuthContext';
import NavigationBar from './NavigationBar';
import { getGroups as fetchGroups } from '../services';
import { Group } from '../types';

type GroupRow = {
    group: Group;
    hidden: boolean;
}

function HomePage() {
    const authContext = useContext(AuthContext);
    const [groups, setGroups] = useState<Array<GroupRow> | null>(null);

    const getGroups = async (token: string): Promise<Array<Group>> => {
        return await fetchGroups(token);
    }

    const sortBy = (func: (row1: GroupRow, row2: GroupRow) => number): void => {
        if (groups !== null) {
            const sorted = [...groups].sort(func);
            setGroups(sorted);
        }
    }

    const sortByOwner = (): void => {
        sortBy((row1: GroupRow, row2: GroupRow) => {
            const owner1 = `${row1.group.author.first_name} ${row1.group.author.last_name}`
            const owner2 = `${row2.group.author.first_name} ${row2.group.author.last_name}`
            if (owner1 < owner2) {
                return -1;
            } else if (owner1 > owner2) {
                return 1;
            } else {
                return 0;
            }
        });
    }

    const sortByName = (): void => {
        sortBy((row1: GroupRow, row2: GroupRow) => {
            if (row1.group.name.toLowerCase() < row2.group.name.toLowerCase()) {
                return -1;
            } else if (row1.group.name.toLowerCase() > row2.group.name.toLowerCase()) {
                return 1;
            } else {
                return 0;
            }
        });
    }

    const sortByDate = (): void => {
        sortBy((row1: GroupRow, row2: GroupRow) => {
            const date1 = new Date(row1.group.created_date);
            const date2 = new Date(row2.group.created_date);
            if (date1 < date2) {
                return -1;
            } else if (date1 > date2) {
                return 1;
            } else {
                return 0;
            }
        });
    }

    const filterByName = (searchTerm: string): void => {
        if (groups !== null && searchTerm !== '') {
            const filtered = [...groups].map((row) => {
                const isMatch = row.group.name.toLowerCase().includes(searchTerm.toLowerCase())
                return { group: row.group, hidden: !isMatch };
            });
            setGroups(filtered);
        } else if (groups !== null && searchTerm === '') {
            const rows = [...groups].map((row) => {
                return { group: row.group, hidden: false };
            });
            setGroups(rows);
        }
    }

    useEffect(() => {
        if (!authContext.isLoading) {
            getGroups(authContext?.token)
                .then((response) => {
                    const rows = response.map((group) => {
                        return { group: group, hidden: false };
                    })
                    setGroups(rows);
                });
        }
    }, [authContext.isLoading]);

    return (
        <>
            <NavigationBar />
            <div className='content-wrapper'>
                <h1 className='header'>My Groups</h1>
                <input type='text' className='searchBar' placeholder='Filter by name' onChange={(e) => { filterByName(e.target.value) }} />
                <table className='content-table'>
                    <thead>
                        <tr>
                            <th onClick={sortByName}>Name</th>
                            <th onClick={sortByOwner}>Owner</th>
                            <th onClick={sortByDate}>Created Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            groups && groups.map((row) => {
                                if (!row.hidden) {
                                    const link = `http://localhost:3000/groups/${row.group.id}`
                                    const date = new Date(row.group.created_date);
                                    return (
                                        <tr key={row.group.id} onClick={() => { window.location.href = link }}>
                                            <td>{row.group.name}</td>
                                            <td>{row.group.author.first_name + ' ' + row.group.author.last_name}</td>
                                            <td>{`${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`}</td>
                                        </tr>
                                    )
                                }
                            })
                        }
                    </tbody>
                </table>
                <a href='/groups/create' className='btn'>+ Create New</a>
            </div>
        </>
    )
}

export default HomePage;
