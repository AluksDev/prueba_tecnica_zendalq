<script setup lang="ts">
const { toasts } = useToast()
</script>

<template>
  <div class="toast-container">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="toast"
      :class="`toast--${toast.type}`"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 1000;
}

.toast {
  padding: 12px 20px;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  color: #ffffff;
}

.toast--success {
  background-color: var(--success);
}

.toast--error {
  background-color: var(--danger);
}
</style>
