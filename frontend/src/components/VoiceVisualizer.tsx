import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

interface VoiceVisualizerProps {
  isActive: boolean
}

export default function VoiceVisualizer({ isActive }: VoiceVisualizerProps) {
  const [bars, setBars] = useState(20)

  useEffect(() => {
    const updateBars = () => {
      const width = window.innerWidth
      if (width < 640) {
        setBars(10)
      } else if (width < 1024) {
        setBars(15)
      } else {
        setBars(20)
      }
    }

    updateBars()
    window.addEventListener('resize', updateBars)
    return () => window.removeEventListener('resize', updateBars)
  }, [])

  return (
    <div className="flex items-center justify-center gap-0.5 sm:gap-1 h-12 sm:h-16 lg:h-20">
      {[...Array(bars)].map((_, i) => (
        <motion.div
          key={i}
          className="w-1 sm:w-2 bg-gradient-to-t from-cyber-blue to-cyber-purple rounded-full"
          animate={{
            height: isActive 
              ? [20, Math.random() * 40 + 20, 20]
              : 20
          }}
          transition={{
            duration: 0.5,
            repeat: Infinity,
            delay: i * 0.05,
            ease: "easeInOut"
          }}
          style={{
            boxShadow: '0 0 10px rgba(0, 217, 255, 0.5)'
          }}
        />
      ))}
    </div>
  )
}