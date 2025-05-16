import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'

import './App.css'
import Login from './pages/Login'
import Success from './pages/Success'
import Register from './pages/Register'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/success" element={<Success />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  )
}

export default App
