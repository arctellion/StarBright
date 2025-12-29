# StarBright: Traveller Utility Suite

StarBright is a modernized, all-in-one utility suite designed for Traveller campaigns. It provides a premium, "Deep Space" themed interface for Gamemasters and Players to handle complex calculations and generation tasks with ease.

## 🚀 Key Features

### 🌌 Modern UI/UX
- **Glassmorphism Aesthetic**: Beautiful, semi-transparent "glass" cards and vibrant accent colors.
- **Responsive Navigation**: A clean side-navigation rail for switching between tools.
- **Optimized Inputs**: Custom numeric spinners and compact layouts for faster data entry.

### 💰 Commerce & Trade
- **Trade: Buy**: Generate speculative goods, passenger manifests, and freight lots (minimum 1dt) based on planet UWP.
- **Trade: Sell**: Calculate the best sale prices for your cargo, accounting for broker skills and market conditions.

### 🌍 System Generator
- **Instant World Profiling**: Generate complete Traveller 5.1 world profiles (UWP, PBG, Extensions, Bases) from any seed number.
- **Randomization**: A dedicated "Roll" button to explore infinite unique worlds.

### 🔫 GunMaker Utility
- **Modular Design**: A full weapon engineering system ported and refined for Python.
- **Real-time Statistics**: Instantly see changes to Mass, Cost, TL, and QREBS as you swap weapon types, descriptors, and modifications.
- **Advanced Modifications**: Dozens of Burdens, Stages, and Options (Laser Sights, Silencers, etc.) displayed in a clear, high-visibility list.

---

## 🛠 Internal Libraries (`travtools`)

The core logic of StarBright is powered by a set of modular Python libraries:

- **`dice.py`**: Robust dice rolling logic (2D6, Flux, etc.).
- **`converters.py`**: Extended Hexadecimal (EHex) conversion utilities for Traveller standards.
- **`qrebs.py`**: Seed-based QREBS generation and descriptive breakdown.
- **`system.py`**: Logic for UWP generation, PBG calculations, and T5.1 trade code verification.
- **`commerce.py`**: Pricing algorithms for speculative trade and freight generation.
- **`gunmaker.py`**: Comprehensive weapon design logic and chart data.

---

## 📝 To Do

* write more utility modules
* add more functionality
* extra maker tools (e.g. thingmaker, beastmaker, etc.)
* other sutff...

---

*Launch the application with:*
```bash
python app.py
```

---

## Folders

* `misc` - old and miscellaneous files
* `html_demos` - html single page applications for testing proof of concept before coding in python
* `screenshots` - screenshots of the application
* `travtools` - internal libraries
* `views` - views for the application