import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

export const formatDate = (dateStr) =>
  format(parseISO(dateStr), "d 'de' MMMM yyyy", { locale: es });

export const formatDateShort = (dateStr) =>
  format(parseISO(dateStr), 'dd/MM/yyyy');

export const toISODate = (date) => format(date, 'yyyy-MM-dd');

export const todayISO = () => format(new Date(), 'yyyy-MM-dd');
