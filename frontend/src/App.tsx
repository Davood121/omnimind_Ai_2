import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import HolographicLogo from '@/components/HolographicLogo'
import HolographicCore3D from '@/components/HolographicCore3D'
import AudioVisualizer3D from '@/components/AudioVisualizer3D'
import ParticleField3D from '@/components/ParticleField3D'
import VoiceVisualizer from '@/components/VoiceVisualizer'
import SpeechWaveform from '@/components/SpeechWaveform'
import SystemPanel from '@/components/SystemPanel'
import EnhancedSystemPanel from '@/components/EnhancedSystemPanel'
import ChatInterface from '@/components/ChatInterface'
import SkillsPanel from '@/components/SkillsPanel'
import ParticleField from '@/components/ParticleField'
import BootAnimation from '@/components/BootAnimation'
import { api } from '@/services/api'
import { useAudioReactive } from '@/hooks/useAudioReactive'
import { useBootAnimation } from '@/hooks/useBootAnimation'
import { Menu, X, Zap } from 'lucide-react'

function App() {
  const [isListening, setIsListening] = useState(false)
  const [aiStatus, setAiStatus] = useState<'idle' | 'thinking' | 'speaking'>('idle')
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant', content: string }>>([])
  const [showSystemPanel, setShowSystemPanel] = useState(true)
  const [showChatPanel, setShowChatPanel] = useState(true)
  const [showSkillsPanel, setShowSkillsPanel] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [use3DMode, setUse3DMode] = useState(true)
  
  // Boot animation
  const { showBoot, handleBootComplete } = useBootAnimation()
  
  // Audio-reactive hologram
  const { audioLevel } = useAudioReactive(aiStatus === 'speaking')

  useEffect(() => {
    // Check backend connection and load conversation history
    const initializeApp = async () => {
      try {
        await api.getStatus()
        setIsConnected(true)
        
        const history = await api.getConversations()
        // Don't auto-load history - start fresh
        setMessages([
          { role: 'assistant', content: 'OmniMind OS initialized. All systems operational.' }
        ])
      } catch (error) {
        setIsConnected(false)
        setMessages([{ 
          role: 'assistant', 
          content: 'Backend connection failed. Please start the API server with: python api_server.py' 
        }])
      }
    }

    initializeApp()

    // Auto-hide panels on mobile
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setShowSystemPanel(false)
        setShowChatPanel(false)
        setShowSkillsPanel(false)
      } else {
        setShowSystemPanel(true)
        setShowChatPanel(true)
        setShowSkillsPanel(false)
      }
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const handleSendMessage = async (msg: string) => {
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    setAiStatus('thinking')
    
    try {
      const response = await api.sendMessage(msg)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.response 
      }])
      
      // Sync hologram with voice duration
      if (response.speaking && response.speech_duration) {
        setAiStatus('speaking')
        setTimeout(() => setAiStatus('idle'), response.speech_duration)
      } else {
        setAiStatus('speaking')
        const sentences = response.response.split(/[.!?]+/).length
        setTimeout(() => setAiStatus('idle'), sentences * 2000)
      }
      
      return response
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Connection error. Please ensure the API server is running on port 8000.' 
      }])
      setAiStatus('idle')
      setIsConnected(false)
      return null
    }
  }

  const clearChat = () => {
    setMessages([])
  }

  const handleExecuteSkill = async (skillId: string, query: string) => {
    setMessages(prev => [...prev, { role: 'user', content: query }])
    setAiStatus('thinking')
    
    try {
      const response = await fetch('http://localhost:8000/api/execute-skill', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skill_id: skillId, query })
      })
      const data = await response.json()
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.success ? data.result : `Error: ${data.error || 'Failed to execute skill'}` 
      }])
      setAiStatus('idle')
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Failed to execute skill. Please check connection.' 
      }])
      setAiStatus('idle')
    }
  }

  return (
    <>
      {/* Boot Animation */}
      {showBoot && <BootAnimation onComplete={handleBootComplete} />}
      
      {/* Main App */}
      <div className="relative w-full h-full bg-black overflow-hidden">
      {/* Animated Background - 3D or 2D */}
      {use3DMode ? (
        <ParticleField3D isSpeaking={aiStatus === 'speaking'} audioLevel={audioLevel} />
      ) : (
        <ParticleField isSpeaking={aiStatus === 'speaking'} audioLevel={audioLevel} />
      )}
      
      {/* Holographic Grid Background */}
      <div className="absolute inset-0 opacity-20 pointer-events-none">
        <div className="absolute inset-0" style={{
          backgroundImage: `
            linear-gradient(rgba(0, 217, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 217, 255, 0.1) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px'
        }} />
      </div>

      {/* Main Content */}
      <div className="relative z-10 w-full h-full flex flex-col">
        {/* Header */}
        <header className="glass-panel border-b border-cyber-blue/30 px-4 sm:px-6 lg:px-8 py-3 sm:py-4 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 sm:gap-4">
              <button
                onClick={() => setUse3DMode(!use3DMode)}
                className="w-8 h-8 sm:w-12 sm:h-12 rounded-full glow-border flex items-center justify-center flex-shrink-0 hover:scale-110 transition-transform cursor-pointer"
                title={use3DMode ? "Switch to 2D Mode" : "Switch to 3D Mode"}
              >
                <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple animate-pulse" />
              </button>
              <div>
                <h1 className="text-lg sm:text-2xl font-bold holo-text" style={{ fontFamily: 'var(--font-orbitron)' }}>
                  OMNIMIND OS
                </h1>
                <p className="text-[10px] sm:text-xs text-cyber-blue/70">Neural Interface v2.0</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2 sm:gap-6">
              <div className="hidden sm:flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${
                  !isConnected ? 'bg-red-500' :
                  aiStatus === 'idle' ? 'bg-cyber-green' : 
                  aiStatus === 'thinking' ? 'bg-cyber-orange animate-pulse' : 
                  'bg-cyber-blue animate-pulse'
                }`} />
                <span className="text-xs sm:text-sm text-gray-400 uppercase tracking-wider">
                  {!isConnected ? 'offline' : aiStatus}
                </span>
              </div>

              {/* Mobile Menu Buttons */}
              <div className="flex gap-2 lg:hidden">
                <button
                  onClick={() => setShowSystemPanel(!showSystemPanel)}
                  className="p-2 rounded-lg bg-cyber-blue/20 border border-cyber-blue/50 text-cyber-blue"
                  title="System Status"
                >
                  <Menu size={20} />
                </button>
                <button
                  onClick={() => setShowSkillsPanel(!showSkillsPanel)}
                  className="p-2 rounded-lg bg-cyber-purple/20 border border-cyber-purple/50 text-cyber-purple"
                  title="AI Skills"
                >
                  <Zap size={20} />
                </button>
                <button
                  onClick={() => setShowChatPanel(!showChatPanel)}
                  className="p-2 rounded-lg bg-cyber-pink/20 border border-cyber-pink/50 text-cyber-pink"
                  title="Chat"
                >
                  <Menu size={20} />
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Layout */}
        <div className="flex-1 flex gap-2 sm:gap-4 p-2 sm:p-4 overflow-hidden">
          {/* Left Panel - System Info */}
          <div className={`
            ${showSystemPanel ? 'flex' : 'hidden lg:flex'}
            w-full lg:w-80 flex-col gap-4
            ${showSystemPanel && window.innerWidth < 1024 ? 'absolute inset-0 z-50 bg-black/95 p-4' : ''}
          `}>
            {showSystemPanel && window.innerWidth < 1024 && (
              <button
                onClick={() => setShowSystemPanel(false)}
                className="absolute top-4 right-4 p-2 rounded-lg bg-cyber-blue/20 border border-cyber-blue text-cyber-blue"
              >
                <X size={20} />
              </button>
            )}
            {use3DMode ? (
              <EnhancedSystemPanel isConnected={isConnected} />
            ) : (
              <SystemPanel isConnected={isConnected} />
            )}
          </div>

          {/* Skills Panel (Desktop: between system and center) */}
          <div className={`
            ${showSkillsPanel ? 'flex' : 'hidden'}
            w-full lg:w-80 flex-col gap-4
            ${showSkillsPanel && window.innerWidth < 1024 ? 'absolute inset-0 z-50 bg-black/95 p-4' : ''}
          `}>
            {showSkillsPanel && window.innerWidth < 1024 && (
              <button
                onClick={() => setShowSkillsPanel(false)}
                className="absolute top-4 right-4 p-2 rounded-lg bg-cyber-purple/20 border border-cyber-purple text-cyber-purple"
              >
                <X size={20} />
              </button>
            )}
            <SkillsPanel onExecuteSkill={handleExecuteSkill} />
          </div>

          {/* Center - Holographic Logo (3D or 2D) */}
          <div className="flex-1 flex flex-col items-center justify-center relative min-w-0">
            <div className="w-full max-w-md aspect-square flex items-center justify-center">
              {use3DMode ? (
                <HolographicCore3D
                  isActive={isListening || aiStatus !== 'idle'} 
                  isSpeaking={aiStatus === 'speaking'}
                  audioLevel={audioLevel}
                />
              ) : (
                <HolographicLogo 
                  isActive={isListening || aiStatus !== 'idle'} 
                  isSpeaking={aiStatus === 'speaking'}
                  audioLevel={audioLevel}
                />
              )}
            </div>
            
            {/* Voice Input Visualizer */}
            {isListening && (
              <div className="absolute bottom-16 sm:bottom-20">
                <VoiceVisualizer isActive={isListening} />
              </div>
            )}

            {/* AI Speech Waveform - 3D or 2D */}
            {aiStatus === 'speaking' && (
              <div className="absolute bottom-16 sm:bottom-20 flex flex-col items-center gap-2">
                {use3DMode ? (
                  <div className="w-64 h-32">
                    <AudioVisualizer3D isActive={true} audioLevel={audioLevel} />
                  </div>
                ) : (
                  <SpeechWaveform isActive={true} audioLevel={audioLevel} />
                )}
                <motion.div
                  className="text-cyber-blue text-sm font-semibold uppercase tracking-wider"
                  style={{ fontFamily: 'var(--font-orbitron)' }}
                  animate={{
                    opacity: [0.5, 1, 0.5],
                    scale: [0.95, 1.05, 0.95]
                  }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  AI Speaking...
                </motion.div>
              </div>
            )}

            <button
              onClick={() => setIsListening(!isListening)}
              className={`mt-4 sm:mt-8 px-4 sm:px-8 py-2 sm:py-4 rounded-full font-semibold text-sm sm:text-lg transition-all duration-300 ${
                isListening 
                  ? 'bg-cyber-pink/20 border-2 border-cyber-pink text-cyber-pink pulse-glow' 
                  : 'bg-cyber-blue/20 border-2 border-cyber-blue text-cyber-blue hover:bg-cyber-blue/30'
              }`}
              style={{ fontFamily: 'var(--font-orbitron)' }}
            >
              {isListening ? 'LISTENING...' : 'ACTIVATE VOICE'}
            </button>
          </div>

          {/* Right Panel - Chat Interface */}
          <div className={`
            ${showChatPanel ? 'flex' : 'hidden lg:flex'}
            w-full lg:w-96 flex-col
            ${showChatPanel && window.innerWidth < 1024 ? 'absolute inset-0 z-50 bg-black/95 p-4' : ''}
          `}>
            {showChatPanel && window.innerWidth < 1024 && (
              <button
                onClick={() => setShowChatPanel(false)}
                className="absolute top-4 right-4 p-2 rounded-lg bg-cyber-purple/20 border border-cyber-purple text-cyber-purple z-10"
              >
                <X size={20} />
              </button>
            )}
            <ChatInterface 
              messages={messages} 
              onSendMessage={handleSendMessage}
              onClearChat={clearChat}
              isConnected={isConnected}
            />
          </div>
        </div>
      </div>
    </div>
    </>
  )
}

export default App