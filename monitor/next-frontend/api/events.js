import { request } from './client';
export const listEvents = () => request('/events');
