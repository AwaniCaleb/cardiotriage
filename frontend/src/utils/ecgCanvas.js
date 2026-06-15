export function drawECG(canvas, isAfib) {
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width, h = canvas.height, mid = h * 0.55
  ctx.clearRect(0, 0, w, h)

  ctx.strokeStyle = 'rgba(34,211,238,0.07)'
  ctx.lineWidth = 0.5
  for (let x = 0; x < w; x += 50) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke() }
  for (let y = 0; y < h; y += 20) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke() }

  ctx.strokeStyle = '#22D3EE'
  ctx.lineWidth = 1.5
  ctx.beginPath()
  ctx.moveTo(0, mid)

  if (isAfib) {
    const beats = [0, 62, 116, 182, 258, 310, 376, 438, 502, 560, 624, 690]
    beats.forEach((bx) => {
      if (bx >= w) return
      for (let n = 0; n < 10; n++) ctx.lineTo(bx + n * 5, mid + (Math.random() - 0.5) * 5)
      if (bx + 22 < w) {
        ctx.lineTo(bx + 9, mid + 5)
        ctx.lineTo(bx + 13, mid - h * 0.5)
        ctx.lineTo(bx + 17, mid + 8)
        ctx.lineTo(bx + 22, mid)
      }
    })
  } else {
    const bw = 90
    for (let b = 0; b < w / bw + 1; b++) {
      const bx = b * bw
      ctx.lineTo(bx + 10, mid)
      ctx.quadraticCurveTo(bx + 15, mid - 8, bx + 20, mid)
      ctx.lineTo(bx + 25, mid + 5)
      ctx.lineTo(bx + 29, mid - h * 0.5)
      ctx.lineTo(bx + 33, mid + 8)
      ctx.lineTo(bx + 38, mid)
      ctx.quadraticCurveTo(bx + 50, mid - 14, bx + 60, mid)
      ctx.lineTo(bx + bw, mid)
    }
  }
  ctx.lineTo(w, mid)
  ctx.stroke()
}

export function drawPPG(canvas) {
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width, h = canvas.height, mid = h * 0.6
  ctx.clearRect(0, 0, w, h)

  ctx.strokeStyle = 'rgba(249,115,22,0.12)'
  ctx.lineWidth = 0.5
  for (let x = 0; x < w; x += 50) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke() }

  ctx.strokeStyle = '#F97316'
  ctx.lineWidth = 1.5
  ctx.beginPath()
  ctx.moveTo(0, mid)
  const bw = 68
  for (let b = 0; b < w / bw + 1; b++) {
    const bx = b * bw
    ctx.lineTo(bx + 8, mid)
    ctx.quadraticCurveTo(bx + 14, mid - h * 0.65, bx + 18, mid - h * 0.55)
    ctx.quadraticCurveTo(bx + 24, mid - h * 0.18, bx + 28, mid - h * 0.26)
    ctx.quadraticCurveTo(bx + 46, mid + h * 0.08, bx + bw, mid)
  }
  ctx.stroke()
}
