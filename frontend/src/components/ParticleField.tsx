import { useEffect, useRef } from 'react'

interface ParticleFieldProps {
  isSpeaking?: boolean
  audioLevel?: number
}

export default function ParticleField({ isSpeaking = false, audioLevel = 0 }: ParticleFieldProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const particles: Array<{
      x: number
      y: number
      vx: number
      vy: number
      size: number
      color: string
    }> = []

    const colors = ['#00d9ff', '#b537f2', '#ff006e', '#00ff88']

    // Create particles - adjust count based on device
    const particleCount = window.innerWidth < 768 ? 50 : 100
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 1,
        color: colors[Math.floor(Math.random() * colors.length)]
      })
    }

    function animate() {
      if (!ctx || !canvas) return
      
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      particles.forEach((particle, i) => {
        // Add speech-reactive movement
        const speedMultiplier = isSpeaking ? 1 + audioLevel * 2 : 1
        particle.x += particle.vx * speedMultiplier
        particle.y += particle.vy * speedMultiplier

        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1

        // Speech-reactive size
        const sizeMultiplier = isSpeaking ? 1 + audioLevel * 0.5 : 1
        const currentSize = particle.size * sizeMultiplier

        ctx.beginPath()
        ctx.arc(particle.x, particle.y, currentSize, 0, Math.PI * 2)
        
        // Speech-reactive glow
        if (isSpeaking) {
          const gradient = ctx.createRadialGradient(
            particle.x, particle.y, 0,
            particle.x, particle.y, currentSize * 2
          )
          gradient.addColorStop(0, particle.color)
          gradient.addColorStop(1, 'transparent')
          ctx.fillStyle = gradient
        } else {
          ctx.fillStyle = particle.color
        }
        ctx.fill()

        // Draw connections
        particles.slice(i + 1).forEach(otherParticle => {
          const dx = particle.x - otherParticle.x
          const dy = particle.y - otherParticle.y
          const distance = Math.sqrt(dx * dx + dy * dy)

          const maxDistance = isSpeaking ? 150 + audioLevel * 100 : 150
          if (distance < maxDistance) {
            ctx.beginPath()
            ctx.moveTo(particle.x, particle.y)
            ctx.lineTo(otherParticle.x, otherParticle.y)
            
            const opacity = isSpeaking 
              ? (0.2 + audioLevel * 0.3) * (1 - distance / maxDistance)
              : 0.2 * (1 - distance / maxDistance)
            
            ctx.strokeStyle = `rgba(0, 217, 255, ${opacity})`
            ctx.lineWidth = isSpeaking ? 1 : 0.5
            ctx.stroke()
          }
        })
      })

      requestAnimationFrame(animate)
    }

    animate()

    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none" />
}