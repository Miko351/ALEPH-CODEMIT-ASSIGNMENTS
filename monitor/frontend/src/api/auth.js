import { apiRequest } from './client.js';
export const login = (username, password) => apiRequest('/auth/login', {
  method: 'POST', body: JSON.stringify({ username, password }),
});
