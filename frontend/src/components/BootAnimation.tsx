import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Terminal, Cpu, Database, Zap, Activity, Code, CheckCircle } from 'lucide-react'

interface BootAnimationProps {
  onComplete: () => void
}

interface BootStep {
  id: string
  icon: typeof Terminal
  label: string
  duration: number
}

const bootSteps: BootStep[] = [
  { id: 'bios', icon: Cpu, label: 'INITIALIZING BIOS', duration: 800 },
  { id: 'kernel', icon: Terminal, label: 'LOADING KERNEL', duration: 600 },
  { id: 'neural', icon: Activity, label: 'ACTIVATING NEURAL NETWORK', duration: 900 },
  { id: 'database', icon: Database, label: 'CONNECTING TO DATABASE', duration: 700 },
  { id: 'ai', icon: Zap, label: 'INITIALIZING AI CORE', duration: 1000 },
  { id: 'systems', icon: Code, label: 'LOADING SYSTEM MODULES', duration: 800 },
]

// Matrix rain effect component
function MatrixRain() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const chars = '01アイウエオカキクケコサシスセソタチツテト'
    const fontSize = 14
    const columns = canvas.width / fontSize
    const drops: number[] = []

    for (let i = 0; i < columns; i++) {
      drops[i] = Math.random() * -100
    }

    function draw() {
      if (!ctx || !canvas) return
      
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = '#00d9ff'
      ctx.font = `${fontSize}px monospace`

      for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)]
        ctx.fillText(text, i * fontSize, drops[i] * fontSize)

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0
        }
        drops[i]++
      }
    }

    const interval = setInterval(draw, 50)
    return () => clearInterval(interval)
  }, [])

  return <canvas ref={canvasRef} className="absolute inset-0 opacity-10" />
}

// Glitch text effect component
function GlitchText({ text, className = '' }: { text: string; className?: string }) {
  return (
    <div className={`relative ${className}`}>
      <span className="relative z-10">{text}</span>
      <motion.span
        className="absolute inset-0 text-cyber-blue"
        animate={{
          x: [-2, 2, -2],
          opacity: [0, 0.5, 0],
        }}
        transition={{
          duration: 0.2,
          repeat: Infinity,
          repeatDelay: 2,
        }}
      >
        {text}
      </motion.span>
      <motion.span
        className="absolute inset-0 text-cyber-pink"
        animate={{
          x: [2, -2, 2],
          opacity: [0, 0.5, 0],
        }}
        transition={{
          duration: 0.2,
          repeat: Infinity,
          repeatDelay: 2,
          delay: 0.1,
        }}
      >
        {text}
      </motion.span>
    </div>
  )
}

// Holographic scan lines
function ScanLines() {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      <motion.div
        className="absolute inset-0"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, rgba(0, 217, 255, 0.03) 0px, transparent 2px, transparent 4px)',
        }}
        animate={{
          y: [0, 4, 0],
        }}
        transition={{
          duration: 0.1,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
    </div>
  )
}

export default function BootAnimation({ onComplete }: BootAnimationProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  const [isComplete, setIsComplete] = useState(false)
  const [showGlitch, setShowGlitch] = useState(false)

  // Enhanced Web Audio API for generating tech sounds
  const playBootSound = (frequency: number, duration: number, type: 'beep' | 'sweep' | 'pulse' | 'startup' = 'beep') => {
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      const filter = audioContext.createBiquadFilter()

      oscillator.connect(filter)
      filter.connect(gainNode)
      gainNode.connect(audioContext.destination)

      filter.type = 'lowpass'
      filter.frequency.value = frequency * 2

      if (type === 'startup') {
        // Complex startup sound
        oscillator.frequency.setValueAtTime(frequency * 0.5, audioContext.currentTime)
        oscillator.frequency.exponentialRampToValueAtTime(frequency * 2, audioContext.currentTime + duration / 2000)
        oscillator.frequency.exponentialRampToValueAtTime(frequency, audioContext.currentTime + duration / 1000)
        oscillator.type = 'sawtooth'
      } else if (type === 'sweep') {
        oscillator.frequency.exponentialRampToValueAtTime(frequency * 2, audioContext.currentTime + duration / 1000)
        oscillator.type = 'sine'
      } else if (type === 'pulse') {
        oscillator.type = 'square'
        oscillator.frequency.value = frequency
      } else {
        oscillator.type = 'sine'
        oscillator.frequency.value = frequency
      }

      gainNode.gain.setValueAtTime(0.15, audioContext.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration / 1000)

      oscillator.start(audioContext.currentTime)
      oscillator.stop(audioContext.currentTime + duration / 1000)
    } catch (error) {
      console.log('Audio not available:', error)
    }
  }

  // Glitch effect trigger
  useEffect(() => {
    const glitchInterval = setInterval(() => {
      if (Math.random() > 0.7) {
        setShowGlitch(true)
        setTimeout(() => setShowGlitch(false), 100)
      }
    }, 3000)

    return () => clearInterval(glitchInterval)
  }, [])

  useEffect(() => {
    // Play enhanced startup sound
    playBootSound(400, 800, 'startup')
    
    const totalDuration = bootSteps.reduce((sum, step) => sum + step.duration, 0)
    let elapsed = 0

    const interval = setInterval(() => {
      elapsed += 50
      const newProgress = Math.min((elapsed / totalDuration) * 100, 100)
      setProgress(newProgress)

      // Update current step
      let cumulativeDuration = 0
      for (let i = 0; i < bootSteps.length; i++) {
        cumulativeDuration += bootSteps[i].duration
        if (elapsed < cumulativeDuration) {
          if (currentStep !== i) {
            setCurrentStep(i)
            // Play different sounds for different steps
            const frequencies = [600, 700, 800, 900, 1000, 1100]
            const soundTypes: Array<'beep' | 'pulse' | 'sweep'> = ['beep', 'pulse', 'sweep', 'beep', 'pulse', 'sweep']
            playBootSound(frequencies[i], 150, soundTypes[i])
          }
          break
        }
      }

      if (elapsed >= totalDuration) {
        clearInterval(interval)
        setIsComplete(true)
        // Play completion sound sequence
        playBootSound(1000, 200, 'sweep')
        setTimeout(() => playBootSound(1200, 200, 'beep'), 200)
        setTimeout(() => playBootSound(1400, 300, 'sweep'), 400)
        setTimeout(() => {
          onComplete()
        }, 1000)
      }
    }, 50)

    return () => clearInterval(interval)
  }, [])

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 bg-black flex items-center justify-center overflow-hidden"
        initial={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Matrix Rain Background */}
        <MatrixRain />

        {/* Scan Lines */}
        <ScanLines />

        {/* Animated Grid Background */}
        <div className="absolute inset-0 opacity-20">
          <motion.div
            className="absolute inset-0"
            style={{
              backgroundImage: `
                linear-gradient(rgba(0, 217, 255, 0.3) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 217, 255, 0.3) 1px, transparent 1px)
              `,
              backgroundSize: '50px 50px',
            }}
            animate={{
              backgroundPosition: ['0px 0px', '50px 50px'],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'linear',
            }}
          />
        </div>

        {/* Scanning Line Effect */}
        <motion.div
          className="absolute inset-0 pointer-events-none"
          initial={{ y: '-100%' }}
          animate={{ y: '100%' }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'linear',
          }}
        >
          <div className="w-full h-1 bg-gradient-to-r from-transparent via-cyber-blue to-transparent opacity-50 shadow-lg shadow-cyber-blue" />
        </motion.div>

        {/* Glitch overlay */}
        {showGlitch && (
          <motion.div
            className="absolute inset-0 bg-cyber-blue/10"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 0.1 }}
          />
        )}

        {/* Main Content */}
        <div className="relative z-10 w-full max-w-2xl px-8">
          {/* Logo/Title */}
          <motion.div
            className="text-center mb-12"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              className="inline-block mb-4 relative"
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: 'linear',
              }}
            >
              <div className="w-24 h-24 rounded-full border-4 border-cyber-blue relative">
                <div className="absolute inset-2 rounded-full border-2 border-cyber-purple" />
                <div className="absolute inset-4 rounded-full border-2 border-cyber-pink" />
                <motion.div
                  className="absolute inset-0 rounded-full bg-gradient-to-br from-cyber-blue/20 to-cyber-purple/20"
                  animate={{
                    scale: [1, 1.1, 1],
                    opacity: [0.5, 0.8, 0.5],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                  }}
                />
                {/* Pulsing rings */}
                <motion.div
                  className="absolute inset-0 rounded-full border-2 border-cyber-blue"
                  animate={{
                    scale: [1, 1.5, 1.5],
                    opacity: [0.8, 0, 0],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                  }}
                />
              </div>
            </motion.div>

            <GlitchText
              text="OMNIMIND OS"
              className="text-5xl font-bold holo-text mb-2"
            />
            <motion.p
              className="text-cyber-blue/70 text-sm uppercase tracking-widest"
              style={{ fontFamily: 'var(--font-orbitron)' }}
              animate={{
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
              }}
            >
              Neural Interface v2.0
            </motion.p>
          </motion.div>

          {/* Boot Steps */}
          <div className="space-y-3 mb-8">
            {bootSteps.map((step, index) => {
              const Icon = step.icon
              const isActive = index === currentStep
              const isCompleted = index < currentStep

              return (
                <motion.div
                  key={step.id}
                  className={`flex items-center gap-4 p-4 rounded-lg border transition-all duration-300 ${
                    isActive
                      ? 'bg-cyber-blue/10 border-cyber-blue shadow-lg shadow-cyber-blue/20'
                      : isCompleted
                      ? 'bg-cyber-green/5 border-cyber-green/30'
                      : 'bg-white/5 border-white/10'
                  }`}
                  initial={{ x: -50, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="relative">
                    {isCompleted ? (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: 'spring', stiffness: 200 }}
                      >
                        <CheckCircle className="text-cyber-green" size={24} />
                      </motion.div>
                    ) : (
                      <Icon
                        className={isActive ? 'text-cyber-blue' : 'text-gray-500'}
                        size={24}
                      />
                    )}
                    {isActive && (
                      <>
                        <motion.div
                          className="absolute inset-0 rounded-full bg-cyber-blue/30"
                          animate={{
                            scale: [1, 1.5, 1],
                            opacity: [0.5, 0, 0.5],
                          }}
                          transition={{
                            duration: 1,
                            repeat: Infinity,
                          }}
                        />
                        <motion.div
                          className="absolute inset-0 rounded-full border-2 border-cyber-blue"
                          animate={{
                            scale: [1, 2],
                            opacity: [0.8, 0],
                          }}
                          transition={{
                            duration: 1,
                            repeat: Infinity,
                          }}
                        />
                      </>
                    )}
                  </div>

                  <div className="flex-1">
                    <p
                      className={`text-sm font-semibold tracking-wider ${
                        isActive
                          ? 'text-cyber-blue'
                          : isCompleted
                          ? 'text-cyber-green'
                          : 'text-gray-500'
                      }`}
                      style={{ fontFamily: 'var(--font-orbitron)' }}
                    >
                      {step.label}
                    </p>
                  </div>

                  {isActive && (
                    <motion.div
                      className="flex gap-1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      {[0, 1, 2].map((i) => (
                        <motion.div
                          key={i}
                          className="w-2 h-2 rounded-full bg-cyber-blue"
                          animate={{
                            scale: [1, 1.5, 1],
                            opacity: [0.3, 1, 0.3],
                          }}
                          transition={{
                            duration: 0.8,
                            repeat: Infinity,
                            delay: i * 0.2,
                          }}
                        />
                      ))}
                    </motion.div>
                  )}
                </motion.div>
              )
            })}
          </div>

          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-xs text-gray-400 uppercase tracking-wider">
              <span style={{ fontFamily: 'var(--font-orbitron)' }}>
                {isComplete ? 'BOOT COMPLETE' : 'BOOTING SYSTEM'}
              </span>
              <motion.span
                style={{ fontFamily: 'var(--font-orbitron)' }}
                animate={{
                  color: isComplete ? '#00ff88' : '#00d9ff',
                }}
              >
                {Math.round(progress)}%
              </motion.span>
            </div>
            <div className="h-2 bg-white/10 rounded-full overflow-hidden relative">
              <motion.div
                className="h-full bg-gradient-to-r from-cyber-blue via-cyber-purple to-cyber-pink relative"
                initial={{ width: '0%' }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.3 }}
              >
                <motion.div
                  className="absolute inset-0 bg-white/30"
                  animate={{
                    x: ['-100%', '100%'],
                  }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                    ease: 'linear',
                  }}
                />
              </motion.div>
              {/* Glow effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent"
                style={{
                  width: '20%',
                  filter: 'blur(10px)',
                }}
                animate={{
                  x: ['-20%', '120%'],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: 'linear',
                }}
              />
            </div>
          </div>

          {/* System Info */}
          <motion.div
            className="mt-8 text-center text-xs text-gray-500 space-y-1"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <p style={{ fontFamily: 'var(--font-orbitron)' }}>
              KERNEL VERSION 2.0.1 | BUILD 20250124
            </p>
            <p style={{ fontFamily: 'var(--font-orbitron)' }}>
              COPYRIGHT © 2025 OMNIMIND SYSTEMS
            </p>
          </motion.div>
        </div>

        {/* Corner Decorations with animation */}
        {[
          { top: '20px', left: '20px', rotate: 0 },
          { top: '20px', right: '20px', rotate: 90 },
          { bottom: '20px', left: '20px', rotate: 270 },
          { bottom: '20px', right: '20px', rotate: 180 },
        ].map((pos, i) => (
          <motion.div
            key={i}
            className="absolute w-12 h-12 border-l-2 border-t-2 border-cyber-blue/50"
            style={pos}
            initial={{ opacity: 0, scale: 0 }}
            animate={{
              opacity: [0.5, 1, 0.5],
              scale: 1,
            }}
            transition={{
              opacity: { duration: 2, repeat: Infinity, delay: i * 0.2 },
              scale: { delay: i * 0.1 },
            }}
          />
        ))}

        {/* Holographic overlay particles */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 bg-cyber-blue rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                opacity: [0, 1, 0],
                scale: [0, 1, 0],
              }}
              transition={{
                duration: 2 + Math.random() * 2,
                repeat: Infinity,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>
      </motion.div>
    </AnimatePresence>
  )
}