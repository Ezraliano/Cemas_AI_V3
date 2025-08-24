import axios from 'axios';

// Base URL for API
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config: { headers: { Authorization: string; }; }) => {
  // Check if code is running in browser environment
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Auth API
export const authAPI = {
  register: async (email: string, name: string, password: string) => {
    const response = await api.post('/auth/register', { email, name, password });
    return response.data;
  },
  
  login: async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    // Store token in localStorage (only in browser environment)
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', response.data.access_token);
    }
    
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
  
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  },
};

// Chat API
export const chatAPI = {
  getConversations: async () => {
    const response = await api.get('/conversations/');
    return response.data;
  },
  
  getConversation: async (id: number) => {
    const response = await api.get(`/conversations/${id}`);
    return response.data;
  },
  
  createConversation: async (title: string) => {
    const response = await api.post('/conversations/', { title });
    return response.data;
  },
  
  updateConversation: async (id: number, title: string) => {
    const response = await api.put(`/conversations/${id}`, { title });
    return response.data;
  },
  
  deleteConversation: async (id: number) => {
    await api.delete(`/conversations/${id}`);
  },
  
  getMessages: async (conversationId: number) => {
    const response = await api.get(`/conversations/${conversationId}/messages/`);
    return response.data;
  },
  
  sendMessage: async (conversationId: number, content: string) => {
    const response = await api.post(`/conversations/${conversationId}/messages/`, {
      role: 'user',
      content,
    });
    return response.data;
  },
  
  getInsights: async (conversationId: number) => {
    const response = await api.post(`/conversations/${conversationId}/insights/`);
    return response.data;
  },
};

// User API
export const userAPI = {
  getUsers: async () => {
    const response = await api.get('/users/');
    return response.data;
  },
};

export default {
  auth: authAPI,
  chat: chatAPI,
  user: userAPI,
};