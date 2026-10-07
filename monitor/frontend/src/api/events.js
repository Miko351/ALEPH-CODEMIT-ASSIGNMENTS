import { apiRequest } from './client.js';
export const getEvents = () => apiRequest('/events');
