const colors = {
  confirmed: 'bg-green-100 text-green-800',
  pending: 'bg-yellow-100 text-yellow-800',
  cancelled: 'bg-red-100 text-red-800',
  completed: 'bg-blue-100 text-blue-800',
  no_show: 'bg-gray-100 text-gray-800',
};

const labels = {
  confirmed: 'Confirmado',
  pending: 'Pendiente',
  cancelled: 'Cancelado',
  completed: 'Completado',
  no_show: 'Ausente',
};

export function StatusBadge({ status }) {
  return (
    <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
      {labels[status] || status}
    </span>
  );
}
