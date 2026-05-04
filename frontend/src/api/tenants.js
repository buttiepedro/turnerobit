import apiClient from './client';

export const listTenants = () => apiClient.get('/superadmin/tenants');
export const getTenant = (id) => apiClient.get(`/superadmin/tenants/${id}`);
export const createTenant = (data) => apiClient.post('/superadmin/tenants', data);
export const updateTenant = (id, data) => apiClient.patch(`/superadmin/tenants/${id}`, data);
export const deactivateTenant = (id) => apiClient.delete(`/superadmin/tenants/${id}`);

export const listTenantUsers = (tenantId) =>
  apiClient.get(`/superadmin/tenants/${tenantId}/users`);
export const createTenantUser = (tenantId, data) =>
  apiClient.post(`/superadmin/tenants/${tenantId}/users`, data);
export const updateTenantUser = (tenantId, userId, data) =>
  apiClient.patch(`/superadmin/tenants/${tenantId}/users/${userId}`, data);
export const resetTenantUserPassword = (tenantId, userId, data) =>
  apiClient.post(`/superadmin/tenants/${tenantId}/users/${userId}/reset-password`, data);
