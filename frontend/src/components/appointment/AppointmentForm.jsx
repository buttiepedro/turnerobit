import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Input } from '../ui/Input.jsx';
import { Button } from '../ui/Button.jsx';

const schema = z.object({
  client_name: z.string().min(2, 'Nombre requerido'),
  client_email: z.string().email('Email inválido').optional().or(z.literal('')),
  client_phone: z.string().optional(),
  notes: z.string().optional(),
});

export function AppointmentForm({ slot, agendaId, appointmentDate, onSubmit, onCancel }) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(schema),
  });

  const submit = handleSubmit(async (values) => {
    await onSubmit({
      agenda_id: agendaId,
      appointment_date: appointmentDate,
      start_time: slot.start_time,
      ...values,
    });
  });

  return (
    <form onSubmit={submit} className="flex flex-col gap-4">
      <p className="text-sm text-gray-600">
        Turno: <strong>{slot.start_time}</strong> &mdash; <strong>{slot.end_time}</strong>
      </p>
      <Input label="Nombre del cliente" error={errors.client_name?.message} {...register('client_name')} />
      <Input label="Email" type="email" error={errors.client_email?.message} {...register('client_email')} />
      <Input label="Teléfono" type="tel" {...register('client_phone')} />
      <Input label="Notas internas" {...register('notes')} />
      <div className="flex gap-2 justify-end">
        <Button variant="ghost" type="button" onClick={onCancel}>Cancelar</Button>
        <Button type="submit" disabled={isSubmitting}>Confirmar turno</Button>
      </div>
    </form>
  );
}
