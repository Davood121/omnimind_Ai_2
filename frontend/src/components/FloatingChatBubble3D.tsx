import { motion } from 'framer-motion'
import type { ReactNode } from 'react'

interface FloatingChatBubble3DProps {
  children: ReactNode
  isUser?: boolean
  delay?: number
}

export default function FloatingChatBubble3D({ 
  children, 
  isUser = false,
  delay = 0
}: FloatingChatBubble3DProps) {
  return (
    <motion.div
      className={`relative ${isUser ? 'ml-auto' : 'mr-auto'} max-w-[85%]`}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
      whileHover={{ scale: 1.02 }}
    >
      <motion.div
        className={`glass-panel rounded-2xl p-3 sm:p-4 ${
          isUser 
            ? 'bg-gradient-to-br from-cyber-blue/20 to-cyber-purple/20 border-cyber-blue/50' 
            : 'bg-gradient-to-br from-cyber-purple/20 to-cyber-pink/20 border-cyber-purple/50'
        } border`}
        animate={{
          boxShadow: [
            `0 0 10px ${isUser ? '#00d9ff20' : '#b537f220'}`,
            `0 0 15px ${isUser ? '#00d9ff30' : '#b537f230'}`,
            `0 0 10px ${isUser ? '#00d9ff20' : '#b537f220'}`
          ]
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        {children}
      </motion.div>
    </motion.div>
  )
}