// Update this to your Render backend URL after deployment
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function predict(endpoint, data) {
  const res = await fetch(`${BASE_URL}/predict/${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}
