import apiClient from './client';

export const loginUser = (username, password) => {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);
  return apiClient.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
};

export const getMe = () => apiClient.get('/auth/me');
