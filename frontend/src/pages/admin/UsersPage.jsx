import { useEffect, useState } from 'react';
import apiClient from '../../api/client.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Modal } from '../../components/ui/Modal.jsx';
import { Input } from '../../components/ui/Input.jsx';

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({ email: '', password: '', full_name: '', role: 'usuario_agenda' });
  const [error, setError] = useState('');

  const load = () => apiClient.get('/tenants/users').then((r) => setUsers(r.data)).catch(() => {});

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await apiClient.post('/tenants/users', form);
      setIsOpen(false);
      setForm({ email: '', password: '', full_name: '', role: 'usuario_agenda' });
      load();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear usuario');
    }
  };

  return (
    <PageWrapper>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Usuarios</h1>
        <Button onClick={() => setIsOpen(true)}>Nuevo usuario</Button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              {['Nombre', 'Email', 'Rol', 'Estado'].map((h) => (
                <th key={h} className="px-4 py-3 text-left">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {users.map((u) => (
              <tr key={u.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium text-gray-900">{u.full_name}</td>
                <td className="px-4 py-3 text-gray-500">{u.email}</td>
                <td className="px-4 py-3">{u.role}</td>
                <td className="px-4 py-3">
                  <span className={`text-xs font-medium ${u.is_active ? 'text-green-700' : 'text-red-600'}`}>
                    {u.is_active ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Nuevo Usuario">
        <form onSubmit={handleCreate} className="flex flex-col gap-4">
          <Input label="Nombre completo" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required />
          <Input label="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <Input label="Contraseña" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">Rol</label>
            <select
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
            >
              <option value="usuario_agenda">Usuario Agenda</option>
              <option value="admin_empresa">Admin Empresa</option>
            </select>
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="flex gap-2 justify-end">
            <Button variant="ghost" type="button" onClick={() => setIsOpen(false)}>Cancelar</Button>
            <Button type="submit">Crear</Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
