import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  getTenant, updateTenant, deactivateTenant,
  listTenantUsers, createTenantUser, updateTenantUser, resetTenantUserPassword,
} from '../../api/tenants.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Input } from '../../components/ui/Input.jsx';
import { Modal } from '../../components/ui/Modal.jsx';

const ROLE_LABELS = {
  admin_empresa: 'Admin',
  usuario_agenda: 'Operador',
};

export default function TenantDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [tenant, setTenant] = useState(null);
  const [editing, setEditing] = useState(false);
  const [tenantForm, setTenantForm] = useState({});

  const [users, setUsers] = useState([]);
  const [createOpen, setCreateOpen] = useState(false);
  const [resetOpen, setResetOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  const [createForm, setCreateForm] = useState({
    email: '', password: '', full_name: '', role: 'usuario_agenda',
  });
  const [resetPassword, setResetPassword] = useState('');
  const [error, setError] = useState('');

  const loadTenant = () =>
    getTenant(id).then((r) => {
      setTenant(r.data);
      setTenantForm({ name: r.data.name, max_agendas: r.data.max_agendas, plan: r.data.plan });
    });

  const loadUsers = () =>
    listTenantUsers(id).then((r) => setUsers(r.data));

  useEffect(() => {
    loadTenant();
    loadUsers();
  }, [id]);

  const handleSaveTenant = async (e) => {
    e.preventDefault();
    await updateTenant(id, { ...tenantForm, max_agendas: Number(tenantForm.max_agendas) });
    setEditing(false);
    loadTenant();
  };

  const handleDeactivate = async () => {
    if (!confirm('¿Desactivar este tenant?')) return;
    await deactivateTenant(id);
    navigate('/superadmin/tenants');
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await createTenantUser(id, createForm);
      setCreateOpen(false);
      setCreateForm({ email: '', password: '', full_name: '', role: 'usuario_agenda' });
      loadUsers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear usuario');
    }
  };

  const handleToggleActive = async (user) => {
    await updateTenantUser(id, user.id, { is_active: !user.is_active });
    loadUsers();
  };

  const openResetModal = (user) => {
    setSelectedUser(user);
    setResetPassword('');
    setError('');
    setResetOpen(true);
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await resetTenantUserPassword(id, selectedUser.id, { new_password: resetPassword });
      setResetOpen(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cambiar contraseña');
    }
  };

  if (!tenant) return <PageWrapper><p className="text-gray-500">Cargando...</p></PageWrapper>;

  return (
    <PageWrapper>
      {/* ── Tenant info ────────────────────────────────────────────── */}
      <div className="max-w-2xl mb-10">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900">{tenant.name}</h1>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => setEditing(!editing)}>
              {editing ? 'Cancelar' : 'Editar'}
            </Button>
            <Button variant="danger" onClick={handleDeactivate}>Desactivar</Button>
          </div>
        </div>

        {editing ? (
          <form onSubmit={handleSaveTenant} className="flex flex-col gap-4 bg-white p-6 rounded-xl border border-gray-200">
            <Input label="Nombre" value={tenantForm.name} onChange={(e) => setTenantForm({ ...tenantForm, name: e.target.value })} />
            <Input label="Plan" value={tenantForm.plan} onChange={(e) => setTenantForm({ ...tenantForm, plan: e.target.value })} />
            <Input label="Máx. agendas" type="number" min={1} value={tenantForm.max_agendas} onChange={(e) => setTenantForm({ ...tenantForm, max_agendas: e.target.value })} />
            <Button type="submit">Guardar cambios</Button>
          </form>
        ) : (
          <div className="bg-white rounded-xl border border-gray-200 p-6 grid grid-cols-2 gap-4 text-sm">
            {[
              ['Slug', tenant.slug],
              ['Schema', tenant.schema_name],
              ['Plan', tenant.plan],
              ['Máx. agendas', tenant.max_agendas],
              ['Estado', tenant.is_active ? 'Activo' : 'Inactivo'],
              ['Creado', tenant.created_at?.substring(0, 10)],
            ].map(([label, value]) => (
              <div key={label}>
                <p className="text-gray-500 text-xs">{label}</p>
                <p className="font-medium text-gray-900">{value}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Usuarios del tenant ────────────────────────────────────── */}
      <div className="max-w-2xl">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Usuarios</h2>
          <Button onClick={() => { setError(''); setCreateOpen(true); }}>Nuevo usuario</Button>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          {users.length === 0 ? (
            <p className="text-sm text-gray-500 p-6">Este tenant no tiene usuarios aún.</p>
          ) : (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
                <tr>
                  {['Nombre', 'Email', 'Rol', 'Estado', 'Acciones'].map((h) => (
                    <th key={h} className="px-4 py-3 text-left">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-gray-900">{u.full_name}</td>
                    <td className="px-4 py-3 text-gray-500">{u.email}</td>
                    <td className="px-4 py-3 text-gray-600">{ROLE_LABELS[u.role] ?? u.role}</td>
                    <td className="px-4 py-3">
                      <span className={`text-xs font-medium ${u.is_active ? 'text-green-700' : 'text-red-600'}`}>
                        {u.is_active ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <button
                          onClick={() => openResetModal(u)}
                          className="text-xs text-blue-600 hover:underline"
                        >
                          Contraseña
                        </button>
                        <button
                          onClick={() => handleToggleActive(u)}
                          className="text-xs text-gray-500 hover:underline"
                        >
                          {u.is_active ? 'Desactivar' : 'Activar'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* ── Modal: crear usuario ───────────────────────────────────── */}
      <Modal isOpen={createOpen} onClose={() => setCreateOpen(false)} title="Nuevo usuario">
        <form onSubmit={handleCreateUser} className="flex flex-col gap-4">
          <Input
            label="Nombre completo"
            value={createForm.full_name}
            onChange={(e) => setCreateForm({ ...createForm, full_name: e.target.value })}
            required
          />
          <Input
            label="Email"
            type="email"
            value={createForm.email}
            onChange={(e) => setCreateForm({ ...createForm, email: e.target.value })}
            required
          />
          <Input
            label="Contraseña"
            type="password"
            value={createForm.password}
            onChange={(e) => setCreateForm({ ...createForm, password: e.target.value })}
            required
          />
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">Rol</label>
            <select
              value={createForm.role}
              onChange={(e) => setCreateForm({ ...createForm, role: e.target.value })}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="usuario_agenda">Operador</option>
              <option value="admin_empresa">Admin empresa</option>
            </select>
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="flex gap-2 justify-end">
            <Button variant="ghost" type="button" onClick={() => setCreateOpen(false)}>Cancelar</Button>
            <Button type="submit">Crear</Button>
          </div>
        </form>
      </Modal>

      {/* ── Modal: resetear contraseña ─────────────────────────────── */}
      <Modal isOpen={resetOpen} onClose={() => setResetOpen(false)} title={`Cambiar contraseña — ${selectedUser?.full_name}`}>
        <form onSubmit={handleResetPassword} className="flex flex-col gap-4">
          <Input
            label="Nueva contraseña"
            type="password"
            value={resetPassword}
            onChange={(e) => setResetPassword(e.target.value)}
            required
          />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="flex gap-2 justify-end">
            <Button variant="ghost" type="button" onClick={() => setResetOpen(false)}>Cancelar</Button>
            <Button type="submit">Guardar</Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
