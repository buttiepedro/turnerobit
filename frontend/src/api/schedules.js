import apiClient from './client';

export const listSchedules = (agendaId) =>
  apiClient.get('/schedules', { params: { agenda_id: agendaId } });
export const createSchedule = (data) => apiClient.post('/schedules', data);
export const updateSchedule = (id, data) => apiClient.put(`/schedules/${id}`, data);
export const deleteSchedule = (id) => apiClient.delete(`/schedules/${id}`);

export const listExceptions = (agendaId) =>
  apiClient.get('/schedules/exceptions', { params: { agenda_id: agendaId } });
export const createException = (data) => apiClient.post('/schedules/exceptions', data);
