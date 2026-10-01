import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL ||
  (process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getApiErrorMessage = (error, fallback) => {
  const detail = error.response?.data?.detail;

  if (typeof detail === 'string') {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const field = Array.isArray(item.loc) ? item.loc[item.loc.length - 1] : null;
        return field ? `${field}: ${item.msg}` : item.msg;
      })
      .filter(Boolean)
      .join('; ');
  }

  return fallback;
};

// Очередь запросов, ожидающих обновления токена
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// Интерцептор для автоматической вставки токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Интерцептор для обработки ошибок 401 и refresh токена
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Если ошибка 401 и это не запрос на refresh
    if (error.response?.status === 401 && 
        !originalRequest.url.includes('/auth/refresh') &&
        !originalRequest._retry) {
      
      if (isRefreshing) {
        // Если уже обновляем токен, добавляем запрос в очередь
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return axios(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }
      
      originalRequest._retry = true;
      isRefreshing = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        processQueue(error, null);
        isRefreshing = false;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('userId');
        return Promise.reject(error);
      }
      
      try {
        // Пытаемся обновить access токен
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken
        });
        
        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken);
        
        // Обновляем заголовок и перезапускаем запрос
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        
        // Обрабатываем очередь ожидающих запросов
        processQueue(null, newAccessToken);
        isRefreshing = false;
        
        return axios(originalRequest);
      } catch (refreshError) {
        // Если refresh не удался, очищаем localStorage
        processQueue(refreshError, null);
        isRefreshing = false;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('userId');
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (userData) => api.post('/auth/login', userData),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
};

export const announcementAPI = {
  getAllAnnouncements: () => api.get('/announcements/'),
  getAnnouncementById: (id) => api.get(`/announcements/${id}`),
  getAnnouncementsByCategory: (category) => api.get(`/announcements/category/${category}`),
  createAnnouncement: (announcementData) => api.post('/announcements/', announcementData),
  updateAnnouncement: (id, announcementData) => api.put(`/announcements/${id}`, announcementData),
  deleteAnnouncement: (id) => api.delete(`/announcements/${id}`),
};

export const userAPI = {
  getMe: () => api.get('/user/me'),
};

export default api;
