import { useState, useEffect, useRef } from 'react'

interface AudioReactiveState {
  audioLevel: number
  isAnalyzing: boolean
}

/**
 * Hook to simulate audio-reactive behavior based on AI speaking state
 * In a real implementation, this would analyze actual audio output
 */
export function useAudioReactive(isSpeaking: boolean): AudioReactiveState {
  const [audioLevel, setAudioLevel] = useState<number>(0)
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false)
  const animationFrameRef = useRef<number | undefined>(undefined)
  const timeRef = useRef<number>(0)

  useEffect(() => {
    if (isSpeaking) {
      setIsAnalyzing(true)
      
      const animate = () => {
        timeRef.current += 0.05
        
        // Simulate natural speech patterns with varying intensity
        const baseWave = Math.sin(timeRef.current * 3) * 0.5 + 0.5
        const microVariation = Math.sin(timeRef.current * 15) * 0.2
        const randomSpike = Math.random() * 0.3
        
        // Combine for realistic speech-like pattern
        const level = Math.min(1, Math.max(0, baseWave + microVariation + randomSpike))
        
        setAudioLevel(level)
        animationFrameRef.current = requestAnimationFrame(animate)
      }
      
      animate()
      
      return () => {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current)
        }
      }
    } else {
      setIsAnalyzing(false)
      setAudioLevel(0)
      timeRef.current = 0
    }
  }, [isSpeaking])

  return { audioLevel, isAnalyzing }
}

/**
 * Hook for real Web Audio API implementation (future enhancement)
 * This would analyze actual audio output from text-to-speech
 */
export function useRealAudioAnalyzer(audioElement: HTMLAudioElement | null): AudioReactiveState {
  const [audioLevel, setAudioLevel] = useState<number>(0)
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false)
  const analyzerRef = useRef<AnalyserNode | null>(null)
  const animationFrameRef = useRef<number | undefined>(undefined)

  useEffect(() => {
    if (!audioElement) return

    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      const source = audioContext.createMediaElementSource(audioElement)
      const analyzer = audioContext.createAnalyser()
      
      analyzer.fftSize = 256
      source.connect(analyzer)
      analyzer.connect(audioContext.destination)
      
      analyzerRef.current = analyzer
      setIsAnalyzing(true)

      const dataArray = new Uint8Array(analyzer.frequencyBinCount)

      const analyze = () => {
        if (!analyzerRef.current) return

        analyzerRef.current.getByteFrequencyData(dataArray)
        
        // Calculate average volume
        const average = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length
        const normalizedLevel = average / 255
        
        setAudioLevel(normalizedLevel)
        animationFrameRef.current = requestAnimationFrame(analyze)
      }

      analyze()

      return () => {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current)
        }
        if (audioContext.state !== 'closed') {
          audioContext.close()
        }
      }
    } catch (error) {
      console.error('Failed to initialize audio analyzer:', error)
      setIsAnalyzing(false)
    }
  }, [audioElement])

  return { audioLevel, isAnalyzing }
}