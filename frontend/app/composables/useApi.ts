import type { FetchError } from '~/models/error'

export const useApi = () => {
  const config = useRuntimeConfig()

  const request = async <T>(url: string, options: Record<string, unknown> = {}): Promise<T> => {
    try {
      return await $fetch<T>(`${config.public.apiBase}${url}`, options)
    } catch (error) {
      const fetchError = error as FetchError
      throw fetchError?.data || { detail: 'Error desconocido' }
    }
  }

  return { request }
}