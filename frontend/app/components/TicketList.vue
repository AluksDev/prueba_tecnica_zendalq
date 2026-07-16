<script setup lang="ts">
import type { Ticket, TicketStatus } from '~/models/ticket';

defineProps<{ tickets: Ticket[] }>()
const emit = defineEmits(['update'])

const { updateTicket } = useTickets()

const loading = ref<boolean>(false)

const changeStatus = async (ticket: Ticket) => {
  loading.value = true
  try {
    const nextStatusMap: Record<TicketStatus, TicketStatus> = {
      open: 'in_progress',
      in_progress: 'closed',
      closed: 'in_progress',
    }

    const next = (nextStatusMap[ticket.status] || 'open') as TicketStatus

    await updateTicket(ticket.id, { status: next })
    emit('update')
  } catch (e: any) {
    alert(e.data?.detail || 'Error al actualizar el estado')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-for="t in tickets" :key="t.id">
    <h3>{{ t.title }}</h3>
    <p>{{ t.priority }} - {{ t.status }}</p>
    <small>{{ t.created_at }}</small>

    <button 
      @click="changeStatus(t)"
      :disabled="loading"
    >
      Cambiar estado
    </button>
  </div>
</template>