import { useCallback, useState } from 'react';
import * as appointmentsApi from '../api/appointments';

export function useAppointments(agendaId) {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAppointments = useCallback(
    async (filters = {}) => {
      setLoading(true);
      setError(null);
      try {
        const { data } = await appointmentsApi.list({ agenda_id: agendaId, ...filters });
        setAppointments(Array.isArray(data) ? data : data.items ?? []);
      } catch (e) {
        setError(e.response?.data?.detail || 'Error al cargar turnos');
      } finally {
        setLoading(false);
      }
    },
    [agendaId]
  );

  const createAppointment = useCallback(async (payload) => {
    const { data } = await appointmentsApi.create(payload);
    setAppointments((prev) => [...prev, data]);
    return data;
  }, []);

  const cancelAppointment = useCallback(async (id, reason) => {
    const { data } = await appointmentsApi.cancel(id, reason);
    setAppointments((prev) => prev.map((a) => (a.id === id ? data : a)));
    return data;
  }, []);

  const completeAppointment = useCallback(async (id) => {
    const { data } = await appointmentsApi.complete(id);
    setAppointments((prev) => prev.map((a) => (a.id === id ? data : a)));
    return data;
  }, []);

  return {
    appointments,
    loading,
    error,
    fetchAppointments,
    createAppointment,
    cancelAppointment,
    completeAppointment,
  };
}
