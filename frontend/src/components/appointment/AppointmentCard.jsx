import { StatusBadge } from '../ui/Badge.jsx';
import { Button } from '../ui/Button.jsx';
import { formatTime } from '../../utils/formatters.js';

export function AppointmentCard({ appointment, onCancel, onComplete }) {
  const { client_name, client_phone, client_email, start_time, end_time, status, appointment_date } =
    appointment;

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm flex flex-col gap-2">
      <div className="flex items-start justify-between">
        <div>
          <p className="font-semibold text-gray-900">{client_name}</p>
          {client_phone && <p className="text-xs text-gray-500">{client_phone}</p>}
          {client_email && <p className="text-xs text-gray-500">{client_email}</p>}
        </div>
        <StatusBadge status={status} />
      </div>
      <p className="text-sm text-gray-600">
        {appointment_date} &mdash; {formatTime(start_time)} a {formatTime(end_time)}
      </p>
      {status === 'confirmed' && (
        <div className="flex gap-2 pt-1">
          <Button variant="secondary" className="text-xs py-1" onClick={() => onComplete(appointment.id)}>
            Completar
          </Button>
          <Button variant="danger" className="text-xs py-1" onClick={() => onCancel(appointment.id)}>
            Cancelar
          </Button>
        </div>
      )}
    </div>
  );
}
