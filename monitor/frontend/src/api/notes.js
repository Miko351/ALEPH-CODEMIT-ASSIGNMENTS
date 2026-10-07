import { apiRequest } from './client.js';
export const getNotes = () => apiRequest('/notes');
export const getNote = (id) => apiRequest(`/notes/${id}`);
export const createNote = (values) => apiRequest('/notes', { method: 'POST', body: JSON.stringify(values) });
export const updateNote = (id, values) => apiRequest(`/notes/${id}`, { method: 'PUT', body: JSON.stringify(values) });
export const deleteNote = (id) => apiRequest(`/notes/${id}`, { method: 'DELETE' });
