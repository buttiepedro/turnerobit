import { useEffect, useState } from 'react';
import { listAgendas } from '../../api/agendas.js';
import { list as listAppointments } from '../../api/appointments.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';
import { StatusBadge } from '../../components/ui/Badge.jsx';
import { formatTime } from '../../utils/formatters.js';
import { toISODate } from '../../utils/dateUtils.js';
import { addDays, startOfWeek, format } from 'date-fns';
import { es } from 'date-fns/locale';

export default function CalendarPage() {
  const [agendas, setAgendas] = useState([]);
  const [selectedAgenda, setSelectedAgenda] = useState('');
  const [weekStart, setWeekStart] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));
  const [appointments, setAppointments] = useState([]);

  const weekDays = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));

  useEffect(() => {
    listAgendas().then((r) => {
      setAgendas(r.data);
      if (r.data.length) setSelectedAgenda(r.data[0].id);
    });
  }, []);

  useEffect(() => {
    if (!selectedAgenda) return;
    const from = toISODate(weekStart);
    listAppointments({ agenda_id: selectedAgenda })
      .then((r) => setAppointments(Array.isArray(r.data) ? r.data : []))
      .catch(() => {});
  }, [selectedAgenda, weekStart]);

  const dayAppointments = (day) =>
    appointments.filter((a) => a.appointment_date === toISODate(day));

  return (
    <PageWrapper>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-gray-900">Calendario</h1>
        <div className="flex gap-2">
          <button
            className="px-3 py-1.5 rounded-lg border border-gray-300 text-sm hover:bg-gray-50"
            onClick={() => setWeekStart((d) => addDays(d, -7))}
          >
            &larr; Semana anterior
          </button>
          <button
            className="px-3 py-1.5 rounded-lg border border-gray-300 text-sm hover:bg-gray-50"
            onClick={() => setWeekStart((d) => addDays(d, 7))}
          >
            Semana siguiente &rarr;
          </button>
        </div>
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

      <div className="grid grid-cols-7 gap-2">
        {weekDays.map((day) => (
          <div key={day.toISOString()} className="bg-white rounded-xl border border-gray-200 p-3 min-h-32">
            <p className="text-xs font-semibold text-gray-500 uppercase mb-2">
              {format(day, 'EEE d', { locale: es })}
            </p>
            <div className="flex flex-col gap-1">
              {dayAppointments(day).map((a) => (
                <div key={a.id} className="text-xs bg-blue-50 rounded p-1 truncate">
                  <span className="font-medium">{formatTime(a.start_time)}</span> {a.client_name}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </PageWrapper>
  );
}
