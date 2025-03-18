# Coastal Defense 🌊🛡️  

A Pygame-based arcade shooter where players defend their coast by precisely aiming and shooting at incoming enemies.  

---

## ℹ️ About  

**Coastal Defense** is a fast-paced defense game where players must calculate bullet angles and take down advancing enemies before they reach the shore. As the game progresses, enemy speed increases, making precise shots even more crucial.  

---

## 📌 Project Structure  

This game was developed by:  
- **Daniela Dantas (22202104)** – Collision system, main game loop, enemy behavior, end screen, and UI design.  
- **Vitória Rodrigues (22204356)** – Bullet angle calculation and Markdown documentation.  

### Code Structure  
- **Variables & Setup**: Initializes game settings.  
- **Bullet Class**: Manages projectile behavior.  
- **Shooting Mechanism**: Handles firing logic.  
- **Main Game Loop**: Processes events, mouse interactions, and gameplay mechanics.  
- **Enemy System**: Generates enemies with increasing speed based on the player's score.  
- **Game Over Screen**: Displays the end-game interface.  

External libraries used: `numpy`, `math`, and `random`.  

---

## 🎮 Controls  

- **Aim & Shoot** – Left mouse button  
- **Quit the Game** – Close the window  

---

## 🛠️ Running the Game  

To run **Coastal Defense**, follow these steps:  

1. **Clone the repository**  
   ```sh
   git clone https://github.com/arbyun/Coastal-Defense.git
   cd Coastal-Defense
   ```

2. **Install dependencies (requires Python and Pygame)**
   ```sh
   pip install pygame numpy
   ```

3. **Run the game**
   ```sh
   python main.py
   ```

## 📜 License  

This project is licensed under the **MIT License**.  See the [LICENSE](LICENSE) file for more details.  
