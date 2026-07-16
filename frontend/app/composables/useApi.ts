export const useApi = () => {
  const config = useRuntimeConfig()

  const request = async <T>(url: string, options: any = {}): Promise<T> => {
    try {
      return await $fetch<T>(`${config.public.apiBase}${url}`, options)
    } catch (error: any) {
      throw error?.data || { detail: 'Unknown error' }
    }
  }

  return { request }
}