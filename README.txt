
# CMG ATLAS Restart Overlay Plugin – Standalone GUI + GitHub Sync + Discord Integration

This Chaotic Minds Gaming (CMG) toolkit is a solution for managing your ATLAS server's restart countdown, grid status, and integration with GitHub and Discord.

## 🛠️ What’s Inside:

- `launch_gui.exe` – Standalone executable for managing your restart countdown, grid status, and server sync
- `index.html` / `style.css` / `overlay.js` – Overlay for GitHub Pages or Google Sites
- `restart-time.json` – JSON used by the overlay (live countdown data)
- `auto_push_restart_json.py` – Auto-pushes the JSON to your GitHub every 60 seconds
- `push_restart_json.bat` – Manual GitHub push for `restart-time.json`
- `README.txt` – Complete step-by-step guide for setup

## 📦 Setup & Instructions:

### Step 1: Install Requirements
1. **Install Python (if not already installed):**
   - [Download Python](https://www.python.org/downloads/)

2. **Install PyInstaller for building the executable:**
   - Open a Command Prompt (CMD) and run:
     ```bash
     pip install pyinstaller
     ```

3. **Install Required Python Libraries:**
   - Open a Command Prompt (CMD) and run:
     ```bash
     pip install flask pystray rcon requests
     ```

### Step 2: Build the `.exe` File
1. **Download the Full Toolkit** from the zip file:  
   [Download CMG ATLAS Restart Overlay Plugin](sandbox:/mnt/data/chaotic-atlas-restart-toolkit.zip)

2. **Extract the zip** to a folder, e.g., `C:tlas-restart-toolkit`.

3. **Navigate to the folder** where you extracted the files and run:
   ```bash
   cd C:tlas-restart-toolkit
   pyinstaller --onefile --windowed launch_gui.py
   ```

4. **Wait for PyInstaller to finish**. The `.exe` will be located in the `dist` folder (`launch_gui.exe`)

### Step 3: Run the `.exe` File
1. **Test the executable** by double-clicking `launch_gui.exe`:
   - The GUI will open and allow you to start the countdown, update the grid status, and sync to GitHub.
   - You can manually edit `restart-time.json` and push updates to GitHub with the buttons.

2. **Test GitHub Push:**
   - Ensure the `.bat` or Python script pushes the updated `restart-time.json` to GitHub.

### Step 4: Embed Overlay in Google Sites or GitHub Pages
1. **Upload** the `index.html`, `style.css`, and `overlay.js` files to your GitHub repository.
2. **Enable GitHub Pages** in your repository settings, and link the GitHub Pages URL to your Google Sites.

### Step 5: Optional - Auto-Start on Windows
1. **Create a shortcut** to `launch_gui.exe` in the **Startup** folder:
   - Press `Windows+R`, type `shell:startup`, and hit Enter.
   - Create a shortcut to `launch_gui.exe` in the **Startup** folder.

---

## 🔗 Useful Links:
- [Download Python](https://www.python.org/downloads/)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [GitHub Pages Setup](https://docs.github.com/en/pages/getting-started-with-github-pages)
- [Google Sites](https://sites.google.com/)

### 💡 Support
- If you run into any issues during the build or setup, feel free to reach out for additional help.
