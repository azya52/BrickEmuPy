# BrickEmuPy
Handheld LCD games emulator in Python with PyQt6.

The following handheld games are currently emulated: 
* Brick Games
  * Brick Game E-23 PLUS MARK II 96 in 1 (An [article](https://habr.com/ru/articles/773040/) describing the reverse engineering.)
  * Brick Game E-88 8 in 1
  * Brick Game E-33 2 in 1
  * Block Game & Echo Key GA888 (Tetris Jr. clone)
  * Radio Shack Stack Challenge
  * Keychain 55 in 1
  * Keychain GA-878
  * Micon KC-32
* Virtual Pets
  * Tamagotchi P1 (distributed without ROM)
  * Tamagotchi P2 (distributed without ROM)
  * Tamagotchi Mothra (distributed without ROM)
  * Tamagotchi Angle (distributed without ROM)
  * Tamagotchi Umino (distributed without ROM)
  * Tamagotchi Morino (distributed without ROM)
  * Tamagotchi Genjintch (distributed without ROM)
  * Digimon Ver. 1 (distributed without ROM)
  * Digimon Ver. 2 (distributed without ROM)
  * Digimon Ver. 3 (distributed without ROM)
  * Nikko virtual pet
  * Pocket Pikachu (distributed without ROM)
  * Mickey Deluxe Virtual Game virtual pet
  * Apollo 2 in 1 virtual pet
* Other LCD Games
  * Epoch Chibi Pachi Alien Fever
  * Formel 1 (Hartung Spiele Berlin/Epoch)
  * The Legend of Zelda Game Watch (distributed without ROM)
  * Space Intruder TK-150I
  * Mame Game Tamagotch (distributed without ROM)
  * Mame Galaxian (distributed without ROM)
  * Keychain Pin Ball
  * Hiro Pocket Boy No.2

## Compiling

### Windows

Install [Python](https://www.python.org/downloads/) and make sure to check the box that says "Add Python to PATH" during installation.

Download the repository and extract it's content.

Open the cmd, then run following command to install dependencies:
```
pip install pyqt6
```
Navigate to the extracted folder and run main.py:
```
cd path\to\BrickEmuPy-main
python main.py
```

### Linux (Debian-based)

```
sudo apt install pip
pip install pyqt6 --break-system-packages
git clone https://github.com/azya52/BrickEmuPy && cd BrickEmuPy
python3 main.py
```


## Preview
<img src="https://github.com/azya52/BrickEmuPy/assets/31337838/65dc8c6c-7998-48c9-b351-383522dd8171" width=100%>
<img src="https://github.com/azya52/BrickEmuPy/assets/31337838/d8c25a9f-c2df-4ae0-add2-3d3134eb6a5e" width=100%>
