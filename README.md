# StudyStreak

An ambient, health-aware desk device designed to promote healthier work-break cycles for students and focused professionals.

-----

### Description

StudyStreak is a custom-designed desk accessory that intelligently tracks your presence to manage Pomodoro-style focus sessions. Instead of intrusive alarms or on-screen notifications, it uses a soft, color-coded ambient light and a glanceable OLED display to gently signal when it's time to work and when it's time to take a break.

### Why I Made This

As a student, I know the challenge of long, uninterrupted study sessions that lead to burnout and eye strain. I wanted to create a physical tool that could encourage healthier habits without adding to the digital distractions from phones and computers. StudyStreak is my solution: a simple, dedicated device to help maintain focus and well-being during intense work periods.

-----

## Pictures of the Project

### 3D Model & Case Design

The enclosure is a multi-part, 3D-printable case designed from scratch in Fusion 360 for ergonomics, aesthetics, and ease of assembly.

![StudyStreak 3D Model - Front View](images/studystreak-3.png)

![StudyStreak 3D Model - Side View](images/studystreak-4.png)

![StudyStreak 3D Model - Back View](images/studystreak-5.png)

![StudyStreak 3D Model - Exploded View](images/studystreak-6.png)

*The complete CAD source files (`.f3d`, `.stl`) are located in the `/case` directory.*

### PCB Design & Wiring Diagram

All electronics are integrated onto a custom 2-layer PCB designed in EasyEDA. The schematic below serves as the wiring diagram for the project.

**PCB Layout:**

![PCB Layout](images/pcb.png)

![PCB Layout with holes](images/pcb_with_holes.png)

![PCB 3D View](images/pcb_3d.png)

**Schematic:**

![Schematic Diagram](images/schematics_updated_v2.png)

*The complete EasyEDA source file (`.json`) is located in the `/hardware` directory.*

-----

## Bill of Materials (BOM)

The following table is a summary of the components required for this project, with prices including estimated shipping.

| Item No. | Part Name / Description | Qty | Estimated Total Price + shipping (USD) |
| :--- | :--- | :-- | :--- |
| 1 | ESP32 Development Board | 1 | $9.61 |
| 2 | OLED Display Module, 0.96 inch | 1 | $4.99 |
| 3 | TCRT5000 Reflective Optical Sensor Module | 1 | $3.14 |
| 4 | WS2812B Addressable RGB LEDs | 5 | $3.71 |
| 5 | TTP223 Capacitive Touch Sensor Module | 1 | $3.65 |
| | **Subtotal (Major Components)** | | **$25.10** |
| 6 | Resistor Kit (330 Ohm) | 1 | $4.24 |
| 7 | Capacitor Kit, Elyt., 100uF (\>=10V) | 1 | $4.81 |
| 8 | Micro USB cable | 1 | $3.66 |
| 9 | Solderless Breadboard | 1 | $6.80 |
| 10 | Jumper Wires Assortment | 2 | $4.43 |
| 11 | Soldering Iron & Multimeter Repair Kit | 1 | $25.63 |
| | **Subtotal (Passives & Prototyping)** | | **$49.57** |
| | **GRAND TOTAL (ESTIMATE)** | | **$74.67** |

*A complete `BOM.csv` file is available in the root directory of this repository.*

-----

*Acknowledgement: AI assisted in writing readme.md*