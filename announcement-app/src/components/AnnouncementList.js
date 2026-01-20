import React, { useState, useEffect } from 'react';
import { announcementAPI, userAPI } from '../services/api';

const AnnouncementList = () => {
  const [announcements, setAnnouncements] = useState([]);
  const [filteredAnnouncements, setFilteredAnnouncements] = useState([]);
  const [category, setCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentUserId, setCurrentUserId] = useState(null);

  // Загружаем ID текущего пользователя
  useEffect(() => {
    const loadUserData = async () => {
      try {
        const response = await userAPI.getMe();
        localStorage.setItem('userId', response.data.id);
        setCurrentUserId(response.data.id);
      } catch (err) {
        console.error('Ошибка загрузки пользователя:', err);
      }
    };

    loadUserData();
  }, []);

  // Функция для загрузки объявлений
  const fetchAnnouncements = async () => {
    try {
      const response = await announcementAPI.getAllAnnouncements();
      setAnnouncements(response.data.account || []);
      setFilteredAnnouncements(response.data.account || []);
      setError('');
    } catch (err) {
      setError('Ошибка загрузки объявлений');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Первоначальная загрузка
  useEffect(() => {
    fetchAnnouncements();
  }, []);

  // Polling каждые 3 секунды
  useEffect(() => {
    const intervalId = setInterval(fetchAnnouncements, 3000);
    
    // Очистка интервала при размонтировании компонента
    return () => clearInterval(intervalId);
  }, []);

  // Фильтрация по категории
  useEffect(() => {
    if (category === 'all') {
      setFilteredAnnouncements(announcements);
    } else {
      const filtered = announcements.filter(
        announcement => announcement.category === category
      );
      setFilteredAnnouncements(filtered);
    }
  }, [category, announcements]);

  const categories = ['all', 'transport', 'sale', 'hobby'];
  const categoryLabels = {
    'all': 'Все',
    'transport': 'Транспорт',
    'sale': 'Продажи',
    'hobby': 'Хобби'
  };

  const handleDelete = async (id) => {
    if (window.confirm('Вы уверены, что хотите удалить это объявление?')) {
      try {
        await announcementAPI.deleteAnnouncement(id);
        // После удаления обновляем список
        fetchAnnouncements();
      } catch (err) {
        if (err.response?.status === 401) {
          setError('Вы не можете удалить это объявление');
        } else {
          setError('Не удалось удалить объявление');
        }
        console.error('Ошибка удаления:', err);
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU');
  };

  if (loading) return <div className="container">Загрузка...</div>;
  if (error) return <div className="container error">{error}</div>;

  return (
    <div className="container">
      <h1>Объявления</h1>
      
      <div className="category-tabs">
        {categories.map(cat => (
          <button
            key={cat}
            className={`category-tab ${category === cat ? 'active' : ''}`}
            onClick={() => setCategory(cat)}
          >
            {categoryLabels[cat]}
          </button>
        ))}
      </div>
      
      {filteredAnnouncements.length === 0 ? (
        <div className="card">
          <p>Нет объявлений в выбранной категории</p>
        </div>
      ) : (
        <div className="grid">
          {filteredAnnouncements.map(announcement => {
            // Получаем userId из localStorage или из состояния
            const userId = currentUserId || localStorage.getItem('userId');
            const isOwner = announcement.user_id === parseInt(userId);
            
            return (
              <div key={announcement.id} className="card">
                <h3>{announcement.name}</h3>
                <p><strong>Ссылка:</strong> {announcement.link}</p>
                <p>
                  <strong>Категория:</strong> {categoryLabels[announcement.category]}
                </p>
                <p>
                  <strong>Начало:</strong> {formatDate(announcement.date)}
                </p>
                <p>
                  <strong>Конец:</strong> {formatDate(announcement.end_date)}
                </p>
                
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
                  
                  {/* Показываем кнопку удаления только если пользователь владелец */}
                  {isOwner && (
                    <button 
                      className="btn btn-danger"
                      onClick={() => handleDelete(announcement.id)}
                    >
                      Удалить
                    </button>
                  )}
                </div>
                
                {isOwner && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: '#666' }}>
                    (Ваше объявление)
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
      
      <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
        ⏱️ Обновляется каждые 3 секунды
      </div>
    </div>
  );
};

export default AnnouncementList;