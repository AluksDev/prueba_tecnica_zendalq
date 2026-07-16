// The raw ofetch error wrapper — only used inside useApi.ts
export interface FetchError {
  data?: ApiError
}

// The DRF error body — used by all components
export interface ApiError {
  detail?: string
  [field: string]: string[] | string | undefined
}
