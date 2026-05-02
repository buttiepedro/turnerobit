import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTenant, updateTenant, deactivateTenant } from '../../api/tenants.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Input } from '../../components/ui/Input.jsx';

export default function TenantDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tenant, setTenant] = useState(null);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({});

  useEffect(() => {
    getTenant(id).then((r) => {
      setTenant(r.data);
      setForm({ name: r.data.name, max_agendas: r.data.max_agendas, plan: r.data.plan });
    });
  }, [id]);

  const handleSave = async (e) => {
    e.preventDefault();
    await updateTenant(id, { ...form, max_agendas: Number(form.max_agendas) });
    setEditing(false);
    getTenant(id).then((r) => setTenant(r.data));
  };

  const handleDeactivate = async () => {
    if (!confirm('¿Desactivar este tenant?')) return;
    await deactivateTenant(id);
    navigate('/superadmin/tenants');
  };

  if (!tenant) return <PageWrapper><p className="text-gray-500">Cargando...</p></PageWrapper>;

  return (
    <PageWrapper>
      <div className="max-w-xl">
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
          <form onSubmit={handleSave} className="flex flex-col gap-4 bg-white p-6 rounded-xl border border-gray-200">
            <Input label="Nombre" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            <Input label="Plan" value={form.plan} onChange={(e) => setForm({ ...form, plan: e.target.value })} />
            <Input label="Máx. agendas" type="number" min={1} value={form.max_agendas} onChange={(e) => setForm({ ...form, max_agendas: e.target.value })} />
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
    </PageWrapper>
  );
}
