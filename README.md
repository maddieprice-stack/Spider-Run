# 🕷️ Spider-Run

A **Pac-Man-inspired, Spider-Man-themed maze game** with comic book cut-scenes, built with Flask and HTML5 Canvas.

## 🎮 Game Overview

Spider-Run is a comic book-styled arcade game where you play as Spider-Man helping Dr. Strange clean up spilled space dust across New York City. The game features:

- **Comic Book Visual Style**: Bold outlines, halftone textures, vibrant colors
- **Interactive Comic Cut-Scenes**: Click-through dialogue with Dr. Strange and Spider-Man
- **Page-Flip Transitions**: Smooth comic book page-turning animations
- **Pac-Man-Inspired Gameplay**: Collect dust, avoid enemies, use power-ups

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game**:
   ```bash
   python run.py
   ```

3. **Open your browser** and go to: `http://localhost:8081`

## 🎯 Current Features

### ✅ Implemented
- **Title Screen**: Comic cover style with Start Game and Instructions buttons
- **Comic Intro Sequence**: 7-panel interactive story with Dr. Strange and Spider-Man
- **Page-Flip Animations**: Smooth transitions between comic panels
- **Comic Book Styling**: Bold borders, halftone backgrounds, speech bubbles
- **Click-Through Dialogue**: Advance story by clicking or pressing Enter/Space
- **Placeholder Game Canvas**: Ready for gameplay implementation

### 🎨 Visual Style
- **Bold Black Outlines**: Classic comic book aesthetic
- **Halftone Textures**: Dot patterns for authentic comic feel
- **Vibrant Color Palette**: Red, blue, yellow, and green primary colors
- **Speech Bubbles**: Comic-style dialogue presentation
- **Comic Sans Font**: Authentic comic book typography

## 📖 Comic Intro Story

The intro sequence follows the exact script from the PRD:

0. **Spider-Man**: "Hi Dr. Strange!"
1. **Dr. Strange**: "Spider-Man! I need your help — I've spilled space dust all over New York City!"
2. **Spider-Man**: "What's a little more dust on the streets? We've seen worse."
3. **Dr. Strange**: "This dust isn't ordinary, Spider-Man. If left unchecked... it could END THE WORLD!"
4. **Spider-Man**: "...Okay, okay. Guess I'll grab a broom."
5. **Dr. Strange**: "The dust is scattered across the East Village — start there before it spreads any further!"
6. **Dr. Strange**: "Be careful, Spider-Man. Some of your enemies are out tonight."

## 🎮 Controls

- **Click** or **Enter/Space**: Advance through comic panels
- **Mouse**: Navigate menus and buttons
- **ESC**: (Future) Pause game

## 🔧 Technical Details

### Architecture
- **Backend**: Flask web server
- **Frontend**: HTML5 Canvas + JavaScript
- **Styling**: CSS3 with comic book aesthetics
- **Animations**: CSS keyframes for page-flip effects

### File Structure
```
hackathon/
├── run.py              # Main game server
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── static/            # Future game assets
└── Docs/              # Game design documents
    ├── Overall PRD.md
    ├── Intro Comic.md
    └── Level 2 Board Layout.md
```

### Game States
1. **Title Screen**: Main menu with comic cover styling
2. **Comic Intro**: 6-panel interactive story sequence
3. **Gameplay**: (Future) Level 1 East Village maze
4. **Cut-Scenes**: (Future) Between-level story panels

## 🎨 Style References

The game's visual style is inspired by classic comic books, featuring:
- **Dr. Strange**: Red cloak, blue tunic, magical poses
- **Spider-Man**: Red and blue suit, dynamic action poses
- **Comic Panels**: Bold borders, halftone shading, splash panels
- **Typography**: All-caps, bold, comic-style lettering

## 🚧 Future Development

### Next Steps
- [ ] Implement Level 1 gameplay (East Village maze)
- [ ] Add grid-based movement system
- [ ] Create enemy AI and collision detection
- [ ] Implement power-up system (Strange Orbs)
- [ ] Add scoring and lives system
- [ ] Create Level 2 (Times Square)
- [ ] Add sound effects and music

### Asset Integration
- [ ] Replace placeholder character images with proper sprites
- [ ] Add background music and sound effects
- [ ] Create animated character sprites
- [ ] Design level-specific backgrounds

## 🎯 Game Design

Based on the comprehensive PRD documents:
- **Core Gameplay**: Pac-Man-style maze navigation
- **Objectives**: Collect space dust, avoid enemies, use power-ups
- **Progression**: Comic cut-scenes → Level 1 → Cut-scene → Level 2 → Finale
- **Style**: Comic book brought to life with modern web technology

## 🐛 Known Issues

- Placeholder art is currently used for characters
- Sound effects are console-logged placeholders
- Gameplay canvas shows placeholder elements

## 📝 License

This is a hackathon project created for educational and entertainment purposes.

---

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/maddieprice-stack/Spider-Run.git
   cd Spider-Run
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python run.py
   ```

4. **Open your browser** and go to: `http://localhost:8081`

## 🤝 Contributing

This is a hackathon project, but contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve the comic book styling

## 📄 License

This project is created for educational and entertainment purposes.

---

**Ready to swing into action? Run `python run.py` and start your Spider-Run adventure!** 🕷️✨


