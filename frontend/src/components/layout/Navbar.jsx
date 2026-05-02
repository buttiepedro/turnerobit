import { useAuth } from '../../context/AuthContext.jsx';
import { Button } from '../ui/Button.jsx';

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <span className="font-semibold text-gray-900 text-lg">Sistema de Turnos</span>
      {user && (
        <div className="flex items-center gap-3 text-sm text-gray-600">
          <span>{user.role ?? user.type}</span>
          <Button variant="ghost" onClick={logout} className="text-sm">
            Cerrar sesión
          </Button>
        </div>
      )}
    </header>
  );
}
