<script setup lang="ts">
import type { TicketPriority, TicketStatus } from '~/models/ticket'
import type { ApiError } from '~/models/error'

const emit = defineEmits(['created'])
const { createTicket } = useTickets()
const toast = useToast()

const title = ref<string>('')
const description = ref<string>('')
const priority = ref<TicketPriority>('low')
const status = ref<TicketStatus>('open')
const loading = ref<boolean>(false)

const submit = async () => {
  if (!title.value.trim()) {
    toast.error('El título es obligatorio')
    return
  }

  loading.value = true
  try {
    await createTicket({
      title: title.value,
      description: description.value || undefined,
      priority: priority.value,
      status: status.value
    })

    title.value = ''
    description.value = ''
    priority.value = 'low'
    status.value = 'open'
    toast.success('Ticket creado')
    emit('created')
  } catch (e) {
    const error = e as ApiError
    console.error('Error al crear el ticket', error)
    toast.error(error.detail || 'Error al crear el ticket')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="ticket-form" @submit.prevent="submit">
    <input v-model="title" placeholder="Título" :disabled="loading" />
    <textarea v-model="description" placeholder="Descripción" :disabled="loading" />
    <div class="row">
      <select v-model="priority" :disabled="loading">
        <option value="low">Baja</option>
        <option value="medium">Media</option>
        <option value="high">Alta</option>
      </select>
      <select v-model="status" :disabled="loading">
        <option value="open">Abierto</option>
        <option value="in_progress">En progreso</option>
      </select>
    </div>
    <button type="submit" :disabled="loading">
      <span v-if="loading" class="spinner spinner--sm"></span>
      {{ loading ? 'Creando...' : 'Crear' }}
    </button>
  </form>
</template>

<style scoped>
.ticket-form {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing);
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: var(--spacing);
}

.row {
  display: flex;
  gap: 12px;
}

.row select {
  flex: 1;
}

.ticket-form button {
  align-self: flex-start;
}
</style>
