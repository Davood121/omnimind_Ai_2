"""
Real-time system monitoring module for OmniMind OS.
Provides CPU, memory, disk, network, and WiFi information.
"""

import psutil
import platform
import time
from typing import Dict, List, Optional
import subprocess
import re


class SystemMonitor:
    """Monitor system resources in real-time"""
    
    def __init__(self):
        self.cpu_percent_history: List[float] = []
        self.memory_percent_history: List[float] = []
        self.max_history = 60  # Keep last 60 readings
    
    def get_cpu_info(self) -> Dict:
        """Get CPU usage and information"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        # Update history
        self.cpu_percent_history.append(cpu_percent)
        if len(self.cpu_percent_history) > self.max_history:
            self.cpu_percent_history.pop(0)
        
        return {
            "usage_percent": round(cpu_percent, 1),
            "frequency_ghz": round(cpu_freq.current / 1000, 2) if cpu_freq else 0,
            "cores": cpu_count,
            "history": self.cpu_percent_history[-20:]  # Last 20 readings
        }
    
    def get_memory_info(self) -> Dict:
        """Get memory usage information"""
        memory = psutil.virtual_memory()
        
        # Update history
        self.memory_percent_history.append(memory.percent)
        if len(self.memory_percent_history) > self.max_history:
            self.memory_percent_history.pop(0)
        
        return {
            "usage_percent": round(memory.percent, 1),
            "used_gb": round(memory.used / (1024**3), 2),
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "history": self.memory_percent_history[-20:]
        }
    
    def get_disk_info(self) -> Dict:
        """Get disk usage information"""
        disk = psutil.disk_usage('/')
        
        return {
            "usage_percent": round(disk.percent, 1),
            "used_gb": round(disk.used / (1024**3), 2),
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2)
        }
    
    def get_network_info(self) -> Dict:
        """Get network usage information"""
        net_io = psutil.net_io_counters()
        
        return {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def get_wifi_signal_strength(self) -> Optional[int]:
        """Get WiFi signal strength (Windows only)"""
        try:
            if platform.system() == 'Windows':
                # Run netsh command to get WiFi info
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'interfaces'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    # Parse signal strength
                    for line in result.stdout.split('\n'):
                        if 'Signal' in line:
                            # Extract percentage
                            match = re.search(r'(\d+)%', line)
                            if match:
                                return int(match.group(1))
            
            # For other systems or if command fails
            return None
        except Exception:
            return None
    
    def get_battery_info(self) -> Optional[Dict]:
        """Get battery information if available"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": round(battery.percent, 1),
                    "plugged_in": battery.power_plugged,
                    "time_left_minutes": round(battery.secsleft / 60, 0) if battery.secsleft != -1 else None
                }
        except Exception:
            pass
        return None
    
    def get_temperature(self) -> Optional[Dict]:
        """Get system temperature if available"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Get first available temperature sensor
                for name, entries in temps.items():
                    if entries:
                        return {
                            "sensor": name,
                            "current_celsius": round(entries[0].current, 1),
                            "high_celsius": entries[0].high if entries[0].high else None
                        }
        except Exception:
            pass
        return None
    
    def get_process_info(self) -> List[Dict]:
        """Get top 5 processes by CPU usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    if info['cpu_percent'] > 0:
                        processes.append({
                            'name': info['name'],
                            'cpu_percent': round(info['cpu_percent'], 1),
                            'memory_percent': round(info['memory_percent'], 1)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and return top 5
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:5]
        except Exception:
            return []
    
    def get_all_stats(self) -> Dict:
        """Get all system statistics"""
        return {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "wifi_signal": self.get_wifi_signal_strength(),
            "battery": self.get_battery_info(),
            "temperature": self.get_temperature(),
            "top_processes": self.get_process_info(),
            "timestamp": time.time()
        }