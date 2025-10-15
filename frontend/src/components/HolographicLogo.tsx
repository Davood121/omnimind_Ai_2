import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

interface HolographicLogoProps {
  isActive: boolean
  isSpeaking?: boolean
  audioLevel?: number
}

// Real-time voice-reactive pulse
function useVoicePulse(isSpeaking: boolean) {
  const [pulse, setPulse] = useState(1)
  
  useEffect(() => {
    if (!isSpeaking) {
      setPulse(1)
      return
    }
    
    let frame: number
    const animate = () => {
      // Simulate voice waveform
      const time = Date.now() / 100
      const wave = Math.sin(time) * 0.3 + Math.sin(time * 2.3) * 0.2
      setPulse(1 + Math.abs(wave))
      frame = requestAnimationFrame(animate)
    }
    
    animate()
    return () => cancelAnimationFrame(frame)
  }, [isSpeaking])
  
  return pulse
}

export default function HolographicLogo({ isActive, isSpeaking = false }: HolographicLogoProps) {
  const pulse = useVoicePulse(isSpeaking)
  const size = 320

  return (
    <div className="relative" style={{ width: size, height: size }}>
      {/* Main Core Sphere */}
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{
          background: `radial-gradient(circle, 
            rgba(0, 217, 255, ${isSpeaking ? 0.4 * pulse : 0.2}) 0%, 
            rgba(181, 55, 242, ${isSpeaking ? 0.3 * pulse : 0.15}) 50%, 
            transparent 70%)`,
          boxShadow: isSpeaking 
            ? `0 0 ${60 * pulse}px rgba(0, 217, 255, ${0.8 * pulse}), inset 0 0 ${40 * pulse}px rgba(181, 55, 242, ${0.6 * pulse})`
            : '0 0 40px rgba(0, 217, 255, 0.5), inset 0 0 30px rgba(181, 55, 242, 0.4)'
        }}
        animate={{
          scale: isSpeaking ? pulse : isActive ? [1, 1.05, 1] : 1
        }}
        transition={{
          duration: 0.1
        }}
      />

      {/* Rotating Ring */}
      <motion.svg
        className="absolute inset-8"
        viewBox="0 0 100 100"
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
      >
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke="url(#ring1)"
          strokeWidth="1.5"
          strokeDasharray="10 5"
          opacity={isSpeaking ? 0.9 : 0.6}
        />
        <defs>
          <linearGradient id="ring1">
            <stop offset="0%" stopColor="#00d9ff" />
            <stop offset="100%" stopColor="#b537f2" />
          </linearGradient>
        </defs>
      </motion.svg>

      {/* Counter-Rotating Ring */}
      <motion.svg
        className="absolute inset-12"
        viewBox="0 0 100 100"
        animate={{ rotate: -360 }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
      >
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke="url(#ring2)"
          strokeWidth="1.5"
          strokeDasharray="5 10"
          opacity={isSpeaking ? 0.9 : 0.6}
        />
        <defs>
          <linearGradient id="ring2">
            <stop offset="0%" stopColor="#b537f2" />
            <stop offset="100%" stopColor="#ff006e" />
          </linearGradient>
        </defs>
      </motion.svg>

      {/* Center "O" Logo */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        animate={{
          scale: isSpeaking ? [pulse * 0.9, pulse * 1.1, pulse * 0.9] : isActive ? [1, 1.1, 1] : 1
        }}
        transition={{
          duration: isSpeaking ? 0.15 : 2,
          repeat: Infinity
        }}
      >
        <svg width="120" height="120" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="35"
            fill="none"
            stroke="url(#logo)"
            strokeWidth="3"
            opacity={isSpeaking ? 1 : 0.8}
          />
          <circle
            cx="50"
            cy="50"
            r="20"
            fill="none"
            stroke="url(#logo)"
            strokeWidth="2"
            opacity={isSpeaking ? 1 : 0.8}
          />
          <circle
            cx="50"
            cy="50"
            r="6"
            fill="url(#logo)"
            opacity={isSpeaking ? 1 : 0.9}
          />
          <defs>
            <linearGradient id="logo">
              <stop offset="0%" stopColor="#00d9ff" />
              <stop offset="50%" stopColor="#b537f2" />
              <stop offset="100%" stopColor="#ff006e" />
            </linearGradient>
          </defs>
        </svg>
      </motion.div>

      {/* Voice Waveform Bars - Only when speaking */}
      {isSpeaking && (
        <div className="absolute inset-0 flex items-center justify-center gap-1">
          {[...Array(8)].map((_, i) => (
            <motion.div
              key={i}
              className="w-1 bg-gradient-to-t from-cyber-blue to-cyber-purple rounded-full"
              animate={{
                height: [20, 60 * pulse, 20]
              }}
              transition={{
                duration: 0.3,
                repeat: Infinity,
                delay: i * 0.05
              }}
            />
          ))}
        </div>
      )}

      {/* Scan Lines */}
      {isSpeaking && (
        <motion.div
          className="absolute left-0 right-0 h-0.5"
          style={{
            background: `linear-gradient(90deg, transparent, rgba(0, 217, 255, ${pulse}), transparent)`,
            filter: 'blur(2px)'
          }}
          animate={{ top: [0, size, 0] }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
      )}
    </div>
  )
}