import { Navigate, Route, Routes } from 'react-router-dom';
import { RoleRoute } from './routes/RoleRoute.jsx';

import LoginPage from './pages/auth/LoginPage.jsx';
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage.jsx';

import TenantsPage from './pages/superadmin/TenantsPage.jsx';
import TenantDetailPage from './pages/superadmin/TenantDetailPage.jsx';

import DashboardPage from './pages/admin/DashboardPage.jsx';
import AgendasPage from './pages/admin/AgendasPage.jsx';
import UsersPage from './pages/admin/UsersPage.jsx';

import CalendarPage from './pages/agenda/CalendarPage.jsx';
import SchedulePage from './pages/agenda/SchedulePage.jsx';
import AppointmentsPage from './pages/agenda/AppointmentsPage.jsx';

function Unauthorized() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white rounded-xl p-8 shadow text-center">
        <h1 className="text-xl font-bold text-red-600 mb-2">Acceso denegado</h1>
        <p className="text-gray-500">No tenés permisos para ver esta página.</p>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/unauthorized" element={<Unauthorized />} />

      {/* Superadmin */}
      <Route
        path="/superadmin/tenants"
        element={
          <RoleRoute allowedRoles={['superadmin']}>
            <TenantsPage />
          </RoleRoute>
        }
      />
      <Route
        path="/superadmin/tenants/:id"
        element={
          <RoleRoute allowedRoles={['superadmin']}>
            <TenantDetailPage />
          </RoleRoute>
        }
      />

      {/* Admin Empresa */}
      <Route
        path="/admin/dashboard"
        element={
          <RoleRoute allowedRoles={['admin_empresa']}>
            <DashboardPage />
          </RoleRoute>
        }
      />
      <Route
        path="/admin/agendas"
        element={
          <RoleRoute allowedRoles={['admin_empresa']}>
            <AgendasPage />
          </RoleRoute>
        }
      />
      <Route
        path="/admin/users"
        element={
          <RoleRoute allowedRoles={['admin_empresa']}>
            <UsersPage />
          </RoleRoute>
        }
      />

      {/* Usuario Agenda */}
      <Route
        path="/agenda/calendar"
        element={
          <RoleRoute allowedRoles={['usuario_agenda', 'admin_empresa']}>
            <CalendarPage />
          </RoleRoute>
        }
      />
      <Route
        path="/agenda/schedule"
        element={
          <RoleRoute allowedRoles={['usuario_agenda', 'admin_empresa']}>
            <SchedulePage />
          </RoleRoute>
        }
      />
      <Route
        path="/agenda/appointments"
        element={
          <RoleRoute allowedRoles={['usuario_agenda', 'admin_empresa']}>
            <AppointmentsPage />
          </RoleRoute>
        }
      />

      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
