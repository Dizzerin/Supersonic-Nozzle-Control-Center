# Supersonic Nozzle Lab GUI
This is a Graphical User Interface (GUI) and Control Center for the Supersonic Nozzle Lab Experiment at Walla Walla University.

This project is written in python (because it was originally desired to be cross platform) and uses DearPyGUI for its UI.  This project also relies on a LabJack UE9 Pro ADC and a USB camera module.

The lab experiment requires screen recording functionality.  Sadly DearPyGUI does not support this, so the third-party free program [OBS Studio](https://obsproject.com) is recommended to fulfill this requirement.

To read the full project paper, see [Final Paper.pdf](Reference%20Materials/Full%20Project%20Paper%20and%20Documentation/Final%20Paper.pdf).

---
## Installation Guide For Lab Use
To install this software for use in the Fluid's lab, the following steps should be taken:
1. Ensure Python 3.10 is installed on the system, if not, install it.
2. Download the "[Main Code](Main%20Code)" directory from this repository.
    * This can be done by just downloading a zip of the directory directly from GitHub, or...
    * You can clone just the "Main Code" subdirectory within this repository use the following commands:
        ```shell script
        mkdir <your_chosen_path>
        cd <your_chosen_path>
        git clone -n --depth=1 --filter=tree:0 https://github.com/Dizzerin/Supersonic-Nozzle-Control-Center
        cd Supersonic-Nozzle-Control-Center
        git sparse-checkout set --no-cone "Main Code"
        git checkout
        ```
3. Install the necessary python package dependencies
    * This can be done by opening a terminal window and running:
   ``pip install -r requirements.txt``.
4. Download and install the drivers for the LabJack UE9 Pro ADC
    * The standalone LabJack ADC driver required for this program to run properly and communicate with the LabJack ADC can be downloaded from [here](https://support.labjack.com/docs/windows-setup-basic-driver-only).  (Note this installer supports silent install parameters etc.!)
      * [Direct download link](https://support.labjack.com/__attachments/49547062/labjackbasic-2019-05-20.exe?inst-v=53c3afbe-b679-4ae4-ad8c-e895cddff14e) 
    * Or, if desired, you can download the full LabJack UD software package [here](https://support.labjack.com/docs/ud-software-installer-downloads-u3-u6-ue9).  This full package installer includes several graphical programs that can be used to interface directly with the LabJack ADC.  This is not necessary for this project as this project only requires the driver
        * [Direct download link](https://files.labjack.com/installers/LJM/Windows/x86_64/release/LabJack_2024-05-16.exe)
5. Download and install [OBS Studio](https://obsproject.com) for screen recording
    * Download OBS Studio [here](https://obsproject.com/download).
        * [Direct download link](https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.2.3-Windows-Installer.exe)
6. The setup is now complete! Run "[main.py](Main%20Code/main.py)" and make sure everything works!
    * Basic Operation Verification Steps (if desired):
      * Ensure a new sessions can be run without any obvious errors.
      * Ensure the live camera feed is working.
      * Ensure the live graphs/data feed is working.
      * Ensure the system can be calibrated.
      * Ensure data can be logged and captured to a *.csv file and ensure the data is in the file.
7. Final Setup Steps:
   * Create a shortcut to run "[main.py](Main%20Code/main.py)" with the necessary permissions etc. and place the shortcut on the desktop.
   * Download the "[Icon 1.ico](Image%20Resources/Icons/Icon%201.ico)" file (or some other icon if desired).
   * Set the icon of the shortcut to the desired icon.

If the program fails to run, try running the python file as an administrator or try placing the executable in a directory which does not require administrator privileges to read and write from.

---
## Instructions for screen recording in OBS Studio
1. Launch program.
2. Under the "Sources" section at the bottom click the "+" and then select "Display Capture".
3. Ensure there is at least 1 scene added under scene, if there are none, add one.
4. Click "Start Recording".
   * (Optionally you can also configure a hot key to start and stop recording).
5. When done click "Stop Recording".  The recording will be saved to the user's "Videos" folder by default.  However this can be changed in the settings if desired.  The video output format etc. can also be configured there if desired.

---
## Notes for Developers
### General coding guidelines and design principles
* Where docstrings are used, they should follow the [Sphinx](https://www.sphinx-doc.org/en/master/) and reStructuredText (reST) format as defined by the
       [PEP 287 standard](https://www.python.org/dev/peps/pep-0287/).
* Try to maintain a good [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns)
* Try to follow the [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principle
* Try to apply [Clean Code Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) design pattern principles

See the documentation in the [Final Paper.pdf](Reference%20Materials/Full%20Project%20Paper%20and%20Documentation/Final%20Paper.pdf) starting on page 46 for more information about this software package and its design principles.
See also the [system architecture diagrams](Reference%20Materials/Software%20Diagrams/Architecture%20Diagrams).

#### Naming conventions:
* ALL_CAPS for constants/globals
* UpperCamelCase for classes
* I – indicates interface for a class
* snake_case for functions and variables
* _ prefix indicates private member variable or function?
* See naming convention guide [here](https://github.com/naming-convention/naming-convention-guides/tree/master/python)

---
### Possible future improvements
There are lots of possible future improvements that could be made to this project.  I ran out of time to complete the project the way I had originally intended and also ran into several bugs and limitations due to using python and DearPyGUI.  If one desired to, they could write a much better version of this that's only for Windows now since the project requirements have changed and that is the only OS that needs to be supported now.  This means one could use C# and the .NET framework etc. and directly tie into and use Windows native graphics which would look and operate much better and avoid several limitations I was running into.
There are also several improvements that could be made to this project or additional enhancements which are not necessary but could be nice.  I ended up removing some half-done features I was working on (such as a settings screen which allows several of the system parameters to be configured from within the application).
Some possible future enhancements:
* Implement screen recording directly within the program.
* Make it so the sample rate can be controlled from the config file.
* Make it so the sample rate can be controlled from the settings window.
* Support different camera resolutions.
* Add support for camera white balance adjustment.
* Add support for camera exposure adjustment.
* Find the actual valid range for the focus and brightness adjustments for the camera.
* Choose how many decimals of precision to have for each of the values reported on the live window and recorded in the *.csv file.
* Add a button to open an explorer window to the current directory selected as the save location
* Use an icon for the home button 
* Add custom fonts so that they can be rescaled and headings can be larger etc.  Clean up the UI so it looks a little nicer.
* Fix the window sizing issues (dependent on DearPyGUI fixing their bugs).
* Make all UI elements scale and position be relative and make it so the window size can be rescaled and is not fixed to a 1920x1080 resolution.
* Add the settings feature back in and fully implement support for it.
* Package the project into an EXE using pyinstaller, nuitka, or similar.
* Create a single installer for the project that installs all necessary dependencies such as the LabJack driver etc. as well (using something like AdvancedInstaller).
* Address all skipped todo items.
* Add better error handling.
* Clean up existing code, remove globals, follow better coding principles, etc.

### Potential Packaging Commands
The following commands could potentially be used to package the project into a single standalone EXE, though they may need to be adapted some.
#### Nuitka
```shell
python -m nuitka ^
--follow-imports ^
--include-plugin-directory=”Main Code\Image_Resources” ^
--include-plugin-files=”Main Code\config.cfg” ^
--windows-icon-from-ico=”Old\All Image Resources\Icons\Icon 1.ico” ^
--standalone ^
--product-name=”Supersonic Nozzle Control Center” ^
--output-filename=”Supersonic Nozzle Control Center.exe” ^
“Main Code\main.py”
```
Note there is also a --onefile variation of this command.

#### Pyinstaller
```shell
pyinstaller --onedir ^
--name “Supersonic Nozzle Control Center” ^
--add-data “Main Code\config.cfg:.” ^
--add-data “Main Code\Image_Resources:Image_Resources” ^
--icon “Old\All Image Resources\Icons\Icon 1.ico” ^
--windowed ^
“Main Code\main.py”
```
Note there is also a --onefile variation of this command.