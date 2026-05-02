import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

export function RoleRoute({ allowedRoles, children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  const userRole = user.role ?? user.type;
  if (!allowedRoles.includes(userRole)) return <Navigate to="/unauthorized" replace />;
  return children;
}
