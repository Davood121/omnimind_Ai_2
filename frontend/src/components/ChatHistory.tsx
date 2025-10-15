import { useState, useEffect } from 'react'
import { Clock, Search, Trash2, Download } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface ChatSession {
  id: string
  timestamp: number
  messages: Array<{ role: 'user' | 'assistant', content: string }>
  summary: string
}

interface ChatHistoryProps {
  isOpen: boolean
  onClose: () => void
  onLoadSession: (messages: Array<{ role: 'user' | 'assistant', content: string }>) => void
}

export default function ChatHistory({ isOpen, onClose, onLoadSession }: ChatHistoryProps) {
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    if (isOpen) {
      loadChatHistory()
    }
  }, [isOpen])

  const loadChatHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/conversations')
      const conversations = await response.json()
      
      // Group conversations into sessions (by day or conversation breaks)
      const groupedSessions: ChatSession[] = []
      let currentSession: ChatSession | null = null
      
      conversations.forEach((conv: any, index: number) => {
        const timestamp = conv.timestamp * 1000
        const date = new Date(timestamp)
        
        // Start new session if it's a new day or first message
        if (!currentSession || 
            new Date(currentSession.timestamp).toDateString() !== date.toDateString()) {
          
          if (currentSession) {
            groupedSessions.push(currentSession)
          }
          
          currentSession = {
            id: `session-${index}`,
            timestamp,
            messages: [],
            summary: ''
          }
        }
        
        // Add messages to current session
        currentSession.messages.push(
          { role: 'user', content: conv.user },
          { role: 'assistant', content: conv.assistant }
        )
      })
      
      if (currentSession) {
        groupedSessions.push(currentSession)
      }
      
      // Generate summaries for sessions
      groupedSessions.forEach(session => {
        const firstUserMessage = session.messages.find(m => m.role === 'user')?.content || ''
        session.summary = firstUserMessage.length > 50 
          ? firstUserMessage.substring(0, 50) + '...'
          : firstUserMessage || 'Chat session'
      })
      
      setSessions(groupedSessions.reverse()) // Most recent first
    } catch (error) {
      console.error('Failed to load chat history:', error)
    }
  }

  const filteredSessions = sessions.filter(session =>
    session.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
    session.messages.some(msg => 
      msg.content.toLowerCase().includes(searchTerm.toLowerCase())
    )
  )

  const clearHistory = async () => {
    if (confirm('Are you sure you want to clear all chat history?')) {
      try {
        // This would need a backend endpoint to clear history
        setSessions([])
      } catch (error) {
        console.error('Failed to clear history:', error)
      }
    }
  }

  const exportHistory = () => {
    const dataStr = JSON.stringify(sessions, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `omnimind-chat-history-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="glass-panel rounded-2xl w-full max-w-2xl h-[80vh] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="p-4 border-b border-cyber-blue/30">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-cyber-blue">Chat History</h2>
                <div className="flex gap-2">
                  <button
                    onClick={exportHistory}
                    className="p-2 rounded-lg bg-cyber-green/20 border border-cyber-green/50 text-cyber-green hover:bg-cyber-green/30"
                    title="Export History"
                  >
                    <Download size={16} />
                  </button>
                  <button
                    onClick={clearHistory}
                    className="p-2 rounded-lg bg-red-500/20 border border-red-500/50 text-red-500 hover:bg-red-500/30"
                    title="Clear History"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
              
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                <input
                  type="text"
                  placeholder="Search conversations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-black/50 border border-cyber-blue/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyber-blue"
                />
              </div>
            </div>

            {/* Sessions List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {filteredSessions.length === 0 ? (
                <div className="text-center py-8 text-gray-400">
                  {searchTerm ? 'No matching conversations found' : 'No chat history yet'}
                </div>
              ) : (
                filteredSessions.map((session) => (
                  <motion.div
                    key={session.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-panel rounded-lg p-3 border border-cyber-blue/20 hover:border-cyber-blue/50 cursor-pointer transition-all"
                    onClick={() => {
                      onLoadSession(session.messages)
                      onClose()
                    }}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-sm font-semibold text-white mb-1">
                          {session.summary}
                        </h3>
                        <div className="flex items-center gap-2 text-xs text-gray-400">
                          <Clock size={12} />
                          <span>{new Date(session.timestamp).toLocaleString()}</span>
                          <span>•</span>
                          <span>{session.messages.length} messages</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Preview of first few messages */}
                    <div className="mt-2 space-y-1">
                      {session.messages.slice(0, 2).map((msg, i) => (
                        <div key={i} className="text-xs text-gray-500 truncate">
                          <span className={msg.role === 'user' ? 'text-cyber-pink' : 'text-cyber-blue'}>
                            {msg.role === 'user' ? 'You' : 'AI'}:
                          </span>
                          {' ' + msg.content.substring(0, 60)}
                          {msg.content.length > 60 && '...'}
                        </div>
                      ))}
                    </div>
                  </motion.div>
                ))
              )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-cyber-blue/30">
              <button
                onClick={onClose}
                className="w-full py-2 bg-cyber-blue/20 border border-cyber-blue rounded-lg text-cyber-blue hover:bg-cyber-blue/30 transition-all"
              >
                Close
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}