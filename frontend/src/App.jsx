import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'

import './App.css'
import Login from './pages/Login'
import Success from './pages/Success'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/success" element={<Success />} />
      </Routes>
    </Router>
  )
}

export default App
