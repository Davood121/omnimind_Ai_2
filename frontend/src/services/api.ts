const API_BASE = 'http://localhost:8000/api'

export interface ChatResponse {
  response: string
  status: string
  speaking?: boolean
  speech_duration?: number
  hologram_sync?: boolean
  suggestions?: string[]
  conversation_context?: {
    total_conversations: number
    recent_topics: string[]
    conversation_style: string
  }
}

export interface SystemStatus {
  status: string
  neural_load: string
  processing: string
  memory: string
  connection: string
  detailed?: {
    cpu: {
      usage_percent: number
      frequency_ghz: number
      cores: number
      history: number[]
    }
    memory: {
      usage_percent: number
      used_gb: number
      total_gb: number
      available_gb: number
      history: number[]
    }
    disk: {
      usage_percent: number
      used_gb: number
      total_gb: number
      free_gb: number
    }
    network: {
      bytes_sent_mb: number
      bytes_recv_mb: number
      packets_sent: number
      packets_recv: number
    }
    wifi_signal: number | null
    battery: {
      percent: number
      plugged_in: boolean
      time_left_minutes: number | null
    } | null
    temperature: {
      sensor: string
      current_celsius: number
      high_celsius: number | null
    } | null
    top_processes: Array<{
      name: string
      cpu_percent: number
      memory_percent: number
    }>
    timestamp: number
  }
}

export interface ConversationEntry {
  timestamp: number
  user: string
  assistant: string
}

export const api = {
  async getStatus(): Promise<SystemStatus> {
    try {
      const response = await fetch(`${API_BASE}/status`, {
        signal: AbortSignal.timeout(5000)
      })
      if (!response.ok) throw new Error('Failed to fetch status')
      return response.json()
    } catch (error) {
      // Return mock data when backend is offline
      return {
        status: 'offline',
        neural_load: '0%',
        processing: '0 GHz',
        memory: '0 GB',
        connection: 'Offline'
      }
    }
  },

  async getProfile() {
    const response = await fetch(`${API_BASE}/profile`)
    return response.json()
  },

  async getConversations(): Promise<ConversationEntry[]> {
    const response = await fetch(`${API_BASE}/conversations`)
    return response.json()
  },

  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
      signal: AbortSignal.timeout(60000)
    })
    if (!response.ok) throw new Error('Failed to send message')
    return response.json()
  },

  connectVoiceWebSocket(): WebSocket {
    return new WebSocket('ws://localhost:8000/ws/voice')
  }
}