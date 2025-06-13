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
    const [updatePage, setUpdatePage] = useState(false);
    const [selectedPlayer, setSelectedPlayer] = useState(null);
    const [selectedPosition, setSelectedPosition] = useState(null);
    const [selectedPositions, setSelectedPositions] = useState(null);

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
                const columns_b = allColumn;
                allColumn = ['position'].concat(allColumn);
                setColumnsB(allColumn);

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

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_p`,
                    {method: 'GET'}
                );
                result = await response.json();
                allColumn = ['name', 'team', 'positions'].concat(result.value);
                setColumnsP(allColumn);
                const columns_p = allColumn;
                allColumn = ['position'].concat(allColumn);
                setColumnsP(allColumn);

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/rosters?team=${team}&isBatter=false`,
                    {method: 'GET'}
                );
                result = await response.json();
                let pitchers = result.players;

                response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/search/players`,
                    {method: 'Post',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({"players": pitchers,
                                              "categories": columns_p,
                                              "isBatter": false})
                    }
                );
                result = await response.json();
                setPitcherData(result.data);
            }  catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [updatePage, selectedPlayer])

    //function for drop player button
    const dropPlayer = async(playerID, position) => {
        await fetch(`${import.meta.env.VITE_SERVER_URL}/drop/player`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({"team": team, "player": playerID, "position": position}),
        });

        alert("Drop paleyr successfully!");
        setUpdatePage(!updatePage);
    }

    //function for selecting the first player to swap
    const selectPlayer = (player, position, positions) => {
        setSelectedPlayer(player);
        setSelectedPosition(position);
        setSelectedPositions(positions);
    }

    //function for unselecting the player to swap
    const unselectPlayer = () => {
        setSelectedPlayer(null);
        setSelectedPosition(null);
        setSelectedPositions(null);
    }

    //to be implemented
    const swapPlayer = async(player, position, positions) => {
        const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/swap/player`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({"team": team, "player1": selectedPlayer, "position1": selectedPosition,
                                  "player2": player, "position2": position, "positions2": positions
            }),
        });

        const result = await response.json;
        if (result.success == "False") alert("error");

        setUpdatePage(!updatePage);

        setSelectedPlayer(null);
        setSelectedPosition(null);
        setSelectedPositions(null);
    }

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h1>{name}</h1>

            <table>
                <thead>
                    <tr>
                        <th></th>
                        {columnsB.map(col => {
                            if (col === "position") return (<th></th>);
                            else return (<th key={col}>{col}</th>);
                        })}
                    </tr>
                </thead>

                <tbody>
                    {batterData.map((player) => (
                        <tr key={player}>
                            {player["_id"] ? 
                               (<td><button type="button" onClick={() => dropPlayer(player["_id"].toString(), player["position"])}>Drop</button></td>)
                             : (<td></td>)
                            } 
                            {columnsB.map((col) => {
                                if (col === "positions" && player[col]) return (<td key={col}>{player[col].toString()}</td>)
                                else if (col === "position") {
                                    if (!selectedPlayer) return (<td><button type="button" onClick={() => selectPlayer(player["_id"].toString(), player["position"], player["positions"])}>{player["position"]}</button></td>)
                                    else {
                                        if (player["_id"] === selectedPlayer) return (<td><button type="button" onClick={() => unselectPlayer()}>{player["position"]}</button></td>)
                                        else {
                                            if (selectedPositions.includes(player["position"])) return (<td><button type="button" onClick={() => swapPlayer(player["_id"].toString(), player["position"], player["positions"])}>{player["position"]}</button></td>)
                                            else return (<td>{player["position"]}</td>)
                                        }
                                    }
                                }
                                else return (<td key={col}>{player[col]}</td>)
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>

            <table>
                <thead>
                    <tr>
                        <th></th>
                        {columnsP.map(col => {
                            if (col === "position") return (<th></th>);
                            else return (<th key={col}>{col}</th>);
                        })}
                    </tr>
                </thead>

                <tbody>
                    {pitcherData.map((player) => (
                        <tr key={player}>
                            {player["_id"] ? 
                               (<td><button type="button" onClick={() => dropPlayer(player["_id"].toString(), player["position"])}>Drop</button></td>)
                             : (<td></td>)
                            }
                            {columnsP.map((col) => {
                                if (col === "positions" && player[col]) return (<td key={col}>{player[col].toString()}</td>)
                                else if (col === "position") {
                                    if (!selectedPlayer) return (<td><button type="button" onClick={() => selectPlayer(player["_id"].toString(), player["position"], player["positions"])}>{player["position"]}</button></td>)
                                    else {
                                        if (player["_id"] === selectedPlayer) return (<td><button type="button" onClick={() => unselectPlayer()}>{player["position"]}</button></td>)
                                        else {
                                            if (selectedPositions.includes(player["position"])) return (<td><button type="button" onClick={() => swapPlayer(player["_id"].toString(), player["position"], player["positions"])}>{player["position"]}</button></td>)
                                            else return (<td>{player["position"]}</td>)
                                        }
                                    }
                                }
                                else return (<td key={col}>{player[col]}</td>)
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Team;