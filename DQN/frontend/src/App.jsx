import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ResumeUpload from './pages/ResumeUpload';
import SkillGap from './pages/SkillGap';
import LearningCatalog from './pages/LearningCatalog';
import LearningView from './pages/LearningView';
import QuizView from './pages/QuizView';
import QuizResults from './pages/QuizResults';
import Profile from './pages/Profile';
import { api, getToken, setToken, removeToken } from './api';

function ProtectedLayout({ user, onLogout }) {
  const token = getToken();
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-container">
      <Sidebar user={user} onLogout={onLogout} />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/resume" element={<ResumeUpload />} />
          <Route path="/skill-gap" element={<SkillGap />} />
          <Route path="/learning" element={<LearningCatalog />} />
          <Route path="/learning/:topicId" element={<LearningView />} />
          <Route path="/learning/:topicId/module/:moduleId" element={<LearningView />} />
          <Route path="/quiz/:topicId" element={<QuizView />} />
          <Route path="/quiz/:quizId/results" element={<QuizResults />} />
          <Route path="/profile" element={<Profile onLogout={onLogout} />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);

  const fetchProfile = async () => {
    // Check if token is passed in query string (from GitHub OAuth redirect)
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const urlToken = urlParams.get('token');
      if (urlToken) {
        setToken(urlToken);
        const newPath = window.location.pathname === '/login' ? '/' : window.location.pathname;
        window.history.replaceState({}, document.title, newPath);
      }
    } catch (e) {
      console.warn('Could not parse query params:', e);
    }

    const token = getToken();
    if (!token) {
      setCurrentUser(null);
      setCheckingAuth(false);
      return;
    }
    try {
      const data = await api.me();
      setCurrentUser(data.user);
    } catch (err) {
      console.warn('Session verification failed:', err);
      removeToken();
      setCurrentUser(null);
    } finally {
      setCheckingAuth(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  if (checkingAuth) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-main)' }}>
        <div style={{ color: '#818cf8', fontSize: '1rem', fontWeight: '600' }}>Starting SkillPath AI...</div>
      </div>
    );
  }

  return (
    <Routes>
      <Route 
        path="/login" 
        element={currentUser ? <Navigate to="/dashboard" replace /> : <Login onAuthSuccess={fetchProfile} />} 
      />
      <Route 
        path="/register" 
        element={currentUser ? <Navigate to="/dashboard" replace /> : <Register onAuthSuccess={fetchProfile} />} 
      />
      <Route 
        path="/*" 
        element={<ProtectedLayout user={currentUser} onLogout={() => { removeToken(); setCurrentUser(null); }} />} 
      />
    </Routes>
  );
}
