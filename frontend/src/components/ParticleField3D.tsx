import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import type * as THREE from 'three'

interface ParticleField3DProps {
  isSpeaking?: boolean
  audioLevel?: number
}

function LightParticles({ isSpeaking, audioLevel }: { isSpeaking: boolean; audioLevel: number }) {
  const pointsRef = useRef<THREE.Points>(null)
  
  const { positions, colors } = useMemo(() => {
    const count = 500 // Reduced from 2000
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)
    
    const colorPalette = [
      { r: 0, g: 0.85, b: 1 },      // cyan
      { r: 0.71, g: 0.22, b: 0.95 }, // purple
      { r: 1, g: 0, b: 0.43 }        // pink
    ]
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      const radius = 5 + Math.random() * 5
      const theta = Math.random() * Math.PI * 2
      const phi = Math.random() * Math.PI
      
      positions[i3] = radius * Math.sin(phi) * Math.cos(theta)
      positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
      positions[i3 + 2] = radius * Math.cos(phi)
      
      const color = colorPalette[Math.floor(Math.random() * colorPalette.length)]
      colors[i3] = color.r
      colors[i3 + 1] = color.g
      colors[i3 + 2] = color.b
    }
    
    return { positions, colors }
  }, [])

  useFrame((state) => {
    if (!pointsRef.current) return
    const time = state.clock.getElapsedTime()
    
    pointsRef.current.rotation.y = time * 0.05
    pointsRef.current.rotation.x = Math.sin(time * 0.1) * 0.1
  })

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
        />
        <bufferAttribute
          attach="attributes-color"
          args={[colors, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={isSpeaking ? 0.04 + audioLevel * 0.02 : 0.03}
        vertexColors
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}

export default function ParticleField3D({ isSpeaking = false, audioLevel = 0 }: ParticleField3DProps) {
  return (
    <div className="absolute inset-0 pointer-events-none">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 75 }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <LightParticles isSpeaking={isSpeaking} audioLevel={audioLevel} />
      </Canvas>
    </div>
  )
}