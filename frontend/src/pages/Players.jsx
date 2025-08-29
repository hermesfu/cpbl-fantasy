import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Players = () => {
  const [columns, setColumns] = useState([]);
  const [playerData, setPlayerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [keyword, setKeyword] = useState('');
  const [totalPage, setTotalPage] = useState(0);
  const [updatePage, setUpdatePage] = useState(false);
  const [leagueID, setLeagueID] = useState("");
  
  const navigate = useNavigate();

  //prcocess query string with queryParams
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const teamID = queryParams.get('id') || '';
  const name = queryParams.get('N') || '';
  const position = queryParams.get('P') || 'P';
  const sortby = queryParams.get('C') || 'name';
  const order = queryParams.get('S') || 'A';
  const teamAbbr = queryParams.get('T') || '';
  const page = Number(queryParams.get('page') || 1);

  let teamName = "";
  let isBatter = false;

  //set value for selection based on parameter
  let selectedPosition = 'Pitchers';
  if (position === 'P') selectedPosition = 'Pitchers';
  else if (position === 'Util') selectedPosition = 'Batters';
  else selectedPosition = position;

  let selectedTeam = 'All';
  switch (teamAbbr) {
    case 'F': selectedTeam = 'Fubon Guardian'; break;
    case 'U': selectedTeam = 'Uni-President 7-ELEVEn Lions'; break;
    case 'T': selectedTeam = 'TSG Hawks'; break;
    case 'R': selectedTeam = 'Rakuten Monkeys'; break;
    case 'W': selectedTeam = 'Wei Chuan Dragons'; break;
    case 'C': selectedTeam = 'CTBC Brothers'; break;
    default: selectedTeam = 'All';
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/team?team=${teamID}&value=league`,
                    {method: 'GET'}
                );
        let result = await response.json();
        setLeagueID(result.value);
        const league = result.value;

        //translate team in parameter string to full name
        switch(teamAbbr) {
          case 'F':
            teamName = "富邦悍將";
            break;
          case 'U':
            teamName = "7-ELEVEn";
            break;
          case 'T':
            teamName = "台鋼雄鷹";
            break;
          case 'R':
            teamName = "樂天桃猿";
            break;
          case 'W':
            teamName = "味全龍";
            break;
          case 'C':
            teamName = "中信兄弟";
            break;
          default:
            teamName = "";
        }

        isBatter = !position.includes('P');

        //request categories by league id
        if (isBatter) {
          response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_b`,
                    {method: 'GET'}
                  );
        } else {
          response = await fetch(
                    `${import.meta.env.VITE_SERVER_URL}/get/league?league=${league}&value=categories_p`,
                    {method: 'GET'}
                  );
        }

        result = await response.json();
        let allColumn = ['name', 'team', 'positions'].concat(result.value);
        setColumns(allColumn);

        //request player data
        const requestData = {
          "iaBatter": isBatter,
          "categories": allColumn,
          "positions": [position],
          "name": name,
          "team": teamName,
          "sortby": sortby,
          "ascending": (order === 'A'),
          "page": page,
          "league": league
        }

        response = await fetch(`${import.meta.env.VITE_SERVER_URL}/get/players`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        });
        result = await response.json();
        setPlayerData(result.data);
        setTotalPage(result.totalPage);

        allColumn = ['_id', 'status'].concat(allColumn);
        setColumns(allColumn);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [leagueID, name, position, sortby, order, teamAbbr, page, updatePage]);

  //submission button in player search
  const handleSubmit = (e) => {
    e.preventDefault();
    const searchParams = new URLSearchParams(location.search);
    searchParams.set('N', keyword);
    searchParams.set('page', '1');
    navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true });
  }

  //position selection
  const handlePositionSelect = (e) => {
    const positionSelect = e.target.value;
    const searchParams = new URLSearchParams(location.search);
    if (positionSelect === 'Pitchers') searchParams.set('P', 'P');
    else if (positionSelect === 'Batters') searchParams.set('P', 'Util');
    else searchParams.set('P', positionSelect);
    searchParams.set('C', 'name');
    searchParams.set('S', 'A');
    searchParams.set('page', '1');
    navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true });
  }

  //team selection
  const handleTeamSelect = (e) => {
    const teamSelect = e.target.value[0];
    const searchParams = new URLSearchParams(location.search);
    searchParams.set('T', teamSelect);
    searchParams.set('C', 'name');
    searchParams.set('S', 'A');
    searchParams.set('page', '1');
    navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true });
  }

  //function for add player button
  const addPlayer = async(playerID, positions) => {
    const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/add/player`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"team": teamID, "player": playerID, "positions": positions}),
    });

    const result = await response.json();
    if (result.success) alert("Add paleyr successfully!");
    else alert("The positions for the selected player in your team is full");

    setUpdatePage(!updatePage); 
  }

  //function for drop player button
  const dropPlayer = async(playerID, positions) => {
    let deletePosition = null;
    positions = positions.concat("BEN");

    for (const position of positions) {
      let response = await fetch(`${import.meta.env.VITE_SERVER_URL}/get/roster?team=${teamID}&position=${position}`,
                                  {method: 'GET'});
      let result = await response.json();
      if (result.players.includes(playerID)) {
        deletePosition = position;
        break;
      }
    }

    await fetch(`${import.meta.env.VITE_SERVER_URL}/drop/player`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"team": teamID, "player": playerID, "position": deletePosition}),
    });

    alert("Drop paleyr successfully!");
    setUpdatePage(!updatePage);
  }

  //function for drop player button
  const tradePlayer = async(playerID) => {
    alert("This feature have not been implemented yet");
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Player</h1>
      <form onSubmit={handleSubmit}>
        <label>Name:</label>
        <input value={keyword} onChange={(e) => setKeyword(e.target.value)}/>
        <button type="submit">Search</button>
      </form>

      <div class="selection">
        <label>Position:</label>
        <select onChange={handlePositionSelect} value={selectedPosition}>
            <option>Pitchers</option>
            <option>Batters</option>
            <option>SP</option>
            <option>RP</option>
            <option>IF</option>
            <option>OF</option>
            <option>C</option>
            <option>1B</option>
            <option>2B</option>
            <option>3B</option>
            <option>SS</option>
            <option>LF</option>
            <option>CF</option>
            <option>RF</option>
          </select>

          <label>Team:</label>
          <select onChange={handleTeamSelect} value={selectedTeam}>
              <option>All</option>
              <option>Fubon Guardian</option>
              <option>Uni-President 7-ELEVEn Lions</option>
              <option>TSG Hawks</option>
              <option>Rakuten Monkeys</option>
              <option>Wei Chuan Dragons</option>
              <option>CTBC Brothers</option>
            </select>  
      </div>

      <table>
        <thead>
          <tr>
            {columns.map(col => {
              if (col === "_id") return (<th></th>);
              else if (col !== "status") {
                const sValue = (sortby === col && order === 'D') ? 'A' : 'D';
                const searchParams = new URLSearchParams(location.search);
                searchParams.set('C', col);
                searchParams.set('S', sValue);
                return (
                  <th key={col}><a href={`${location.pathname}?${searchParams.toString()}`}>{col}</a></th>
                )
              }
            })}
          </tr>
        </thead>
        <tbody>
          {playerData.map((player) => (
            <tr key={player}>
              {columns.map((col) => {
                  if (col === "_id") {
                    if (player['status'] === null) {
                      return (<td><button type="button" onClick={() => addPlayer(player[col].toString(), player["positions"])}>Add</button></td>);
                    } else if (player['status'] == teamID) {
                      return (<td><button type="button" onClick={() => dropPlayer(player[col].toString(), player["positions"])}>Drop</button></td>);
                    } else {
                      return (<td><button type="button" onClick={() => tradePlayer(player[col].toString())}>Trade</button></td>);
                    }
                  }
                  else if (col === "positions") return (<td key={col}>{player[col].toString()}</td>)
                  else if (col !== "status") return (<td key={col}>{player[col]}</td>)
              })}
            </tr>
          ))}
        </tbody>
      </table>
          
      <div>
        { //previous button
          page > 1 ? (
            (() => {
              const searchParams = new URLSearchParams(location.search);
              searchParams.set('page', page - 1);
              return (
                <span><a href={`${location.pathname}?${searchParams.toString()}`}>prev</a>&emsp;</span>
              );
            })()
          ) : (
            <span>prev&emsp;</span>
        )}

        { //page number
          Array.from({ length: totalPage }, (_, i) => {
          const searchParams = new URLSearchParams(location.search);
          searchParams.set('page', i + 1);
          if (i + 1 != page) {
            return (
              <span key={i}><a href={`${location.pathname}?${searchParams.toString()}`}>{i + 1}</a>&emsp;</span>
            )
          } else {
            //don't include link if it's current page
            return (
              <span key={i}>{i + 1}&emsp;</span>
            )
          }
        })}
        
        { //next button
          page < totalPage ? (
            (() => {
              const searchParams = new URLSearchParams(location.search);
              searchParams.set('page', page + 1);
              return (
                <span><a href={`${location.pathname}?${searchParams.toString()}`}>next</a>&emsp;</span>
              );
            })()
          ) : (
            <span>next&emsp;</span>
        )}
      </div>
    </div>
  );
};

export default Players;