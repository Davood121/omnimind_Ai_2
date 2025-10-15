import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import type * as THREE from 'three'

interface AudioVisualizer3DProps {
  isActive: boolean
  audioLevel?: number
}

function SimpleWaveform({ audioLevel }: { audioLevel: number }) {
  const groupRef = useRef<THREE.Group>(null)
  
  const bars = useMemo(() => {
    const barCount = 32
    const barArray = []
    const radius = 1.5
    
    for (let i = 0; i < barCount; i++) {
      const angle = (i / barCount) * Math.PI * 2
      barArray.push({
        position: [
          Math.cos(angle) * radius,
          0,
          Math.sin(angle) * radius
        ] as [number, number, number],
        rotation: [0, -angle, 0] as [number, number, number]
      })
    }
    return barArray
  }, [])

  useFrame((state) => {
    if (!groupRef.current) return
    const time = state.clock.getElapsedTime()
    
    groupRef.current.children.forEach((child, i) => {
      const mesh = child as THREE.Mesh
      const height = 0.5 + Math.sin(time * 5 + i * 0.2) * audioLevel * 1.5
      mesh.scale.y = Math.max(0.1, height)
      mesh.position.y = height / 2
    })
    
    groupRef.current.rotation.y = time * 0.3
  })

  return (
    <group ref={groupRef}>
      {bars.map((bar, i) => (
        <mesh key={i} position={bar.position} rotation={bar.rotation}>
          <boxGeometry args={[0.08, 1, 0.08]} />
          <meshStandardMaterial
            color="#00d9ff"
            emissive="#00d9ff"
            emissiveIntensity={0.5 + audioLevel * 0.5}
          />
        </mesh>
      ))}
    </group>
  )
}

export default function AudioVisualizer3D({ isActive, audioLevel = 0 }: AudioVisualizer3DProps) {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [0, 1.5, 3], fov: 75 }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[5, 5, 5]} intensity={1} color="#00d9ff" />
        
        {isActive && <SimpleWaveform audioLevel={audioLevel} />}
      </Canvas>
    </div>
  )
}