import { useState } from 'react';
import { Input } from '../../components/ui/Input.jsx';
import { Button } from '../../components/ui/Button.jsx';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-sm">
        <h1 className="text-xl font-bold text-gray-900 mb-4">Recuperar contraseña</h1>
        {sent ? (
          <p className="text-sm text-green-700">Si el email existe, recibirás instrucciones.</p>
        ) : (
          <form
            onSubmit={(e) => { e.preventDefault(); setSent(true); }}
            className="flex flex-col gap-4"
          >
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Button type="submit" className="w-full">Enviar enlace</Button>
          </form>
        )}
      </div>
    </div>
  );
}
