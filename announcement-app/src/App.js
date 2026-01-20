import React, { useEffect, useState } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import AnnouncementList from './components/AnnouncementList';
import AnnouncementForm from './components/AnnouncementForm';
import UserProfile from './components/UserProfile';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  const location = useLocation();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Проверяем наличие токена при каждом изменении location
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, [location]);

  return (
    <div className="App">
      <Navbar />
      <Routes>
        {/* Публичные маршруты */}
        <Route path="/login" element={
          isAuthenticated ? <Navigate to="/" replace /> : <Login />
        } />
        <Route path="/register" element={
          isAuthenticated ? <Navigate to="/" replace /> : <Register />
        } />
        
        {/* Приватные маршруты */}
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
        
        {/* Перенаправление для несуществующих маршрутов */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;