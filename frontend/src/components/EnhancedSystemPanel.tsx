import { motion } from 'framer-motion'
import { Cpu, HardDrive, Wifi, Zap, Activity, Database } from 'lucide-react'
import { useEffect, useState } from 'react'

interface SystemMetric {
  label: string
  value: number
  icon: React.ReactNode
  color: string
}

interface EnhancedSystemPanelProps {
  isConnected: boolean
}

export default function EnhancedSystemPanel({ isConnected }: EnhancedSystemPanelProps) {
  const [metrics, setMetrics] = useState<SystemMetric[]>([
    { label: 'CPU', value: 0, icon: <Cpu size={18} />, color: '#00d9ff' },
    { label: 'Memory', value: 0, icon: <Database size={18} />, color: '#b537f2' },
    { label: 'Network', value: 0, icon: <Wifi size={18} />, color: '#ff006e' },
    { label: 'Storage', value: 0, icon: <HardDrive size={18} />, color: '#00ff88' },
    { label: 'GPU', value: 0, icon: <Zap size={18} />, color: '#ff6b35' },
    { label: 'Activity', value: 0, icon: <Activity size={18} />, color: '#00d9ff' }
  ])

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => prev.map(metric => ({
        ...metric,
        value: Math.min(100, Math.max(0, metric.value + (Math.random() - 0.5) * 10))
      })))
    }, 2000)

    setMetrics(prev => prev.map(metric => ({
      ...metric,
      value: 30 + Math.random() * 40
    })))

    return () => clearInterval(interval)
  }, [])

  return (
    <motion.div
      className="glass-panel rounded-xl p-4 sm:p-6 h-full flex flex-col gap-4"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="flex items-center justify-between">
        <h2 className="text-lg sm:text-xl font-bold holo-text" style={{ fontFamily: 'var(--font-orbitron)' }}>
          SYSTEM STATUS
        </h2>
        <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-cyber-green' : 'bg-red-500'} animate-pulse`} />
      </div>

      <div className="flex-1 flex flex-col gap-3 overflow-y-auto">
        {metrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            className="glass-panel rounded-lg p-3 border border-white/10"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.01 }}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <div style={{ color: metric.color }}>
                  {metric.icon}
                </div>
                <span className="text-sm font-semibold text-white">{metric.label}</span>
              </div>
              <span className="text-sm font-bold" style={{ color: metric.color }}>
                {Math.round(metric.value)}%
              </span>
            </div>
            
            <div className="relative h-2 bg-black/50 rounded-full overflow-hidden">
              <motion.div
                className="absolute inset-y-0 left-0 rounded-full"
                style={{
                  background: `linear-gradient(90deg, ${metric.color}00, ${metric.color})`,
                  boxShadow: `0 0 8px ${metric.color}`
                }}
                initial={{ width: 0 }}
                animate={{ width: `${metric.value}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </motion.div>
        ))}
      </div>

      <div className="glass-panel rounded-lg p-3 border border-cyber-blue/30">
        <div className="text-xs text-gray-400 space-y-1">
          <div className="flex justify-between">
            <span>OS Version:</span>
            <span className="text-cyber-blue">OmniMind v2.0</span>
          </div>
          <div className="flex justify-between">
            <span>Status:</span>
            <span className={isConnected ? 'text-cyber-green' : 'text-red-500'}>
              {isConnected ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  )
}