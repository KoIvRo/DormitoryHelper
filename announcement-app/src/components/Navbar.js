import React from 'react';
import { Link } from 'react-router-dom';
import { authAPI } from '../services/api';

const Navbar = ({ isAuthenticated }) => {
  const handleLogout = async () => {
    try {
      // Отправляем запрос на logout для добавления токена в blacklist
      await authAPI.logout();
    } catch (error) {
      console.error('Ошибка при logout:', error);
    } finally {
      // Очищаем localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('userId');
      
      // Перезагружаем страницу для сброса состояния React
      window.location.reload();
    }
  };

  return (
    <nav>
      <div className="nav-content">
        <h2>DormitoryHelper</h2>
        <ul className="nav-links">
          {isAuthenticated ? (
            <>
              <li><Link to="/">Все объявления</Link></li>
              <li><Link to="/create">Создать объявление</Link></li>
              <li><Link to="/profile">Профиль</Link></li>
              <li>
                <button 
                  onClick={handleLogout} 
                  className="btn btn-secondary"
                  style={{ padding: '0.5rem 1rem' }}
                >
                  Выйти
                </button>
              </li>
            </>
          ) : (
            <>
              <li><Link to="/login">Вход</Link></li>
              <li><Link to="/register">Регистрация</Link></li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;