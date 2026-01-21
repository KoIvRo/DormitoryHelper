import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { announcementAPI } from '../services/api';

const AnnouncementForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    link: '',
    category: 'transport',
    date: '',
    end_date: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      // Преобразуем даты в нужный формат ISO
      const announcementData = {
        ...formData,
        date: new Date(formData.date).toISOString(),
        end_date: new Date(formData.end_date).toISOString()
      };

      await announcementAPI.createAnnouncement(announcementData);
      
      setSuccess('Объявление успешно создано!');
      setFormData({
        name: '',
        link: '',
        category: 'transport',
        date: '',
        end_date: ''
      });
      
      // Через 2 секунды перенаправляем на главную
      setTimeout(() => {
        navigate('/');
      }, 2000);
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка создания объявления');
    } finally {
      setLoading(false);
    }
  };

  const getCurrentDateTime = () => {
    const now = new Date();
    // Форматируем в YYYY-MM-DDTHH:mm
    return now.toISOString().slice(0, 16);
  };

  return (
    <div className="container">
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <h1>Создать новое объявление</h1>
        
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Название:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Например: Такси"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="link">Ссылка/Контакт:</label>
            <input
              type="text"
              id="link"
              name="link"
              value={formData.link}
              onChange={handleChange}
              required
              placeholder="+7912XXXXXXX или ссылка"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="category">Категория:</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="transport">Транспорт</option>
              <option value="sale">Продажи</option>
              <option value="hobby">Хобби</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="date">Дата и время начала:</label>
            <input
              type="datetime-local"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              required
              min={getCurrentDateTime()}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="end_date">Дата и время окончания:</label>
            <input
              type="datetime-local"
              id="end_date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              required
              min={formData.date || getCurrentDateTime()}
            />
          </div>
          
          <button 
            type="submit" 
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Создание...' : 'Создать объявление'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AnnouncementForm;