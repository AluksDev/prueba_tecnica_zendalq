import type { TicketStatus, TicketPriority } from '~/models/ticket'

export const statusLabels: Record<TicketStatus, string> = {
  open: 'Abierto',
  in_progress: 'En progreso',
  closed: 'Cerrado',
}

export const statusColors: Record<TicketStatus, string> = {
  open: 'var(--primary)',
  in_progress: '#f59e0b',
  closed: 'var(--success)',
}

export const priorityLabels: Record<TicketPriority, string> = {
  low: 'Baja',
  medium: 'Media',
  high: 'Alta',
}
