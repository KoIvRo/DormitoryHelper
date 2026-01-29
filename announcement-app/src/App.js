import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import AnnouncementList from './components/AnnouncementList';
import AnnouncementForm from './components/AnnouncementForm';
import UserProfile from './components/UserProfile';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Функция для обновления состояния аутентификации
  const updateAuthStatus = () => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
  };

  useEffect(() => {
    updateAuthStatus();
    
    // Слушаем изменения в localStorage
    const handleStorageChange = () => {
      updateAuthStatus();
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return (
    <div className="App">
      <Navbar isAuthenticated={isAuthenticated} />
      <Routes>
        <Route path="/login" element={
          <Login onLogin={updateAuthStatus} />
        } />
        <Route path="/register" element={
          <Register onRegister={updateAuthStatus} />
        } />
        
        <Route path="/" element={
          <PrivateRoute>
            <AnnouncementList />
          </PrivateRoute>
        } />
        <Route path="/create" element={
          <PrivateRoute>
            <AnnouncementForm />
          </PrivateRoute>
        } />
        <Route path="/profile" element={
          <PrivateRoute>
            <UserProfile />
          </PrivateRoute>
        } />
        
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  );
}

export default App;