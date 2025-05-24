import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Players = () => {
  const [columns, setColumns] = useState([]);
  const [playerData, setPlayerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const leagueName = queryParams.get('L');
  const sortby = queryParams.get('C') || 'name';
  const order = queryParams.get('S') || 'A';
  const curAddress = `${import.meta.env.VITE_WEB_URL}/players/?L=${leagueName}`;

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response = await fetch(`${import.meta.env.VITE_SERVER_URL}/get/categories?${leagueName}`,
          {method: 'GET'});
        let result = await response.json();
        setColumns(result.categories);

        const requestData = {
          "batter": true,
          "categories": result.categories,
          "positions": ["C"],
          "name": "",
          "sortby": sortby,
          "ascending": (order === 'A')
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
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Player</h1>
      <table>
        <thead>
          <tr>
            {columns.map(col => {
              const sValue = (sortby === col && order === 'D') ? 'A' : 'D';
              return (
                <th key={col}><a href={`${curAddress}&C=${col}&S=${sValue}`}>{col}</a></th>
              )}
            )}
          </tr>
        </thead>
        <tbody>
          {playerData.map((player) => (
            <tr key={player}>
              {columns.map((col) => (
                <td key={col}>{player[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Players;