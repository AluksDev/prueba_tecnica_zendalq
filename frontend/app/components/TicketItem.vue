<script setup lang="ts">
import type { Ticket, TicketStatus } from '~/models/ticket'
import { statusLabels, statusColors, priorityLabels } from '~/helpers/ticket'

const props = defineProps<{ ticket: Ticket }>()
const emit = defineEmits(['update'])

const { updateTicket } = useTickets()
const toast = useToast()

const loading = ref<boolean>(false)

const formatDate = (date: string): string => {
  const d = new Date(date)
  const day = String(d.getDate()).padStart(2, '0')
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const year = d.getFullYear()
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  return `${day}/${month}/${year} - ${hours}:${minutes}`
}

const changeStatus = async () => {
  loading.value = true
  try {
    const nextStatusMap: Record<TicketStatus, TicketStatus> = {
      open: 'in_progress',
      in_progress: 'closed',
      closed: 'in_progress',
    }

    const next = (nextStatusMap[props.ticket.status] || 'open') as TicketStatus

    await updateTicket(props.ticket.id, { status: next })
    toast.success('Estado actualizado')
    emit('update')
  } catch (e: any) {
    console.error('Error al actualizar el estado', e)
    toast.error(e.data?.detail || 'Error al actualizar el estado')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="ticket-card">
    <div class="ticket-header">
      <h3>{{ ticket.title }}</h3>
      <span class="ticket-status" :style="{ backgroundColor: statusColors[ticket.status], color: '#fff' }">{{ statusLabels[ticket.status] }}</span>
    </div>
    <p class="ticket-meta">{{ priorityLabels[ticket.priority] }} &middot; {{ formatDate(ticket.created_at) }}</p>
    <button
      class="btn-secondary"
      @click="changeStatus"
      :disabled="loading"
    >
      <span v-if="loading" class="spinner spinner--sm"></span>
      {{ loading ? 'Actualizando...' : 'Cambiar estado' }}
    </button>
  </div>
</template>

<style scoped>
.ticket-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing);
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.ticket-status {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 4px;
}

.ticket-meta {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.btn-secondary {
  background-color: var(--bg);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background-color: var(--border);
}
</style>
