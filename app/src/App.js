import React from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import IntegratedPlatform from './IntegratedPlatform';
import NewPlatformTest from './NewPlatformTest';
import GitHubAnalysis from './GitHubAnalysis';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <nav className="navbar">
          <div className="header-container">
            <h1>OSS-UAgent: An Agent-base Usability Evaluation System</h1>
          </div>
          <div className="nav-links">
            {/* <NavLink to="/" className="nav-link" end>Integrated Platform</NavLink> */}
            <NavLink to="/new-test" className="nav-link">Evaluation</NavLink>
          </div>
        </nav>

        {/* Route Configuration */}
        <Routes>
          <Route path="/" element={<IntegratedPlatform />} />
          <Route path="/new-test" element={<GitHubAnalysis />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
