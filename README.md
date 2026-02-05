# BGA244 Binary Gas Analyzer Readout
Python code using [serial interface](https://www.pyserial.com/) to take measurements with Stanford Research Systems [BGA244](https://www.thinksrs.com/downloads/pdfs/manuals/BGA244m.pdf) Binary Gas Analyzer. The functionality is usecase related, so not all functionalities are included, but can be added following the BGA244 documentation.
## Gases
The BGA244 comes with a [factory gas table](https://www.thinksrs.com/downloads/pdfs/applicationnotes/BGA244%20Gas%20Table.pdf). Each gas can be identified by its *name* and a *CAS#*.
## Installation
First clone the repository:
```
git clone https://github.com/MaxLKP/bga244.git
```
Then install the package:
```
pip install .bga244
```
Then the functions from the BGA244 class can be used for communication with the instrument, for example on *COM3*:
```
import bga244
bga244 = bga244.BGA244("COM3")
```
## Use
A example to read the binary gas ratio is shown in bga244\bga244\bga244_example.py


