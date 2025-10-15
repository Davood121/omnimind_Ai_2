import { Cpu, Activity, Database, Wifi, HardDrive, Zap, Thermometer } from 'lucide-react'
import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { api, type SystemStatus as SystemStatusType } from '@/services/api'

interface SystemPanelProps {
  isConnected: boolean
}

interface DetailedStats {
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
}

export default function SystemPanel({ isConnected }: SystemPanelProps) {
  const [systemStatus, setSystemStatus] = useState<SystemStatusType | null>(null)
  const [detailedStats, setDetailedStats] = useState<DetailedStats | null>(null)

  useEffect(() => {
    if (!isConnected) return

    const fetchStatus = async () => {
      try {
        const status = await api.getStatus()
        setSystemStatus(status)
        if (status.detailed) {
          setDetailedStats(status.detailed as DetailedStats)
        }
      } catch (error) {
        console.error('Failed to fetch system status:', error)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 2000) // Update every 2 seconds

    return () => clearInterval(interval)
  }, [isConnected])

  const metrics = [
    { 
      icon: Cpu, 
      label: 'CPU Usage', 
      value: systemStatus?.neural_load || '0%', 
      color: 'text-cyber-blue',
      detail: detailedStats ? `${detailedStats.cpu.cores} cores` : ''
    },
    { 
      icon: Activity, 
      label: 'Frequency', 
      value: systemStatus?.processing || '0 GHz', 
      color: 'text-cyber-green',
      detail: ''
    },
    { 
      icon: Database, 
      label: 'Memory', 
      value: systemStatus?.memory || '0 GB', 
      color: 'text-cyber-purple',
      detail: detailedStats ? `${detailedStats.memory.usage_percent}% used` : ''
    },
    { 
      icon: HardDrive, 
      label: 'Disk', 
      value: detailedStats ? `${detailedStats.disk.free_gb} GB free` : 'N/A', 
      color: 'text-cyber-orange',
      detail: detailedStats ? `${detailedStats.disk.usage_percent}% used` : ''
    },
    { 
      icon: Wifi, 
      label: 'WiFi Signal', 
      value: detailedStats?.wifi_signal ? `${detailedStats.wifi_signal}%` : 'N/A', 
      color: detailedStats?.wifi_signal && detailedStats.wifi_signal > 70 ? 'text-cyber-green' : 
             detailedStats?.wifi_signal && detailedStats.wifi_signal > 40 ? 'text-cyber-orange' : 'text-red-500',
      detail: isConnected ? 'Connected' : 'Offline'
    }
  ]

  // Add battery if available
  if (detailedStats?.battery) {
    metrics.push({
      icon: Zap,
      label: 'Battery',
      value: `${detailedStats.battery.percent}%`,
      color: detailedStats.battery.plugged_in ? 'text-cyber-green' : 
             detailedStats.battery.percent > 20 ? 'text-cyber-blue' : 'text-red-500',
      detail: detailedStats.battery.plugged_in ? 'Charging' : 'On Battery'
    })
  }

  // Add temperature if available
  if (detailedStats?.temperature) {
    metrics.push({
      icon: Thermometer,
      label: 'Temperature',
      value: `${detailedStats.temperature.current_celsius}°C`,
      color: detailedStats.temperature.current_celsius > 80 ? 'text-red-500' :
             detailedStats.temperature.current_celsius > 60 ? 'text-cyber-orange' : 'text-cyber-blue',
      detail: detailedStats.temperature.sensor
    })
  }

  return (
    <div className="glass-panel rounded-2xl p-4 sm:p-6 h-full flex flex-col gap-4 overflow-y-auto">
      <h2 className="text-lg sm:text-xl font-bold text-cyber-blue uppercase tracking-wider" style={{ fontFamily: 'var(--font-orbitron)' }}>
        System Status
      </h2>

      <div className="flex-1 space-y-3 sm:space-y-4">
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-blue/20 hover:border-cyber-blue/50 transition-all"
          >
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg bg-black/50 ${metric.color} flex-shrink-0`}>
                <metric.icon size={18} className="sm:w-5 sm:h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[10px] sm:text-xs text-gray-400 uppercase tracking-wider truncate">{metric.label}</p>
                <p className={`text-base sm:text-lg font-semibold ${metric.color} truncate`}>{metric.value}</p>
                {metric.detail && (
                  <p className="text-[9px] sm:text-[10px] text-gray-500 truncate">{metric.detail}</p>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Network Stats */}
      {detailedStats?.network && (
        <div className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-blue/20">
          <h3 className="text-xs sm:text-sm font-semibold text-cyber-blue mb-2 uppercase tracking-wider">Network</h3>
          <div className="grid grid-cols-2 gap-2 text-[10px] sm:text-xs">
            <div>
              <p className="text-gray-400">Sent</p>
              <p className="text-cyber-green font-semibold">{detailedStats.network.bytes_sent_mb.toFixed(1)} MB</p>
            </div>
            <div>
              <p className="text-gray-400">Received</p>
              <p className="text-cyber-purple font-semibold">{detailedStats.network.bytes_recv_mb.toFixed(1)} MB</p>
            </div>
          </div>
        </div>
      )}

      {/* Top Processes */}
      {detailedStats?.top_processes && detailedStats.top_processes.length > 0 && (
        <div className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-blue/20">
          <h3 className="text-xs sm:text-sm font-semibold text-cyber-blue mb-2 uppercase tracking-wider">Top Processes</h3>
          <div className="space-y-1 text-[10px] sm:text-xs">
            {detailedStats.top_processes.slice(0, 3).map((proc, i) => (
              <div key={i} className="flex justify-between text-gray-400">
                <span className="truncate flex-1">{proc.name}</span>
                <span className="text-cyber-orange ml-2">{proc.cpu_percent}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Activity Log */}
      <div className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-blue/20">
        <h3 className="text-xs sm:text-sm font-semibold text-cyber-blue mb-3 uppercase tracking-wider">Recent Activity</h3>
        <div className="space-y-2 text-[10px] sm:text-xs">
          {[
            isConnected ? 'Backend connected' : 'Backend offline',
            'Real-time monitoring active',
            'Neural network operational',
            'System metrics updating',
            'All systems nominal'
          ].map((log, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: i * 0.2 + 0.5 }}
              className="flex items-center gap-2 text-gray-400"
            >
              <div className={`w-1 h-1 rounded-full ${i === 0 && !isConnected ? 'bg-red-500' : 'bg-cyber-green'} animate-pulse flex-shrink-0`} />
              <span className="truncate">{log}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}