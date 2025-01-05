# Required Installations

1. Install Python and pip
2. Install Pylance extension in VSCode
3. Install the micropython-esp32-stubs e.g. `pip install micropython-esp32-stubs`
4. Install [PyMakr](https://marketplace.visualstudio.com/items?itemName=Pycom.pymakr) extension (for eventually installing onto actual ESP32 board)
5. Install the [Wokwi for VS Code](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode) extension.
6. Install the [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) tool, e.g. `pip install mpremote`.
7. Create a `main.py` file in the project root
8. Create a `diagram.json` file in the project root
9. Create a `wokwi.toml` file in the project root
10. Add the following to your `wokwi.toml`:
```
[wokwi]
version = 1
firmware = "./ESP32_GENERIC-1.24.1.bin"
elf = "./ESP32_GENERIC-1.24.1.elf"
rfc2217ServerPort = 4000

```

11. If necessary, add some settings to VSCode by adding `.vscode/settings.json` to the project root and adding this code to it (double-check your own computer's file path wherever the `/site-packages` directory is located; use Warp's terminal to help):
```
{
    "python.analysis.extraPaths": [
        "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages"
    ],
    "python.languageServer": "Pylance",
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingModuleSource": "none"
    }
}
```
12. Use the `diagram.json` file to create your hardware setup and create connections to the ports on the ESP32 board
13. Write your program in `main.py`

# To Run the Wokwi Simulator with MicroPython code
1. Use `CMD+Shift+P` to open the VSCode command palette
2. Type `Wokwi` and choose `Wokwi: Start Simulator`
3. While the sim is runnning and keeping it visible, open another new terminal and enter `python -m mpremote connect port:rfc2217://localhost:4000 run main.py` (this loads your main.py into the sim)
4. You should see your program running in the simulator and any printed output in the wokwi simulator's terminal session

