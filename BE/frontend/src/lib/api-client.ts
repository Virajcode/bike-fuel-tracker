import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface ChatSession {
  id: number;
  topic: string | null;
  created_at: string;
  last_updated: string;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  message: string;
  response: string;
  response_type?: string;
  timestamp: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  data?: {
    access_token: string;
    token_type: string;
  };
}

export const apiClient = {
  auth: {
    login: async (email: string, password: string) => {
      const response = await api.post<LoginResponse>('/signin', { email, password });
      if (response.data.data?.access_token) {
        localStorage.setItem('token', response.data.data.access_token);
      }
      return response.data;
    },
    signup: async (email: string, password: string) => {
      return api.post('/signup', { email, password });
    },
    logout: () => {
      localStorage.removeItem('token');
    },
  },
  chat: {
    createSession: async (topic?: string) => {
      const response = await api.post<ChatSession>('/chat/sessions', { topic });
      return response.data;
    },
    getSessions: async () => {
      const response = await api.get<ChatSession[]>('/chat/sessions');
      return response.data;
    },
    getSession: async (sessionId: number) => {
      const response = await api.get<ChatSession>(`/chat/sessions/${sessionId}`);
      return response.data;
    },
    getHistory: async (sessionId: number) => {
      const response = await api.get<ChatMessage[]>(`/chat/history/${sessionId}`);
      return response.data;
    },
    saveMessage: async (sessionId: number, message: string, response: string, response_type: string = "text") => {
      return api.post('/chat/history', { session_id: sessionId, message, response, response_type });
    },
  },
};
