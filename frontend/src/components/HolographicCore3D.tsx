import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Sphere, MeshDistortMaterial } from '@react-three/drei'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'
import type * as THREE from 'three'

interface HolographicCore3DProps {
  isActive: boolean
  isSpeaking?: boolean
  audioLevel?: number
}

function SimpleSphere({ isSpeaking, audioLevel }: { isSpeaking: boolean; audioLevel: number }) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  useFrame((state) => {
    if (!meshRef.current) return
    const time = state.clock.getElapsedTime()
    
    // Gentle rotation
    meshRef.current.rotation.y = time * 0.3
    meshRef.current.rotation.x = Math.sin(time * 0.2) * 0.1
    
    // Audio-reactive scale
    const scale = isSpeaking ? 1 + audioLevel * 0.2 : 1
    meshRef.current.scale.setScalar(scale)
  })

  return (
    <Sphere ref={meshRef} args={[1, 64, 64]}>
      <MeshDistortMaterial
        color="#00d9ff"
        attach="material"
        distort={isSpeaking ? 0.3 + audioLevel * 0.2 : 0.2}
        speed={isSpeaking ? 2 : 1}
        roughness={0.1}
        metalness={0.8}
        emissive="#00d9ff"
        emissiveIntensity={isSpeaking ? 0.6 + audioLevel * 0.4 : 0.4}
      />
    </Sphere>
  )
}

export default function HolographicCore3D({ isSpeaking = false, audioLevel = 0 }: HolographicCore3DProps) {
  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [0, 0, 3], fov: 75 }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[5, 5, 5]} intensity={1} color="#00d9ff" />
        <pointLight position={[-5, -5, -5]} intensity={0.5} color="#b537f2" />
        
        <SimpleSphere isSpeaking={isSpeaking} audioLevel={audioLevel} />
        
        <EffectComposer>
          <Bloom
            intensity={isSpeaking ? 1 + audioLevel * 0.5 : 0.8}
            luminanceThreshold={0.2}
            luminanceSmoothing={0.9}
            blendFunction={BlendFunction.ADD}
          />
        </EffectComposer>
      </Canvas>
    </div>
  )
}