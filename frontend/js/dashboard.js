import { fetchCases, fetchDevices, fetchArtifacts } from './api.js'

window.addEventListener('load', async () => {
  const cardsEl = document.getElementById('cards')
  const cases = await fetchCases().catch(() => [])
  const devices = await fetchDevices().catch(() => ({ devices: [] }))
  const artifacts = await fetchArtifacts().catch(() => ({ sms: 0, calls: 0, locations: 0, applications: 0, social_media: 0 }))

  const cardHtml = `
    <div class="col-md-3">
      <div class="card card-dark p-3">
        <div class="card-title">TOTAL CASES</div>
        <div class="display-6">${Array.isArray(cases) ? cases.length : 0}</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card card-dark p-3">
        <div class="card-title">DEVICES</div>
        <div class="display-6">${Array.isArray(devices.devices) ? devices.devices.length : 0}</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card card-dark p-3">
        <div class="card-title">SMS RECORDS</div>
        <div class="display-6">${artifacts.sms || 0}</div>
      </div>
    </div>
    <div class="col-md-3">
      <div class="card card-dark p-3">
        <div class="card-title">AI FINDINGS</div>
        <div class="display-6">0</div>
      </div>
    </div>
  `
  cardsEl.innerHTML = cardHtml

  const evidenceCtx = document.getElementById('evidenceChart')
  if (evidenceCtx) {
    new Chart(evidenceCtx, {
      type: 'bar',
      data: {
        labels: ['SMS', 'Calls', 'Locations', 'Applications', 'Social'],
        datasets: [{ label: 'Artifact Distribution', data: [artifacts.sms, artifacts.calls, artifacts.locations, artifacts.applications, artifacts.social_media], backgroundColor: ['#3ec9ff', '#6ee7b7', '#fbbf24', '#c084fc', '#f472b6'] }]
      }
    })
  }

  const anomalyCtx = document.getElementById('anomalyChart')
  if (anomalyCtx) {
    new Chart(anomalyCtx, { type: 'doughnut', data: { labels: ['Potentially Unusual', 'Requires Review'], datasets: [{ data: [1, 1], backgroundColor: ['#38bdf8', '#f59e0b'] }] } })
  }
})
