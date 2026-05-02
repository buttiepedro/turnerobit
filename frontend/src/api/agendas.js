import apiClient from './client';

export const listAgendas = () => apiClient.get('/agendas');
export const getAgenda = (id) => apiClient.get(`/agendas/${id}`);
export const createAgenda = (data) => apiClient.post('/agendas', data);
export const updateAgenda = (id, data) => apiClient.put(`/agendas/${id}`, data);
export const deactivateAgenda = (id) => apiClient.delete(`/agendas/${id}`);
export const getSlots = (agendaId, date) =>
  apiClient.get(`/agendas/${agendaId}/slots`, { params: { date } });
