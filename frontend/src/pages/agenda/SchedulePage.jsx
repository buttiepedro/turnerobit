import { useEffect, useState } from 'react';
import { listAgendas } from '../../api/agendas.js';
import { listSchedules, createSchedule, deleteSchedule } from '../../api/schedules.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Modal } from '../../components/ui/Modal.jsx';
import { Input } from '../../components/ui/Input.jsx';
import { dayNames } from '../../utils/formatters.js';

export default function SchedulePage() {
  const [agendas, setAgendas] = useState([]);
  const [selectedAgenda, setSelectedAgenda] = useState('');
  const [schedules, setSchedules] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({ day_of_week: 0, start_time: '08:00', end_time: '17:00' });

  useEffect(() => {
    listAgendas().then((r) => {
      setAgendas(r.data);
      if (r.data.length) setSelectedAgenda(r.data[0].id);
    });
  }, []);

  useEffect(() => {
    if (selectedAgenda) listSchedules(selectedAgenda).then((r) => setSchedules(r.data));
  }, [selectedAgenda]);

  const handleCreate = async (e) => {
    e.preventDefault();
    await createSchedule({ ...form, agenda_id: selectedAgenda, day_of_week: Number(form.day_of_week) });
    setIsOpen(false);
    listSchedules(selectedAgenda).then((r) => setSchedules(r.data));
  };

  const handleDelete = async (id) => {
    await deleteSchedule(id);
    setSchedules((prev) => prev.filter((s) => s.id !== id));
  };

  return (
    <PageWrapper>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Horarios de Atención</h1>
        <Button onClick={() => setIsOpen(true)} disabled={!selectedAgenda}>Agregar horario</Button>
      </div>

      <div className="mb-4">
        <select
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
          value={selectedAgenda}
          onChange={(e) => setSelectedAgenda(e.target.value)}
        >
          {agendas.map((a) => <option key={a.id} value={a.id}>{a.name}</option>)}
        </select>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              {['Día', 'Inicio', 'Fin', 'Estado', ''].map((h) => (
                <th key={h} className="px-4 py-3 text-left">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {schedules.map((s) => (
              <tr key={s.id}>
                <td className="px-4 py-3">{dayNames[s.day_of_week]}</td>
                <td className="px-4 py-3">{s.start_time?.substring(0, 5)}</td>
                <td className="px-4 py-3">{s.end_time?.substring(0, 5)}</td>
                <td className="px-4 py-3">{s.is_active ? 'Activo' : 'Inactivo'}</td>
                <td className="px-4 py-3">
                  <Button variant="danger" className="text-xs py-1" onClick={() => handleDelete(s.id)}>
                    Eliminar
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Nuevo Horario">
        <form onSubmit={handleCreate} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">Día</label>
            <select
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              value={form.day_of_week}
              onChange={(e) => setForm({ ...form, day_of_week: e.target.value })}
            >
              {dayNames.map((d, i) => <option key={i} value={i}>{d}</option>)}
            </select>
          </div>
          <Input label="Hora inicio" type="time" value={form.start_time} onChange={(e) => setForm({ ...form, start_time: e.target.value })} />
          <Input label="Hora fin" type="time" value={form.end_time} onChange={(e) => setForm({ ...form, end_time: e.target.value })} />
          <div className="flex gap-2 justify-end">
            <Button variant="ghost" type="button" onClick={() => setIsOpen(false)}>Cancelar</Button>
            <Button type="submit">Guardar</Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
