import { motion } from 'framer-motion'
import { Music, Globe, Search, Terminal, FileText, Zap } from 'lucide-react'
import { useEffect, useState } from 'react'

interface Skill {
  id: string
  name: string
  description: string
}

interface SkillsPanelProps {
  onExecuteSkill: (skillId: string, query: string) => void
}

export default function SkillsPanel({ onExecuteSkill }: SkillsPanelProps) {
  const [skills, setSkills] = useState<Skill[]>([])

  useEffect(() => {
    // Fetch available skills
    fetch('http://localhost:8000/api/skills')
      .then(res => res.json())
      .then(data => setSkills(data.skills))
      .catch(err => console.error('Failed to fetch skills:', err))
  }, [])

  const getSkillIcon = (skillId: string) => {
    switch (skillId) {
      case 'play_music': return Music
      case 'open_website': return Globe
      case 'search_web': return Search
      case 'open_application': return Terminal
      case 'file_operations': return FileText
      default: return Zap
    }
  }

  const getSkillColor = (index: number) => {
    const colors = [
      'text-cyber-blue',
      'text-cyber-purple',
      'text-cyber-pink',
      'text-cyber-green',
      'text-cyber-orange'
    ]
    return colors[index % colors.length]
  }

  return (
    <div className="glass-panel rounded-2xl p-4 sm:p-6 h-full flex flex-col gap-4 overflow-y-auto">
      <h2 className="text-lg sm:text-xl font-bold text-cyber-purple uppercase tracking-wider" style={{ fontFamily: 'var(--font-orbitron)' }}>
        AI Skills
      </h2>

      <div className="flex-1 space-y-3">
        {skills.map((skill, index) => {
          const Icon = getSkillIcon(skill.id)
          const color = getSkillColor(index)
          
          return (
            <motion.div
              key={skill.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-purple/20 hover:border-cyber-purple/50 transition-all cursor-pointer group"
              onClick={() => {
                const query = prompt(`Enter command for ${skill.name}:`)
                if (query) {
                  onExecuteSkill(skill.id, query)
                }
              }}
            >
              <div className="flex items-start gap-3">
                <div className={`p-2 rounded-lg bg-black/50 ${color} flex-shrink-0 group-hover:scale-110 transition-transform`}>
                  <Icon size={18} className="sm:w-5 sm:h-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`text-sm sm:text-base font-semibold ${color} truncate`}>{skill.name}</p>
                  <p className="text-[10px] sm:text-xs text-gray-400 mt-1">{skill.description}</p>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Quick Actions */}
      <div className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-purple/20">
        <h3 className="text-xs sm:text-sm font-semibold text-cyber-purple mb-3 uppercase tracking-wider">Quick Actions</h3>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => onExecuteSkill('play_music', 'play relaxing music')}
            className="px-3 py-2 bg-cyber-blue/20 border border-cyber-blue/50 rounded-lg text-cyber-blue text-xs hover:bg-cyber-blue/30 transition-all"
          >
            Play Music
          </button>
          <button
            onClick={() => onExecuteSkill('search_web', 'search latest AI news')}
            className="px-3 py-2 bg-cyber-green/20 border border-cyber-green/50 rounded-lg text-cyber-green text-xs hover:bg-cyber-green/30 transition-all"
          >
            Search Web
          </button>
          <button
            onClick={() => onExecuteSkill('open_application', 'open calculator')}
            className="px-3 py-2 bg-cyber-purple/20 border border-cyber-purple/50 rounded-lg text-cyber-purple text-xs hover:bg-cyber-purple/30 transition-all"
          >
            Calculator
          </button>
          <button
            onClick={() => onExecuteSkill('open_application', 'open notepad')}
            className="px-3 py-2 bg-cyber-pink/20 border border-cyber-pink/50 rounded-lg text-cyber-pink text-xs hover:bg-cyber-pink/30 transition-all"
          >
            Notepad
          </button>
        </div>
      </div>

      {/* Usage Tips */}
      <div className="glass-panel rounded-xl p-3 sm:p-4 border border-cyber-purple/20">
        <h3 className="text-xs sm:text-sm font-semibold text-cyber-purple mb-2 uppercase tracking-wider">Usage Tips</h3>
        <div className="space-y-1 text-[10px] sm:text-xs text-gray-400">
          <p>• Type "play [song name]" to play music</p>
          <p>• Type "open [website]" to browse</p>
          <p>• Type "search [query]" to search web</p>
          <p>• Click skills above for quick access</p>
        </div>
      </div>
    </div>
  )
}