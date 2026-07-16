<script setup lang="ts">
import type { Ticket, TicketStatus } from '~/models/ticket'
import { statusLabels, statusColors, priorityLabels } from '~/helpers/ticket'

const props = defineProps<{ ticket: Ticket }>()
const emit = defineEmits(['update'])

const { updateTicket } = useTickets()
const toast = useToast()

const loading = ref<boolean>(false)
const localStatus = ref<TicketStatus>(props.ticket.status)

watch(() => props.ticket.status, (newStatus) => {
  localStatus.value = newStatus
})

const formatDate = (date: string): string => {
  const d = new Date(date)
  const day = String(d.getDate()).padStart(2, '0')
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const year = d.getFullYear()
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  return `${day}/${month}/${year} - ${hours}:${minutes}`
}

const changeStatus = async (e: Event) => {
  const newStatus = (e.target as HTMLSelectElement).value as TicketStatus
  const previousStatus = props.ticket.status

  loading.value = true
  try {
    await updateTicket(props.ticket.id, { status: newStatus })
    toast.success('Estado actualizado')
    emit('update')
  } catch (e: any) {
    console.error('Error al cambiar el estado', e)
    toast.error(e.status?.[0] || 'Error al cambiar el estado')
    localStatus.value = previousStatus
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
    <select v-model="localStatus" @change="changeStatus" :disabled="loading">
      <option v-for="(label, value) in statusLabels" :key="value" :value="value">
        {{ label }}
      </option>
    </select>
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


</style>
