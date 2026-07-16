interface Toast {
  id: number
  message: string
  type: 'success' | 'error'
}

const toasts = ref<Toast[]>([])
let nextId = 0

export const useToast = () => {
  const show = (message: string, type: Toast['type']) => {
    const id = nextId++
    toasts.value.push({ id, message, type })

    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, 3000)
  }

  const success = (message: string) => show(message, 'success')
  const error = (message: string) => show(message, 'error')

  return { toasts, success, error }
}
