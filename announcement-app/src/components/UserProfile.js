import React, { useState, useEffect } from 'react';
import { userAPI, announcementAPI } from '../services/api';

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await userAPI.getMe();
      setUserData(response.data);
      // Сохраняем ID пользователя для проверок
      localStorage.setItem('userId', response.data.id);
      setError('');
    } catch (err) {
      setError('Ошибка загрузки профиля');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAnnouncement = async (id) => {
    if (window.confirm('Вы уверены, что хотите удалить это объявление?')) {
      try {
        await announcementAPI.deleteAnnouncement(id);
        // Обновляем данные после удаления
        fetchUserData();
      } catch (err) {
        alert('Не удалось удалить объявление');
        console.error(err);
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU');
  };

  if (loading) return <div className="container">Загрузка профиля...</div>;
  if (error) return <div className="container error">{error}</div>;
  if (!userData) return <div className="container">Нет данных</div>;

  return (
    <div className="container">
      <h1>Профиль пользователя</h1>
      
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2>Информация</h2>
        <p><strong>Имя:</strong> {userData.name}</p>
        <p><strong>Email:</strong> {userData.email}</p>
      </div>
      
      <h2>Мои объявления ({userData.announcement?.length || 0})</h2>
      
      {userData.announcement && userData.announcement.length > 0 ? (
        <div className="grid">
          {userData.announcement.map(announcement => (
            <div key={announcement.id} className="card">
              <h3>{announcement.name}</h3>
              <p><strong>Ссылка:</strong> {announcement.link}</p>
              <p><strong>Категория:</strong> {announcement.category}</p>
              <p><strong>Начало:</strong> {formatDate(announcement.date)}</p>
              <p><strong>Конец:</strong> {formatDate(announcement.end_date)}</p>
              
              <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
                <button 
                  className="btn btn-secondary"
                  onClick={() => {
                    if (announcement.link.startsWith('http')) {
                      window.open(announcement.link, '_blank');
                    } else if (announcement.link.startsWith('+')) {
                      window.location.href = `tel:${announcement.link}`;
                    }
                  }}
                >
                  {announcement.link.startsWith('+') ? 'Позвонить' : 'Перейти по ссылке'}
                </button>
                
                <button 
                  className="btn btn-danger"
                  onClick={() => handleDeleteAnnouncement(announcement.id)}
                >
                  Удалить
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card">
          <p>У вас пока нет объявлений</p>
        </div>
      )}
    </div>
  );
};

export default UserProfile;