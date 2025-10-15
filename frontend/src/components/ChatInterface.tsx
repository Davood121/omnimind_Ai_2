import { useState, useRef, useEffect } from 'react'
import { Send, User, Bot, History, Lightbulb, Clock, Trash2, RefreshCw } from 'lucide-react'
import FloatingChatBubble3D from './FloatingChatBubble3D'
import ChatHistory from './ChatHistory'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ChatInterfaceProps {
  messages: Message[]
  onSendMessage: (message: string) => void
  onClearChat: () => void
  isConnected: boolean
}

interface SmartSuggestion {
  text: string
  icon: string
}

export default function ChatInterface({ messages, onSendMessage, onClearChat, isConnected }: ChatInterfaceProps) {
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [showHistoryModal, setShowHistoryModal] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isSending && isConnected) {
      setIsSending(true)
      const response = await onSendMessage(input)
      // Update suggestions if available
      if (response && response.suggestions) {
        setSuggestions(response.suggestions)
      }
      setInput('')
      setIsSending(false)
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion)
  }

  const getSmartSuggestions = (): SmartSuggestion[] => {
    if (suggestions.length > 0) {
      return suggestions.map(s => ({ text: s, icon: '💡' }))
    }
    
    // Default suggestions based on recent messages
    const recentMsg = messages[messages.length - 1]?.content.toLowerCase() || ''
    
    if (recentMsg.includes('news')) {
      return [
        { text: 'Get breaking news', icon: '🚨' },
        { text: 'Search latest AI news', icon: '🤖' },
        { text: 'Show world headlines', icon: '🌍' }
      ]
    } else if (recentMsg.includes('search')) {
      return [
        { text: 'Find more information', icon: '🔍' },
        { text: 'Get detailed analysis', icon: '📊' },
        { text: 'Search related topics', icon: '🔗' }
      ]
    }
    
    return [
      { text: 'What is the latest news?', icon: '📰' },
      { text: 'Search for something', icon: '🔍' },
      { text: 'Tell me about AI', icon: '🤖' }
    ]
  }

  return (
    <div className="glass-panel rounded-2xl h-full flex flex-col overflow-hidden">
      {/* Header */}
      <div className="p-3 sm:p-4 border-b border-cyber-blue/30 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-cyber-blue uppercase tracking-wider" style={{ fontFamily: 'var(--font-orbitron)' }}>
              Neural Interface
            </h2>
            {!isConnected && (
              <p className="text-xs text-red-500 mt-1">Backend offline - Start api_server.py</p>
            )}
          </div>
          <div className="flex gap-2">
            <button
              onClick={onClearChat}
              className="p-2 rounded-lg bg-red-500/20 border border-red-500/50 text-red-500 hover:bg-red-500/30 transition-all"
              title="Clear Chat"
            >
              <Trash2 size={16} />
            </button>
            <button
              onClick={() => setShowHistoryModal(true)}
              className="p-2 rounded-lg bg-cyber-purple/20 border border-cyber-purple/50 text-cyber-purple hover:bg-cyber-purple/30 transition-all"
              title="View Chat History"
            >
              <History size={16} />
            </button>
          </div>
        </div>
        
        {/* Chat Stats */}
        <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
          <div className="flex items-center gap-1">
            <Clock size={12} />
            <span>{messages.length} messages</span>
          </div>
          <div className="flex items-center gap-1">
            <Bot size={12} />
            <span>Enhanced AI</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1">
        {/* Welcome Message */}
        {messages.length <= 1 && (
          <div className="text-center py-8">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center">
              <Bot className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-cyber-blue mb-2" style={{ fontFamily: 'var(--font-orbitron)' }}>Welcome to OmniMind</h3>
            <p className="text-sm text-gray-400 mb-6">Your enhanced AI assistant with multi-engine search capabilities</p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-md mx-auto">
              {getSmartSuggestions().map((suggestion, i) => (
                <button
                  key={i}
                  onClick={() => handleSuggestionClick(suggestion.text)}
                  className="px-4 py-3 text-sm bg-cyber-blue/20 border border-cyber-blue/50 rounded-lg text-cyber-blue hover:bg-cyber-blue/30 transition-all text-center"
                >
                  <div className="text-lg mb-1">{suggestion.icon}</div>
                  <div className="text-xs">{suggestion.text}</div>
                </button>
              ))}
            </div>
          </div>
        )}
        
        {/* Chat Messages */}
        {messages.filter(msg => msg.content.trim()).map((message, index) => (
          <div key={index} className={`flex gap-3 mb-4 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {/* Assistant Avatar */}
            {message.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center flex-shrink-0 mt-1">
                <Bot size={16} />
              </div>
            )}
            
            {/* Message Bubble */}
            <div className={`max-w-[75%] ${message.role === 'user' ? 'order-1' : 'order-2'}`}>
              <div className={`
                px-4 py-3 rounded-2xl shadow-lg
                ${message.role === 'user' 
                  ? 'bg-gradient-to-r from-cyber-pink/20 to-cyber-orange/20 border border-cyber-pink/30 text-white ml-auto' 
                  : 'bg-gradient-to-r from-cyber-blue/20 to-cyber-purple/20 border border-cyber-blue/30 text-white'
                }
              `}>
                <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                  {message.content}
                </p>
                <div className="text-[10px] text-gray-400 mt-2 opacity-70">
                  {new Date().toLocaleTimeString()}
                </div>
              </div>
            </div>

            {/* User Avatar */}
            {message.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyber-pink to-cyber-orange flex items-center justify-center flex-shrink-0 mt-1 order-2">
                <User size={16} />
              </div>
            )}
          </div>
        ))}
        
        {/* Smart Suggestions */}
        {messages.length > 1 && suggestions.length > 0 && (
          <div className="border-t border-cyber-blue/20 pt-4 mt-4">
            <div className="flex items-center gap-2 mb-3">
              <Lightbulb size={14} className="text-cyber-green" />
              <span className="text-xs text-cyber-green font-semibold uppercase tracking-wider">Smart Suggestions</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {suggestions.slice(0, 4).map((suggestion, i) => (
                <button
                  key={i}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="px-3 py-2 text-xs bg-cyber-green/20 border border-cyber-green/50 rounded-lg text-cyber-green hover:bg-cyber-green/30 transition-all text-left"
                >
                  💡 {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-cyber-blue/30 flex-shrink-0 bg-black/20">
        <form onSubmit={handleSubmit}>
          <div className="flex gap-3 items-end">
            <div className="flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSubmit(e)
                  }
                }}
                placeholder={isConnected ? "Type your message... (Enter to send, Shift+Enter for new line)" : "Backend offline..."}
                disabled={!isConnected || isSending}
                rows={1}
                className="w-full bg-black/50 border border-cyber-blue/30 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-cyber-blue transition-colors disabled:opacity-50 resize-none min-h-[48px] max-h-32"
                style={{ 
                  height: 'auto',
                  minHeight: '48px'
                }}
                onInput={(e) => {
                  const target = e.target as HTMLTextAreaElement
                  target.style.height = 'auto'
                  target.style.height = Math.min(target.scrollHeight, 128) + 'px'
                }}
              />
            </div>
            <button
              type="submit"
              disabled={!isConnected || isSending || !input.trim()}
              className="px-4 py-3 bg-cyber-blue/20 border border-cyber-blue rounded-xl text-cyber-blue hover:bg-cyber-blue/30 transition-all flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0 min-h-[48px]"
            >
              {isSending ? (
                <RefreshCw size={18} className="animate-spin" />
              ) : (
                <Send size={18} />
              )}
            </button>
          </div>
        </form>
      </div>
      
      {/* Chat History Modal */}
      <ChatHistory
        isOpen={showHistoryModal}
        onClose={() => setShowHistoryModal(false)}
        onLoadSession={(sessionMessages) => {
          // This would need to be handled by parent component
          console.log('Load session:', sessionMessages)
        }}
      />
    </div>
  )
}