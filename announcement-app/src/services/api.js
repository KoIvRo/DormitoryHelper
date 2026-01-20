// src/services/api.js
import axios from 'axios';

// Базовый URL вашего FastAPI бэкенда
const API_BASE_URL = 'http://localhost:8000';

// Создаем экземпляр axios с базовыми настройками
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем интерцептор для автоматической вставки токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Функции для работы с авторизацией
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (userData) => api.post('/auth/login', userData),
};

// Функции для работы с объявлениями
export const announcementAPI = {
  getAllAnnouncements: () => api.get('/announcements/'),
  getAnnouncementById: (id) => api.get(`/announcements/${id}`),
  getAnnouncementsByCategory: (category) => api.get(`/announcements/category/${category}`),
  createAnnouncement: (announcementData) => api.post('/announcements/', announcementData),
  deleteAnnouncement: (id) => api.delete(`/announcements/${id}`),
};

// Функции для работы с пользователем
export const userAPI = {
  getMe: () => api.get('/user/me'),
};

export default api;