import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [vPassword, setvPassword] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault(); // prevent default form behavior

    if (password != vPassword) {
      alert("Please make sure the passwords are the same")
    } else {
      const data = { username, password };

      try {
        const response = await fetch(`${import.meta.env.VITE_SERVER_URL}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        const result = await response.json();
        if (response.ok && result.success) {
          navigate('/success');
        } else {
          alert('Username have already been used');
        }
      } catch (error) {
        console.error('Login error:', error);
      }
    }
  };

  return (
    <div>
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <label>Username:</label>
        <input
          type="text"
          name="username"
          placeholder="Username"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br />
        <label>Password:</label>
        <input
          type="password"
          name="password"
          placeholder="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <label>Verify Password:</label>
        <input
          type="password"
          name="vPassword"
          placeholder="Verify Password"
          required
          value={vPassword}
          onChange={(e) => setvPassword(e.target.value)}
        />
        <br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Login;