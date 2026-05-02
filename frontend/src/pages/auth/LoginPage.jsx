import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import { Input } from '../../components/ui/Input.jsx';
import { Button } from '../../components/ui/Button.jsx';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(username, password);
      const role = user.role ?? user.type;
      if (role === 'superadmin') navigate('/superadmin/tenants');
      else if (role === 'admin_empresa') navigate('/admin/dashboard');
      else navigate('/agenda/calendar');
    } catch (err) {
      setError(err.response?.data?.detail || 'Credenciales inválidas');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-sm">
        <h1 className="text-2xl font-bold text-gray-900 mb-6 text-center">Sistema de Turnos</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input
            label="Usuario"
            placeholder="email@empresa.com o tenant:email"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
          <Input
            label="Contraseña"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" disabled={loading} className="w-full mt-2">
            {loading ? 'Ingresando...' : 'Ingresar'}
          </Button>
        </form>
        <p className="text-xs text-gray-400 mt-4 text-center">
          Superadmin: <code>admin@sistema.com</code> | Tenant: <code>demo:email</code>
        </p>
      </div>
    </div>
  );
}
