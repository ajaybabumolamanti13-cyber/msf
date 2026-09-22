const API_BASE = (typeof window !== 'undefined' && window.location.protocol.startsWith('http') && window.location.hostname !== '127.0.0.1' && window.location.hostname !== 'localhost')
  ? (window.location.hostname.includes('vercel.app') ? 'https://msf-1-9fse.onrender.com/api' : `${window.location.origin}/api`)
  : 'http://127.0.0.1:8000/api'

export async function fetchCases(){
  const res = await fetch(`${API_BASE}/cases/`)
  return res.json()
}

export async function fetchDevices(){
  const res = await fetch(`${API_BASE}/devices/scan`)
  return res.json()
}

export async function fetchArtifacts(){
  const res = await fetch(`${API_BASE}/artifacts/summary`)
  return res.json()
}
