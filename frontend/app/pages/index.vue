<script setup lang="ts">
import type { Ticket, TicketStats } from '~/models/ticket'
import type { ApiError } from '~/models/error'

const { getTickets, getStats } = useTickets()
const toast = useToast()

const tickets = ref<Ticket[]>([])
const stats = ref<TicketStats[]>([])
const loading = ref<boolean>(false)
const loadingStats = ref<boolean>(false)

const filters = ref({
  status: '',
  priority: ''
})

const fetchTickets = async () => {
  loading.value = true

  try {
    const params: Record<string, string> = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.priority) params.priority = filters.value.priority
    tickets.value = await getTickets(params)
  } catch (e) {
    const error = e as ApiError
    console.error('Error al cargar los tickets', error)
    toast.error('Error al cargar los tickets')
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  loadingStats.value = true
  try {
    stats.value = await getStats()
  } catch (e) {
    const error = e as ApiError
    console.error('Error al cargar las estadísticas', error)
    toast.error('Error al cargar las estadísticas')
  } finally {
    loadingStats.value = false
  }
}

const refresh = () => {
  fetchTickets()
  fetchStats()
}

onMounted(refresh)
</script>

<template>
  <div class="page">
    <h1>Tickets</h1>

    <TicketStats :stats="stats" :loading="loadingStats" />

    <div class="layout">
      <div class="main">
        <TicketFilters v-model="filters" :disabled="loading" @change="refresh" />

        <div v-if="loading" class="state">
          <span class="spinner"></span> Cargando...
        </div>
        <div v-else-if="tickets.length === 0" class="state">No hay tickets</div>

        <TicketList
          v-else
          :tickets="tickets"
          @update="refresh"
        />
      </div>

      <aside class="sidebar">
        <TicketForm @created="refresh" />
      </aside>
    </div>
  </div>
</template>

<style scoped>
.page h1 {
  margin-bottom: var(--spacing);
}

.layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.main {
  flex: 1;
  min-width: 0;
}

.sidebar {
  width: 320px;
  flex-shrink: 0;
  position: sticky;
  top: 32px;
}

.state {
  text-align: center;
  color: var(--text-secondary);
  padding: 32px 0;
}
</style>
