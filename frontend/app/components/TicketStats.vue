<script setup lang="ts">
import type { TicketStats, TicketStatus } from '~/models/ticket'
import { statusLabels, statusColors } from '~/helpers/ticket'

defineProps<{ stats: TicketStats[]; loading?: boolean }>()

const getCount = (stats: TicketStats[], status: TicketStatus): number => {
  return stats.find(s => s.status === status)?.total ?? 0
}
</script>

<template>
  <div class="stats-row">
    <template v-if="loading">
      <div v-for="i in 3" :key="i" class="stat-card stat-card--loading">
        <span class="spinner"></span>
      </div>
    </template>
    <template v-else>
    <div
      v-for="status in (['open', 'in_progress', 'closed'] as TicketStatus[])"
      :key="status"
      class="stat-card"
    >
      <span class="stat-value" :style="{ color: statusColors[status] }">
        {{ getCount(stats, status) }}
      </span>
      <span class="stat-label">{{ statusLabels[status] }}</span>
    </div>
    </template>
  </div>
</template>

<style scoped>
.stats-row {
  display: flex;
  gap: 12px;
  margin-bottom: var(--spacing);
}

.stat-card {
  flex: 1;
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing);
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
}
</style>
