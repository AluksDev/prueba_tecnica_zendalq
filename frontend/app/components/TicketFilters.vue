<script setup lang="ts">
const model = defineModel<any>()
const props = defineProps<{ disabled?: boolean }>()
const emit = defineEmits(['change'])

watch(model, () => emit('change'), { deep: true })
</script>

<template>
  <div class="filters">
    <select v-model="model.status" :disabled="disabled">
      <option value="">Todos los estados</option>
      <option value="open">Abierto</option>
      <option value="in_progress">En progreso</option>
      <option value="closed">Cerrado</option>
    </select>

    <select v-model="model.priority" :disabled="disabled">
      <option value="">Todas las prioridades</option>
      <option value="low">Baja</option>
      <option value="medium">Media</option>
      <option value="high">Alta</option>
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