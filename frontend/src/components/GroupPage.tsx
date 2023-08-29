import NavigationBar from "./NavigationBar";
import { useContext, useEffect, useState } from "react";
import { Group, User } from "../types";
import { getGroup as fetchGroup } from "../services";
import { AuthContext } from "../AuthContext";
import { useParams } from "react-router";
import MetricsContainer from "./MetricsContainer";

function GroupPage() {
    const authContext = useContext(AuthContext);
    const params = useParams();
    const [group, setGroup] = useState<Group | null>(null);
    const [loaded, setLoaded] = useState(false);

    const getGroup = async (token: string, id: number): Promise<Group> => {
        return await fetchGroup(token, id);
    }

    useEffect(() => {
        if (!authContext.isLoading) {
            try {
                if (params?.id === undefined) {
                    throw new Error('Group id undefined');
                } else {
                    const id = parseInt(params?.id);
                    getGroup(authContext?.token, id)
                        .then((group) => {
                            setGroup(group);
                            setLoaded(true);
                        })
                        .catch((e) => {
                            console.log('hello');
                        })
                }
            } catch (e) {
                console.log('Error');
            }
        }
    }, [authContext?.isLoading]);

    return (
        loaded ? (
            <>
                <NavigationBar />
                <div className='content-wrapper'>
                    <h1 className='header'>{group?.name}</h1>
                    <div className='metrics-wrapper'>
                        <MetricsContainer title='Total Spending' value='$100' />
                        <MetricsContainer title='Average Spend Per Person' value='$10' />
                        <MetricsContainer title='Top Spender' value='Aidan Niceberg' />
                    </div>
                </div>
            </>
        ) : (
            <h1>Page not found</h1>
        )
    )
}

export default GroupPage;
