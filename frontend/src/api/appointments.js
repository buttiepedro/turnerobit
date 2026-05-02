import apiClient from './client';

export const list = (params) => apiClient.get('/appointments', { params });
export const create = (data) => apiClient.post('/appointments', data);
export const get = (id) => apiClient.get(`/appointments/${id}`);
export const update = (id, data) => apiClient.patch(`/appointments/${id}`, data);
export const cancel = (id, reason) =>
  apiClient.post(`/appointments/${id}/cancel`, { reason });
export const confirm = (id) => apiClient.post(`/appointments/${id}/confirm`);
export const complete = (id) => apiClient.post(`/appointments/${id}/complete`);
export const checkAvailability = (agendaId, date) =>
  apiClient.get('/appointments/availability', { params: { agenda_id: agendaId, date } });
