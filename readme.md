# StarBright: Traveller Utility Suite

StarBright is a modernized, all-in-one utility suite designed for Traveller Campaigns. It provides a premium, "Deep Space" themed interface for Gamemasters and Players to handle complex calculations and generation tasks with ease.

The application is built using **PyQt6** for a performant and robust desktop experience.

## 🚀 Key Features

### 🌌 Modern UI/UX
- **Glassmorphism Aesthetic**: Beautiful, semi-transparent "glass" frames and vibrant accent colors.
- **Desktop Navigation**: Standard Menu Bar for intuitive access to all tools.
- **Visual Feedback**: Micro-animations, custom icons, and real-time computation.

### 🎲 Dice Utility
- **Dice Roller**: Quick-roll buttons for standard difficulties and custom rolls.
- **Flux Rolls**: Dedicated support for Flux (2d6-7) calculations.

### 💰 Commerce & Trade
- **Buying**: Generate speculative goods, passenger manifests, and freight lots based on planet UWP.
- **Selling**: Calculate best sale prices accounting for skills and market conditions.

### 🌍 Galaxy Engine
- **System Generator**: Instant Traveller 5.1 world profiles with integrated **World Mapping**.
- **Subsector & Sector Generation**: Procedurally generate 8x10 subsectors and full 16-subsector sectors with interactive hex maps.
- **Traveller Map Viewer**: Explore official sectors (M0, M1105, M1120, M1900 milieux) using local SQLite data.

### 🛠️ Maker Tools
- **GunMaker, ArmourMaker, VehicleMaker**: Comprehensive engineering systems with procedural name generation and QREBS integration.

### 🏷️ Utilities
- **Name Generator**: Advanced Markov-chain based procedural naming for characters, planets, and gear.
- **Travel Calculator**: Detailed travel time and distance computations.

---

## 🛠 Internal Libraries (`travtools`)

The core logic of StarBright is powered by modular Python libraries:
- `dice.py`, `converters.py`, `qrebs.py`, `system.py`, `commerce.py`, `gunmaker.py`, `armourmaker.py`, `vehiclemaker.py`, `names.py`, `travel.py`, `traveller_map_db.py`, `world_map_gen.py`.

---

## 📦 Requirements

```bash
pip install PyQt6 numpy
```

## 🏃 Launching the Application

```bash
python main_qt.py
```

## 📁 Project Structure

* `main_qt.py` - Application entry point.
* `travtools/` - Core logic and calculation libraries.
* `views/` - PyQt6 UI view implementations.
* `assets/` - DB and static assets.
