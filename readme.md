# StarBright: Traveller Utility Suite

StarBright is a modernized, all-in-one utility suite designed for Traveller campaigns. It provides a premium, "Deep Space" themed interface for Gamemasters and Players to handle complex calculations and generation tasks with ease.

The application has been recently migrated to **PyQt6** for enhanced stability and a true desktop experience.

## 🚀 Key Features

### 🌌 Modern UI/UX (PyQt6)
- **Glassmorphism Aesthetic**: Beautiful, semi-transparent "glass" frames and vibrant accent colors.
- **Desktop Navigation**: Standard Menu Bar for intuitive access to all tools.
- **Optimized Inputs**: Custom numeric spinners and compact layouts for faster data entry.

### 🎲 Dice Utility
- **Dice Roller**: Quick-roll buttons for standard difficulties (Easy to Impossible).
- **Flux Rolls**: Dedicated support for Flux (2d6-7) calculations.
- **Custom Rolls**: Full string-based roll parsing (e.g., `2d6+3`).

### 💰 Commerce & Trade
- **Buying**: Generate speculative goods, passenger manifests, and freight lots based on planet UWP.
- **Selling**: Calculate the best sale prices for your cargo, accounting for broker skills and market conditions.

### 🌍 Galaxy Engine
- **System Generator**: Instant Traveller 5.1 world profiles (UWP, PBG, Extensions, Bases).
- **Subsector Generator**: Generate 8x10 hex-grid equivalent subsectors.
- **Sector Generator**: Generate complete sectors consisting of 16 subsectors. (to do..)

### 🔫 Maker Tools (Guns & Armour)
- **GunMaker**: Comprehensive weapon engineering system with real-time stats (Mass, Cost, TL, QREBS).
- **ArmourMaker**: Modular armor design with subsystem tracking and drawbacks.

---

## 🛠 Internal Libraries (`travtools`)

The core logic of StarBright is powered by a set of modular Python libraries:

- **`dice.py`**: Robust dice rolling logic (2D6, Flux, etc.).
- **`converters.py`**: Extended Hexadecimal (EHex) conversion utilities.
- **`qrebs.py`**: Seed-based QREBS generation and breakdown.
- **`system.py`**: UWP generation, PBG calculations, and Sector/Subsector logic.
- **`commerce.py`**: Pricing algorithms for speculative trade and freight.
- **`gunmaker.py`**: Weapon design logic and chart data.
- **`armourmaker.py`**: Armor calculation and subsystem datasets.
- **`names.py`**: Name generation logic.
- **`names_data.json`**: Name data for name generation.
- **`travel.py`**: Travel time and distance calculations.

---

## TODO ..

* Check gunmaker/armourmaker logic to ensure it matches the rules.
* Add more makers: Thingmaker, Vehiclemaker, Beastmaker, etc.
* Add more tools: Task manager, interpersonal task creator, etc.
* Add planet mapper
* Character creator
* Add more polish and bling..

---

## 📦 Requirements

To run StarBright, the following Python modules are required:

```bash
pip install PyQt6 numpy
```

---

## 🏃 Launching the Application

Launch the modern PyQt6 interface with:

```bash
python main_qt.py
```

---

## 📁 Project Structure

* `main_qt.py` - Primary application entry point (PyQt6).
* `travtools/` - Core logic and calculation libraries.
* `views/` - UI view implementations (prefixed with `_qt` for the modern version).
* `screenshots/` - Visual previews of the application.
