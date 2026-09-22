// Live Render backend URL
const API_BASE = window.MFIS_API_BASE || 'https://msf-1-9fse.onrender.com/api'

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
