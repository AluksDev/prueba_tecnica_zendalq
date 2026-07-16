<script setup lang="ts">
import type { TicketPriority, TicketStatus } from '~/models/ticket'

const emit = defineEmits(['created'])
const { createTicket } = useTickets()

const title = ref<string>('')
const description = ref<string>('')
const priority = ref<TicketPriority>('low')
const status = ref<TicketStatus>('open')
const error = ref<string | null>(null)

const submit = async () => {
  error.value = null

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
    emit('created')
  } catch (e: any) {
    error.value = e.data || 'Error al crear el ticket'
  }
}
</script>

<template>
  <div>
    <input v-model="title" placeholder="Título" />
    <textarea v-model="description" placeholder="Descripción" />
    <select v-model="priority">
      <option value="low">Baja</option>
      <option value="medium">Media</option>
      <option value="high">Alta</option>
    </select>
    <select v-model="status">
      <option value="open">Abierto</option>
      <option value="in_progress">En progreso</option>
    </select>

    <button @click="submit">Crear</button>

    <div v-if="error">{{ error }}</div>
  </div>
</template>