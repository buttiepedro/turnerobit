import { useEffect, useState } from 'react';
import { listAgendas } from '../../api/agendas.js';
import { AppointmentCard } from '../../components/appointment/AppointmentCard.jsx';
import { AppointmentForm } from '../../components/appointment/AppointmentForm.jsx';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Modal } from '../../components/ui/Modal.jsx';
import { useAppointments } from '../../hooks/useAppointments.js';
import { getSlots } from '../../api/agendas.js';
import { todayISO } from '../../utils/dateUtils.js';

export default function AppointmentsPage() {
  const [agendas, setAgendas] = useState([]);
  const [selectedAgenda, setSelectedAgenda] = useState('');
  const [filterDate, setFilterDate] = useState(todayISO());
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [cancelId, setCancelId] = useState(null);
  const [cancelReason, setCancelReason] = useState('');

  const { appointments, fetchAppointments, createAppointment, cancelAppointment, completeAppointment } =
    useAppointments(selectedAgenda);

  useEffect(() => {
    listAgendas().then((r) => {
      setAgendas(r.data);
      if (r.data.length) setSelectedAgenda(r.data[0].id);
    });
  }, []);

  useEffect(() => {
    if (selectedAgenda) {
      fetchAppointments({ appointment_date: filterDate });
      getSlots(selectedAgenda, filterDate).then((r) => setSlots(r.data));
    }
  }, [selectedAgenda, filterDate]);

  const handleBook = async (payload) => {
    await createAppointment(payload);
    setShowForm(false);
    setSelectedSlot(null);
    getSlots(selectedAgenda, filterDate).then((r) => setSlots(r.data));
  };

  const handleCancel = async () => {
    await cancelAppointment(cancelId, cancelReason || 'Sin motivo');
    setCancelId(null);
    setCancelReason('');
  };

  return (
    <PageWrapper>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Turnos</h1>

      <div className="flex gap-3 mb-6 flex-wrap">
        <select
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
          value={selectedAgenda}
          onChange={(e) => setSelectedAgenda(e.target.value)}
        >
          {agendas.map((a) => <option key={a.id} value={a.id}>{a.name}</option>)}
        </select>
        <input
          type="date"
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
          value={filterDate}
          onChange={(e) => setFilterDate(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <section>
          <h2 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">Slots disponibles</h2>
          <div className="grid grid-cols-3 gap-2">
            {slots.map((slot) => (
              <button
                key={slot.start_time}
                disabled={!slot.available}
                onClick={() => { setSelectedSlot(slot); setShowForm(true); }}
                className={`rounded-lg border text-sm py-2 font-medium transition-colors ${
                  slot.available
                    ? 'border-blue-300 bg-blue-50 text-blue-700 hover:bg-blue-100'
                    : 'border-gray-200 bg-gray-100 text-gray-400 cursor-not-allowed'
                }`}
              >
                {slot.start_time.substring(0, 5)}
              </button>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">Turnos del día</h2>
          <div className="flex flex-col gap-3">
            {appointments.map((a) => (
              <AppointmentCard
                key={a.id}
                appointment={a}
                onCancel={(id) => setCancelId(id)}
                onComplete={completeAppointment}
              />
            ))}
            {appointments.length === 0 && (
              <p className="text-sm text-gray-400">Sin turnos para esta fecha.</p>
            )}
          </div>
        </section>
      </div>

      <Modal isOpen={showForm && !!selectedSlot} onClose={() => setShowForm(false)} title="Nuevo Turno">
        {selectedSlot && (
          <AppointmentForm
            slot={selectedSlot}
            agendaId={selectedAgenda}
            appointmentDate={filterDate}
            onSubmit={handleBook}
            onCancel={() => setShowForm(false)}
          />
        )}
      </Modal>

      <Modal isOpen={!!cancelId} onClose={() => setCancelId(null)} title="Cancelar Turno">
        <div className="flex flex-col gap-4">
          <input
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
            placeholder="Motivo de cancelación"
            value={cancelReason}
            onChange={(e) => setCancelReason(e.target.value)}
          />
          <div className="flex gap-2 justify-end">
            <Button variant="ghost" onClick={() => setCancelId(null)}>Volver</Button>
            <Button variant="danger" onClick={handleCancel}>Confirmar cancelación</Button>
          </div>
        </div>
      </Modal>
    </PageWrapper>
  );
}
