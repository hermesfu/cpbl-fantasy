import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Matchup = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [updatePage, setUpdatePage] = useState(false);

    const [columnsB, setColumnsB] = useState([]);
    const [columnsP, setColumnsP] = useState([]);

    const [batterData1, setBatterData1] = useState(null);
    const [batterData2, setBatterData2] = useState(null);
    const [pitcherData1, setPitcherData1] = useState(null);
    const [pitcherData2, setPitcherData2] = useState(null);
    const [name1, setName1] = useState("");
    const [name2, setName2] = useState("");

    const [total1, setTotal1] = useState(null);
    const [total2, setTotal2] = useState(null);
    const [score1, setScore1] = useState(0);
    const [score2, setScore2] = useState(0);

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    const matchup = queryParams.get('id');

    useEffect(() => {
        const fetchData = async () => {
            try {
                let response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/matchup?matchup=${matchup}&value=league`,
                    {method: 'GET'}
                );
                let result = await response.json();
                const league = result.value;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/matchup?matchup=${matchup}&value=team1`,
                    {method: 'GET'}
                );
                result = await response.json();
                const team1 = result.value;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/matchup?matchup=${matchup}&value=team2`,
                    {method: 'GET'}
                );
                result = await response.json();
                const team2 = result.value;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/team?team=${team1}&value=name`,
                    {method: 'GET'}
                );
                result = await response.json();
                setName1(result.value);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/team?team=${team2}&value=name`,
                    {method: 'GET'}
                );
                result = await response.json();
                setName2(result.value);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_b`,
                    {method: 'GET'}
                );
                result = await response.json();
                let allColumn = ['name', 'team'].concat(result.value);
                const columns_b = allColumn;
                allColumn = ['position'].concat(allColumn);
                setColumnsB(allColumn);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/rosters?team=${team1}&isBatter=true`,
                    {method: 'GET'}
                );
                result = await response.json();
                let batters1 = result.players;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/search/players`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"players": batters1,
                                              "categories": columns_b,
                                              "isBatter": true})
                    }
                );
                result = await response.json();
                setBatterData1(result.data);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/calculate/total`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"data": result.data})
                    }
                );
                result = await response.json();
                let totalStat1 = result;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/rosters?team=${team2}&isBatter=true`,
                    {method: 'GET'}
                );
                result = await response.json();
                let batters2 = result.players;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/search/players`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"players": batters2,
                                              "categories": columns_b,
                                              "isBatter": true})
                    }
                );
                result = await response.json();
                setBatterData2(result.data);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/calculate/total`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"data": result.data})
                    }
                );
                result = await response.json();
                let totalStat2 = result;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_p`,
                    {method: 'GET'}
                );
                result = await response.json();
                allColumn = ['name', 'team'].concat(result.value);
                setColumnsP(allColumn);
                const columns_p = allColumn;
                allColumn = ['position'].concat(allColumn);
                setColumnsP(allColumn);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/rosters?team=${team1}&isBatter=false`,
                    {method: 'GET'}
                );
                result = await response.json();
                let pitchers1 = result.players;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/search/players`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"players": pitchers1,
                                              "categories": columns_p,
                                              "isBatter": false})
                    }
                );
                result = await response.json();
                setPitcherData1(result.data);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/calculate/total`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"data": result.data})
                    }
                );
                result = await response.json();
                totalStat1 = {...totalStat1, ...result};
                setTotal1(totalStat1);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/rosters?team=${team2}&isBatter=false`,
                    {method: 'GET'}
                );
                result = await response.json();
                let pitchers2 = result.players;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/search/players`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"players": pitchers2,
                                              "categories": columns_p,
                                              "isBatter": false})
                    }
                );
                result = await response.json();
                setPitcherData2(result.data);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/calculate/total`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"data": result.data})
                    }
                );
                result = await response.json();
                totalStat2 = {...totalStat2, ...result};
                setTotal2(totalStat2);  
                
                let tmpscore1 = 0
                let tmpscore2 = 0

                for (const key in totalStat1) {
                    if (key === "ERA" || key === "WHIP") {
                        if (totalStat1[key] < totalStat2[key]) tmpscore1++;
                        else tmpscore2++;
                    } else {
                        if (totalStat1[key] > totalStat2[key]) tmpscore1++;
                        else tmpscore2++;
                    }
                }
                setScore1(tmpscore1);
                setScore2(tmpscore2);
            }  catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [updatePage])

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <div>
                <h1>{name1}</h1>
                <h1>{score1}</h1>
                <h1>{name2}</h1>
                <h1>{score2}</h1>
            </div>
            <div>
                <table>
                    <thead>
                        <tr>
                            {columnsB.map(col => {
                                if (col !== "position" && col !== "name" && col !== "team") {
                                    return (<th key={col}>{col}</th>);
                                }
                            })}
                            {columnsP.map(col => {
                                if (col !== "position" && col !== "name" && col !== "team") {
                                    return (<th key={col}>{col}</th>);
                                }
                            })}
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            {columnsB.map(col => {
                                if (col !== "position" && col !== "name" && col !== "team") {
                                    return (<td key={col}>{total1[col]}</td>);
                                }
                            })}
                            {columnsP.map(col => {
                                    if (col !== "position" && col !== "name" && col !== "team") {
                                        return (<td key={col}>{total1[col]}</td>);
                                    }
                            })}
                        </tr>
                        <tr>
                            {columnsB.map(col => {
                                if (col !== "position" && col !== "name" && col !== "team") {
                                    return (<td key={col}>{total2[col]}</td>);
                                }
                            })}
                            {columnsP.map(col => {
                                    if (col !== "position" && col !== "name" && col !== "team") {
                                        return (<td key={col}>{total2[col]}</td>);
                                    }
                            })}
                        </tr>
                    </tbody>
                </table>
            </div>

            <div>
                <table>
                    <thead>
                        <tr>
                            {columnsB.map(col => {
                                return (<th key={col}>{col}</th>);
                            })}
                        </tr>
                    </thead>

                    <tbody>
                        {batterData1.map((player) => (
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
                            {columnsP.map(col => {
                                return (<th key={col}>{col}</th>);
                            })}
                        </tr>
                    </thead>

                    <tbody>
                        {pitcherData1.map((player) => (
                            <tr key={player}>
                                {columnsP.map((col) => {
                                    return (<td key={col}>{player[col]}</td>)
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            
            <div>
                <table>
                    <thead>
                        <tr>
                            {columnsB.map(col => {
                                return (<th key={col}>{col}</th>);
                            })}
                        </tr>
                    </thead>

                    <tbody>
                        {batterData2.map((player) => (
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
                            {columnsP.map(col => {
                                return (<th key={col}>{col}</th>);
                            })}
                        </tr>
                    </thead>

                    <tbody>
                        {pitcherData2.map((player) => (
                            <tr key={player}>
                                {columnsP.map((col) => {
                                    return (<td key={col}>{player[col]}</td>)
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
        
    );
}

export default Matchup;