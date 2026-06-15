export function initials(name) {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

export function severityBadgeClass(severity) {
  switch (severity) {
    case 'RED': return 'badge-red'
    case 'YELLOW': return 'badge-yellow'
    case 'GREEN': return 'badge-green'
    default: return 'badge-none'
  }
}

export function rhythmDescription(rhythmLabel) {
  switch (rhythmLabel) {
    case 'AFib': return 'AFib detected'
    case 'Tachycardia': return 'Tachycardia'
    case 'Bradycardia': return 'Bradycardia'
    case 'Anomaly': return 'Anomaly detected'
    case 'Normal': return 'Normal sinus'
    default: return 'No result'
  }
}

export function avatarColors(severity) {
  switch (severity) {
    case 'RED': return { background: '#0C2340', color: '#22D3EE' }
    case 'YELLOW': return { background: '#2D1B00', color: '#FCD34D' }
    case 'GREEN': return { background: '#052E16', color: '#86EFAC' }
    default: return { background: 'var(--bd)', color: 'var(--tm)' }
  }
}

export function formatRelativeTime(dateStr) {
  if (!dateStr) return ''
  const diffSec = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000)
  if (diffSec < 60) return 'Just now'
  const diffMin = Math.floor(diffSec / 60)
  if (diffMin < 60) return `${diffMin}m ago`
  const diffHr = Math.floor(diffMin / 60)
  if (diffHr < 24) return `${diffHr}h ago`
  const diffDay = Math.floor(diffHr / 24)
  if (diffDay === 1) return '1 day ago'
  if (diffDay < 7) return `${diffDay} days ago`
  const diffWeek = Math.floor(diffDay / 7)
  if (diffWeek === 1) return '1 week ago'
  return `${diffWeek} weeks ago`
}

export function formatRecordingDate(dateStr) {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  const now = new Date()
  const time = date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })
  const startOfDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate())
  const diffDays = Math.round((startOfDay(now) - startOfDay(date)) / 86400000)
  if (diffDays === 0) return `Today at ${time}`
  if (diffDays === 1) return `Yesterday ${time}`
  if (diffDays > 1 && diffDays < 7) return `${diffDays} days ago ${time}`
  return `${date.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })} ${time}`
}

export function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })
}
