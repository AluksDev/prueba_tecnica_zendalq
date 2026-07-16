<script setup lang="ts">
import { statusOptions, priorityOptions } from '~/helpers/ticket'

interface TicketFilterModel {
  status: string
  priority: string
}

const model = defineModel<TicketFilterModel>({ default: () => ({ status: '', priority: '' }) })
const props = defineProps<{ disabled?: boolean }>()
const emit = defineEmits(['change'])

watch(model, () => emit('change'), { deep: true })
</script>

<template>
  <div class="filters">
    <select v-model="model.status" :disabled="disabled">
      <option value="">Todos los estados</option>
      <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>

    <select v-model="model.priority" :disabled="disabled">
      <option value="">Todas las prioridades</option>
      <option v-for="opt in priorityOptions" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.filters {
  display: flex;
  gap: 12px;
  margin-bottom: var(--spacing);
}

.filters select {
  flex: 1;
}
</style>