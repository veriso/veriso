VeriSO
======

* Einstellungen QGIS... (Plastique etc.)
* Konventionen:
 - VeriSOModule.. dann weiter veriso_ee weiter fp3...
 - falls locale nicht vorhanen, wird erster eintrag verwendet.

* nach erstellen von neuen tests muss mit linguist neu übersetzt werden.

* das was bereits im quellcode deutsch ist, müsste für DE nicht übersetzt werden, da dann das als default verwendet wird (?)


* svg in installationsverzeichnis kopieren... ist am einfachsten.

ACHTUNG: wie genau workflow wenn neu übersetzen (also zusätzlich)?


LINGUIST:
* veriso.pro Datei erstellen
* pylupdate4 veriso.pro:
 - im Verzeichnis i18/ sind *.ts Dateien.
* linguist i18n/veriso_de.ts i18n/veriso_fr.ts
* source: POSIX / target: german (any) resp. french (any) -> gibt gleich zwei felder für zwei sprachen... cool
* Mit gelben Pfeilen (next item) zum nächsten.
* Save all..
* File - Release All
