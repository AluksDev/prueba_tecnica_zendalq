<script setup lang="ts">
import type { Ticket } from '~/models/ticket'

const { getTickets, createTicket, updateTicket } = useTickets()

const tickets = ref<Ticket[]>([])
const loading = ref<boolean>(false)
const error = ref<string | null>(null)

const filters = ref({
  status: '',
  priority: ''
})

const fetchTickets = async () => {
  loading.value = true
  error.value = null

  try {
    const params: Record<string, string> = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.priority) params.priority = filters.value.priority
    tickets.value = await getTickets(params)
  } catch (e: any) {
    error.value = e.data || 'Error al cargar los tickets'
  } finally {
    loading.value = false
  }
}

onMounted(fetchTickets)
</script>

<template>
  <div>
    <h1>Tickets</h1>

    <TicketFilters v-model="filters" @change="fetchTickets" />
    
    <TicketForm @created="fetchTickets" /> 

    <div v-if="loading">Cargando...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="tickets.length === 0">No hay tickets</div>

    <TicketList
      v-else
      :tickets="tickets"
      @update="fetchTickets"
    />
  </div>
</template>
