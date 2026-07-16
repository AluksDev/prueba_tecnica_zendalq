<script setup lang="ts">
import type { Ticket } from '~/models/ticket'

defineProps<{ tickets: Ticket[] }>()
const emit = defineEmits(['update'])
</script>

<template>
  <div class="ticket-list">
    <TicketItem
      v-for="ticket in tickets"
      :key="ticket.id"
      :ticket="ticket"
      @update="emit('update')"
    />
  </div>
</template>

<style scoped>
.ticket-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
