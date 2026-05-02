import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listTenants, createTenant } from '../../api/tenants.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Modal } from '../../components/ui/Modal.jsx';
import { Input } from '../../components/ui/Input.jsx';

export default function TenantsPage() {
  const [tenants, setTenants] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({ slug: '', name: '', max_agendas: 1, plan: 'basic' });
  const [error, setError] = useState('');

  const load = () => listTenants().then((r) => setTenants(r.data));

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await createTenant({ ...form, max_agendas: Number(form.max_agendas) });
      setIsOpen(false);
      setForm({ slug: '', name: '', max_agendas: 1, plan: 'basic' });
      load();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear tenant');
    }
  };

  return (
    <PageWrapper>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Tenants</h1>
        <Button onClick={() => setIsOpen(true)}>Nuevo tenant</Button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              {['Nombre', 'Slug', 'Plan', 'Agendas', 'Estado', ''].map((h) => (
                <th key={h} className="px-4 py-3 text-left">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {tenants.map((t) => (
              <tr key={t.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium text-gray-900">{t.name}</td>
                <td className="px-4 py-3 text-gray-500">{t.slug}</td>
                <td className="px-4 py-3">{t.plan}</td>
                <td className="px-4 py-3">{t.max_agendas}</td>
                <td className="px-4 py-3">
                  <span className={`text-xs font-medium ${t.is_active ? 'text-green-700' : 'text-red-600'}`}>
                    {t.is_active ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <Link to={`/superadmin/tenants/${t.id}`} className="text-blue-600 hover:underline text-xs">
                    Ver
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Nuevo Tenant">
        <form onSubmit={handleCreate} className="flex flex-col gap-4">
          <Input label="Nombre" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <Input label="Slug (URL-safe)" value={form.slug} onChange={(e) => setForm({ ...form, slug: e.target.value })} required placeholder="mi-empresa" />
          <Input label="Máx. agendas" type="number" min={1} value={form.max_agendas} onChange={(e) => setForm({ ...form, max_agendas: e.target.value })} />
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
