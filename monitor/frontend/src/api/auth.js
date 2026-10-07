import { apiRequest } from './client.js';
export const login = (username, password) => apiRequest('/auth/login', {
  method: 'POST', body: JSON.stringify({ username, password }),
});
export const getCurrentUser = () => apiRequest('/auth/me');
export const logout = () => apiRequest('/auth/logout', { method: 'POST' });
