import type { Ticket, TicketCreate, TicketStats } from '~/models/ticket'

export const useTickets = () => {
  const { request } = useApi()

  const getTickets = (params: Record<string, string> = {}): Promise<Ticket[]> =>
    request('/tickets/', { query: params })

  const getStats = (): Promise<TicketStats[]> =>
    request('/tickets/stats/')

  const createTicket = (data: TicketCreate): Promise<Ticket> =>
    request('/tickets/', { method: 'POST', body: data })

  const updateTicket = (id: number, data: Partial<Ticket>): Promise<Ticket> =>
    request(`/tickets/${id}/`, { method: 'PATCH', body: data })

  return {
    getTickets,
    getStats,
    createTicket,
    updateTicket
  }
}