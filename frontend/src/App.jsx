import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'

import './App.css'
import Test from './pages/Test'
import Login from './pages/Login'
import Success from './pages/Success'
import Register from './pages/Register'
import Players from './pages/Players'
import Team from './pages/Team'
import Matchup from './pages/Matchup'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/test" element={<Test />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/success" element={<Success />} />
        <Route path="/players" element={<Players />} />
        <Route path="/team" element={<Team />} />
        <Route path="/matchup" element={<Matchup />} />
      </Routes>
    </Router>
  )
}

export default App
