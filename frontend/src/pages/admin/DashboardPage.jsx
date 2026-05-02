import { useEffect, useState } from 'react';
import { listAgendas } from '../../api/agendas.js';
import { PageWrapper } from '../../components/layout/PageWrapper.jsx';

export default function DashboardPage() {
  const [agendas, setAgendas] = useState([]);

  useEffect(() => {
    listAgendas().then((r) => setAgendas(r.data)).catch(() => {});
  }, []);

  return (
    <PageWrapper>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-sm text-gray-500">Agendas activas</p>
          <p className="text-3xl font-bold text-blue-600 mt-1">
            {agendas.filter((a) => a.is_active).length}
          </p>
        </div>
      </div>
    </PageWrapper>
  );
}
