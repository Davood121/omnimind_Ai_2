import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

interface SpeechWaveformProps {
  isActive: boolean
  audioLevel: number
}

export default function SpeechWaveform({ isActive, audioLevel }: SpeechWaveformProps) {
  const [bars, setBars] = useState(30)

  useEffect(() => {
    const updateBars = () => {
      const width = window.innerWidth
      if (width < 640) {
        setBars(15)
      } else if (width < 1024) {
        setBars(20)
      } else {
        setBars(30)
      }
    }

    updateBars()
    window.addEventListener('resize', updateBars)
    return () => window.removeEventListener('resize', updateBars)
  }, [])

  return (
    <div className="flex items-center justify-center gap-0.5 sm:gap-1 h-16 sm:h-20 lg:h-24">
      {[...Array(bars)].map((_, i) => {
        // Create wave pattern
        const centerDistance = Math.abs(i - bars / 2) / (bars / 2)
        const baseHeight = 20 + (1 - centerDistance) * 20
        const audioHeight = audioLevel * 60
        
        return (
          <motion.div
            key={i}
            className="w-1 sm:w-1.5 rounded-full"
            style={{
              background: `linear-gradient(to top, 
                rgba(0, 217, 255, ${0.8 + audioLevel * 0.2}), 
                rgba(181, 55, 242, ${0.6 + audioLevel * 0.4})
              )`,
              boxShadow: `0 0 ${10 + audioLevel * 20}px rgba(0, 217, 255, ${0.5 + audioLevel * 0.5})`
            }}
            animate={{
              height: isActive 
                ? [baseHeight, baseHeight + audioHeight * (1 - centerDistance), baseHeight]
                : baseHeight
            }}
            transition={{
              duration: 0.15,
              repeat: Infinity,
              delay: i * 0.02,
              ease: "easeInOut"
            }}
          />
        )
      })}
    </div>
  )
}