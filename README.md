# Osdag.exe

### Frame & Components

The installer setup file is: osdag_installer_win64.exe within this repo which you'll find at Output/osdag_installer_win64.exe.

Make sure the .exe setup file is run from the primary storage of the computer and not from a secondary storage device, like a pendrive, external hdd/ssd.
The installation script is essentially written in Python and has 3 main components (helper functions). The user must have an active internet connection during installation.

1. **TinyTeX Installation**  
   Firstly, the installer installs TinyTeX, a lightweight alternative to MikTeX, which already consists of most of the required packages for Osdag (to generate PDF reports). The necessary packages which are not inherently present with TinyTeX are installed programmatically. TinyTeX is also fetched from its GitHub release, making the installer future-proof for this component too.

   TinyTex Release: https://github.com/rstudio/tinytex-releases/releases/

3. **Miniconda Installation**  
   Second, it installs Miniconda in the user’s computer only for the current user. The function has been designed to always download the latest version of Miniconda3 from the official link of the releases. By doing so, the installer always remains future-proof, no matter when it is used.

   Miniconda Release: https://repo.anaconda.com/miniconda/

5. **Osdag Installation**  
   After TinyTeX with its packages and Miniconda are configured, the installer creates a conda environment and installs Osdag, using
   `conda activate && conda create -n osdag-env osdag::osdag -c conda-forge`

## Working

1. The script downloads the latest version of Miniconda and installs it in the `{Userprofile}` directory. It also adds conda to the system path.

2. The TinyTeX installation, conducted using the `install_tinytex()` function in the tinytex_prog_logic.exe file, consists of 3 methods as fallback mechanisms in case of a failure of any one:

   - **System.Net.WebClient**
   - **Invoke-WebRequest**
   - **System.Net.Http.HttpClient**

   The logic was derived from the `install_bin_windows.bat` file available on the official TinyTeX release website (Included in this repo).  
   It extracts the TinyTeX files to `Appdata/Roaming/TinyTeX` and adds `tlmgr` to the system path. The script runs TinyTeX installation in a separate shell so that the path is added globally for all instances. After that, when the user clicks on Finish, Miniconda and Osdag are installed.

3. **Osdag Installation**  
   Osdag is installed as a conda environment through the initially installed Miniconda3 `conda.bat` file. The installer is again future-proof. In the event of future updates of Osdag, new users will be able to install the latest version, and prior users can either update using the command line or a new feature can be integrated to automatically check for updates and install the latest version.

## Testing

A sample generation of each design was run.

All designs were generated using TinyTeX and the additional required packages, namely:

- `lastpage`
- `parskip`
- `needspace`
- `fancyhdr`
- `colortbl`
- `multirow`

All generated PDFs can be found in the ‘All Design Trials’ folder within the repo.

## NOTE

When generating a PDF of a design within Osdag that is unsafe or not following the standard protocol of the design (in any manners such as material, section, etc.), it was noticed that generally for these cases it results in a dialog box that says “Latex Creation Error” but the PDF was generated successfully in the location set by the user.

Though less likely, there were instances where clicking on Create Design Report, for a safe design in Osdag resulted in a dialog box which said 'Latex Creation Error', even though the file was successfully generated in the location set by the user.

## Ambiguities & Steps Taken to Resolve

In the event of running the installer on WiFi networks with their own security features or restrictions enabled (e.g., University/College WiFi networks), the installer might fail to install Osdag through the conda channel on the first attempt but may install successfully on successive attempts. This is a specific occurrence only on public networks with high traffic and restrictions enabled.

To resolve this, the installer will try to install Osdag in a loop for 10 attempts until `success = True`.

If, even after 10 attempts, the installer fails to install Osdag, it exits the loop and prompts the user to check their network.

On private networks with a stable internet connection, the installer works flawlessly.
