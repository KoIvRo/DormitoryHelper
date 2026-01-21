import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    // Сначала очищаем localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    
    // Используем setTimeout для безопасного перехода
    setTimeout(() => {
      navigate('/login', { replace: true });
    }, 0);
  };

  return (
    <nav>
      <div className="nav-content">
        <h2>DormitoryHelper</h2>
        <ul className="nav-links">
          {token ? (
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