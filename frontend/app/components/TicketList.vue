<script setup lang="ts">
import type { Ticket, TicketStatus } from '~/models/ticket';

defineProps<{ tickets: Ticket[] }>()
const emit = defineEmits(['update'])

const { updateTicket } = useTickets()

const changeStatus = async (ticket: Ticket) => {
  try {
    const nextStatusMap: Record<TicketStatus, TicketStatus> = {
      open: 'in_progress',
      in_progress: 'closed',
      closed: 'open',
    }

    const next = (nextStatusMap[ticket.status] || 'open') as TicketStatus

    await updateTicket(ticket.id, { status: next })
    emit('update')
  } catch (e: any) {
    alert(e.data?.detail || 'Error al actualizar el estado')
  }
}
</script>

<template>
  <div v-for="t in tickets" :key="t.id">
    <h3>{{ t.title }}</h3>
    <p>{{ t.priority }} - {{ t.status }}</p>
    <small>{{ t.created_at }}</small>

    <button @click="changeStatus(t)">
      Cambiar estado
    </button>
  </div>
</template>