import { useState } from 'react';
import { useAgendas, useCreateAgenda } from '../../hooks/useAgendas.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Modal } from '../../components/ui/Modal.jsx';
import { Input } from '../../components/ui/Input.jsx';

export default function AgendasPage() {
  const { data: agendas = [], isLoading } = useAgendas();
  const createMutation = useCreateAgenda();
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({ name: '', slot_duration_minutes: 30, color: '#3B82F6' });
  const [error, setError] = useState('');

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await createMutation.mutateAsync({ ...form, slot_duration_minutes: Number(form.slot_duration_minutes) });
      setIsOpen(false);
      setForm({ name: '', slot_duration_minutes: 30, color: '#3B82F6' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear agenda');
    }
  };

  return (
    <PageWrapper>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Agendas</h1>
        <Button onClick={() => setIsOpen(true)}>Nueva agenda</Button>
      </div>

      {isLoading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {agendas.map((agenda) => (
            <div key={agenda.id} className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: agenda.color }} />
                <p className="font-semibold text-gray-900">{agenda.name}</p>
              </div>
              <p className="text-xs text-gray-500">Turno: {agenda.slot_duration_minutes} min</p>
              <p className="text-xs text-gray-500">
                Estado: {agenda.is_active ? 'Activa' : 'Inactiva'}
              </p>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Nueva Agenda">
        <form onSubmit={handleCreate} className="flex flex-col gap-4">
          <Input label="Nombre" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <Input label="Duración del turno (min)" type="number" min={5} value={form.slot_duration_minutes} onChange={(e) => setForm({ ...form, slot_duration_minutes: e.target.value })} />
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">Color</label>
            <input type="color" value={form.color} onChange={(e) => setForm({ ...form, color: e.target.value })} className="w-10 h-8 cursor-pointer rounded" />
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
