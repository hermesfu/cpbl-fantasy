import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'

import './App.css'
import Login from './pages/Login'
import Success from './pages/Success'
import Register from './pages/Register'
import Players from './pages/Players'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/success" element={<Success />} />
        <Route path="/players" element={<Players />} />
      </Routes>
    </Router>
  )
}

export default App
