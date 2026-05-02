import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';

const links = {
  superadmin: [
    { to: '/superadmin/tenants', label: 'Tenants' },
  ],
  admin_empresa: [
    { to: '/admin/dashboard', label: 'Dashboard' },
    { to: '/admin/agendas', label: 'Agendas' },
    { to: '/admin/users', label: 'Usuarios' },
  ],
  usuario_agenda: [
    { to: '/agenda/calendar', label: 'Calendario' },
    { to: '/agenda/schedule', label: 'Horarios' },
    { to: '/agenda/appointments', label: 'Turnos' },
  ],
};

export function Sidebar() {
  const { user } = useAuth();
  const role = user?.role ?? user?.type;
  const items = links[role] ?? [];

  return (
    <aside className="w-56 bg-gray-900 text-white flex flex-col py-6 px-4 gap-1 min-h-screen">
      {items.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive ? 'bg-blue-600' : 'hover:bg-gray-700'
            }`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
}
