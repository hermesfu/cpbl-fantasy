import React, { useState, useEffect } from 'react';

const Players = () => {
  const [playerData, setPlayerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const requestData = {
        "batter": false,
        "categories": ["W", "L"],
        "positions": ["SP", "RP"],
        "name": "張",
        "sortby": "W",
        "ascending": false
      }

      try {
        const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/get_players`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        });
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
    </div>
  );
};

export default Players;