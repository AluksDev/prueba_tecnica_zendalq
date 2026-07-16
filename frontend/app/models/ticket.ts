export type TicketPriority = 'low' | 'medium' | 'high'

export type TicketStatus = 'open' | 'in_progress' | 'closed'

export interface Ticket {
  id: number
  title: string
  description: string | null
  priority: TicketPriority
  status: TicketStatus
  created_at: string
  updated_at: string
}

export interface TicketCreate {
  title: string
  description?: string
  priority?: TicketPriority
  status?: TicketStatus
}

export interface TicketUpdate {
  status?: TicketStatus
}

export interface TicketStats {
  status: TicketStatus
  total: number
}
