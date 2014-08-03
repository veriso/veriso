VeriSO
======

* Grundstruktur VerisO. andere Fachschalen möglich. z.B. nplanung oder auch erfassung. 

* Einstellungen QGIS... (Plastique etc.)
* Konventionen:
 - VeriSOModule.. dann weiter veriso_ee weiter fp3...
 - falls locale nicht vorhanen, wird erster eintrag verwendet.

* nach erstellen von neuen tests muss mit linguist neu übersetzt werden.

* das was bereits im quellcode deutsch ist, müsste für DE nicht übersetzt werden, da dann das als default verwendet wird (?)


* svg in installationsverzeichnis kopieren... ist am einfachsten.


* qgis tables json -> beispiel properties und java aufruf.

ACHTUNG: wie genau workflow wenn neu übersetzen (also zusätzlich)?

* erwähnen, dass v.a. kategorisierte Legenden (z.b. Vermarkungsart oder TS1) event. zsuätzlich gemacht werden müssen.
* Multilingual-Legenden: es wird "_fr" angehängt. Aber keine Fallbackebene. Dh. wenn im ComplexCheck die Legende mit Sprache angegeben wird, muss das QML auch vorhanden sein.

* Erläutern wie mängel tabelle funktioniert und wie multilingual.

LINGUIST:
* Modulname als Kontext bei ApplicationModule und Modulname_ComplexCheckFile bei ComplexCheck

* veriso.pro Datei erstellen
* pylupdate4 veriso.pro:
 - im Verzeichnis i18/ sind *.ts Dateien.
* linguist i18n/veriso_de.ts i18n/veriso_fr.ts
* source: POSIX / target: german (any) resp. french (any) -> gibt gleich zwei felder für zwei sprachen... cool
* Mit gelben Pfeilen (next item) zum nächsten.
* die gelben Fragzeichen mit der Maus zu grünen Häckchen machen, wenn Übersetzung i.O. und fertig ist.
* Save all..
* File - Release All

* Umlaute erscheinen übelst... 
 - wenn man nichts macht, funktionierts noch. Und auch wenn man z.B. wiederum LFP3 Nachführung schreibt scheints zu funkionieren.

* Nachführung scheint zu klappen. Einfach wieder gleich aufrufen.
