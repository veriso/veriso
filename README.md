VeriSO
======
 
VeriSO is a QGIS plugin for verifying cadastral surveying data in Interlis format.

It was originally developed by Stefan Ziegler for the canton of Solothurn.

 
Dependencies
------------

VeriSO requires the Qt PostgreSQL database driver (Ubuntu package `libqt5sql5-psql`) and the Python modules XlsxWriter (Ubuntu package `python3-xlsxwriter`) and Openpyxl (Ubuntu package `python3-openpyxl`).

Usage
-----

Available verification modules are located in the folder `modules`. You can download modules from https://github.com/veriso/ and unpack them in `modules`.

The checks are loaded dynamically in alphabetical order from each check folder.

To add your own modules you have to add a folder into veriso/modules, its content should be based on `templates/template_module`
