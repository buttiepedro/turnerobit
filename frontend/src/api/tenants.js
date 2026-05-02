import apiClient from './client';

export const listTenants = () => apiClient.get('/superadmin/tenants');
export const getTenant = (id) => apiClient.get(`/superadmin/tenants/${id}`);
export const createTenant = (data) => apiClient.post('/superadmin/tenants', data);
export const updateTenant = (id, data) => apiClient.patch(`/superadmin/tenants/${id}`, data);
export const deactivateTenant = (id) => apiClient.delete(`/superadmin/tenants/${id}`);
