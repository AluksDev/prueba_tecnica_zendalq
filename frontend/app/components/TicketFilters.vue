<script setup lang="ts">
const model = defineModel<any>()
const emit = defineEmits(['change'])

watch(model, () => emit('change'), { deep: true })
</script>

<template>
  <div>
    <select v-model="model.status">
      <option value="">All status</option>
      <option value="open">Open</option>
      <option value="in_progress">In Progress</option>
      <option value="closed">Closed</option>
    </select>

    <select v-model="model.priority">
      <option value="">All priority</option>
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
    </select>
  </div>
</template>