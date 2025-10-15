"""
OmniMind Feature Installer
Add powerful open-source features to your AI
"""

import subprocess
import sys

FEATURES = {
    "1": {
        "name": "Whisper (Better Voice Recognition)",
        "packages": ["openai-whisper"],
        "description": "Offline speech recognition, much better than Google"
    },
    "2": {
        "name": "ChromaDB (Long-term Memory)",
        "packages": ["chromadb", "sentence-transformers"],
        "description": "Remember everything forever with AI embeddings"
    },
    "3": {
        "name": "Wikipedia (Knowledge Base)",
        "packages": ["wikipedia-api"],
        "description": "Instant access to world knowledge"
    },
    "4": {
        "name": "Screen Capture (AI Sees Screen)",
        "packages": ["pillow", "mss"],
        "description": "AI can see and understand your screen"
    },
    "5": {
        "name": "Image Generation (Stable Diffusion)",
        "packages": ["diffusers", "accelerate"],
        "description": "Generate images from text descriptions"
    }
}

def install_feature(feature_id):
    feature = FEATURES.get(feature_id)
    if not feature:
        print("Invalid feature ID")
        return
    
    print(f"\nInstalling: {feature['name']}")
    print(f"Description: {feature['description']}")
    print(f"Packages: {', '.join(feature['packages'])}\n")
    
    for package in feature['packages']:
        print(f"Installing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package])
    
    print(f"\n✓ {feature['name']} installed successfully!")

def main():
    print("=" * 50)
    print("  OmniMind Feature Installer")
    print("=" * 50)
    print("\nAvailable Features:\n")
    
    for fid, feature in FEATURES.items():
        print(f"{fid}. {feature['name']}")
        print(f"   {feature['description']}\n")
    
    print("0. Install ALL features")
    print("q. Quit\n")
    
    choice = input("Select feature to install (1-5, 0 for all, q to quit): ").strip()
    
    if choice.lower() == 'q':
        return
    elif choice == '0':
        for fid in FEATURES.keys():
            install_feature(fid)
    else:
        install_feature(choice)

if __name__ == "__main__":
    main()