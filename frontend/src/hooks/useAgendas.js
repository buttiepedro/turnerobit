import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as agendasApi from '../api/agendas';

export function useAgendas() {
  return useQuery({
    queryKey: ['agendas'],
    queryFn: () => agendasApi.listAgendas().then((r) => r.data),
  });
}

export function useCreateAgenda() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: agendasApi.createAgenda,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['agendas'] }),
  });
}

export function useUpdateAgenda() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => agendasApi.updateAgenda(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['agendas'] }),
  });
}
