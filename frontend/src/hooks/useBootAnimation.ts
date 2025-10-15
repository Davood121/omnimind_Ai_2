import { useState, useEffect } from 'react'

const BOOT_COMPLETE_KEY = 'omnimind_boot_complete'

export function useBootAnimation() {
  const [showBoot, setShowBoot] = useState(true)
  const [isBooting, setIsBooting] = useState(true)

  useEffect(() => {
    // Check if boot animation has been shown in this session
    const bootComplete = sessionStorage.getItem(BOOT_COMPLETE_KEY)
    
    if (bootComplete === 'true') {
      setShowBoot(false)
      setIsBooting(false)
    }
  }, [])

  const handleBootComplete = () => {
    sessionStorage.setItem(BOOT_COMPLETE_KEY, 'true')
    setIsBooting(false)
    // Small delay before hiding to allow exit animation
    setTimeout(() => {
      setShowBoot(false)
    }, 500)
  }

  const resetBoot = () => {
    sessionStorage.removeItem(BOOT_COMPLETE_KEY)
    setShowBoot(true)
    setIsBooting(true)
  }

  return {
    showBoot,
    isBooting,
    handleBootComplete,
    resetBoot,
  }
}