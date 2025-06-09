import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Team = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [columnsB, setColumnsB] = useState([]);
    const [columnsP, setColumnsP] = useState([]);
    const [batterData, setBatterData] = useState(null);
    const [pitcherData, setPitcherData] = useState(null);
    const [name, setName] = useState("");

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    const team = queryParams.get('T');

    useEffect(() => {
        const fetchData = async () => {
            try {
                let response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/team?team=${team}&value=league`,
                    {method: 'GET'}
                );
                let result = await response.json();
                const league = result.value;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/team?team=${team}&value=name`,
                    {method: 'GET'}
                );
                result = await response.json();
                setName(result.value);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_b`,
                    {method: 'GET'}
                );
                result = await response.json();
                let allColumn = ['name', 'team', 'positions'].concat(result.value);
                setColumnsB(allColumn);
                const columns_b = allColumn;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_p`,
                    {method: 'GET'}
                );
                result = await response.json();
                allColumn = ['name', 'team', 'positions'].concat(result.value);
                setColumnsP(allColumn);
                const columns_p = allColumn;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/rosters?team=${team}&isBatter=true`,
                    {method: 'GET'}
                );
                result = await response.json();
                let batters = result.players;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/search/players`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"players": batters,
                                              "categories": columns_b,
                                              "isBatter": true})
                    }
                );
                result = await response.json();
                setBatterData(result.data);
            }  catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [])

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h1>{name}</h1>

            <table>
                <thead>
                    <tr>
                        <th></th>
                        {columnsB.map(col => (<th key={col}>{col}</th>))}
                    </tr>
                </thead>

                <tbody>
                    {batterData.map((player) => (
                        <tr key={player}>
                            {columnsB.map((col) => {
                                return (<td key={col}>{player[col]}</td>)
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>

            <table>
                <thead>
                    <tr>
                        <th></th>
                        {columnsP.map(col => (<th key={col}>{col}</th>))}
                    </tr>
                </thead>

                <tbody>
            
                </tbody>
            </table>
        </div>
    );
}

export default Team;