CREATE TYPE $$DBSCHEMA.maengel_bereinigen AS ENUM
(
 'i.O.',
 'nicht bereinigen'
)

CREATE TYPE $$DBSCHEMA.avor_bezeichnung AS ENUM
(
 'Waldwege in Bodenbedeckung',
 'Waldwege als Achse in Einzelobjekte',
 'Waldwege löschen',
 'Waldgrenzen: Kontrolle und Beurteilung',
 'Übr. best. Fläche entlang Bäche, Bahn, Autobahn bereinigen',
 'Wytweiden: Definition durch Waldabteilung',
 'Schmale bestockte Fläche ab Bodenbedeckung in Einzelobjekte übernehmen',
 'Schmale bestockte Fläche löschen',
 'Wanderwege: wenn fehlend, als Achse in Einzelobjekte erfassen',
 'Wege in Landwirtschaftszone gemäss Handbuch',
 'GN5: Kontrolle, fehlende erfassen, Name attributieren, schmale Gewässer als Rinnsal',
 'Flüsse und Seen: Bodenbedeckung nach Prinzip LWN anpassen',
 'Hochwasserdamm darstellen od. löschen',
 'Bauernhof: Gartenanlage od. übrig befestigt anpassen',
 'Bauernhof: durchgehenden Weg erfassen',
 'Trottoir und Verkehrsinsel in Bodenbedeckung',
 'Löschen von zu detaillierten Gebäudeerschliessungen',
 'Erfassung und/oder Ergänzungen von Gebäudeerschliessungen',
 'Löschen und Separatablage von Verkehrshindernissen und Verkehrschwellen',
 'Löschen von privaten Parkplätzen',
 'Erfassung und/oder Ergänzung von grossen Parkplätzen',
 'Erfassung und/oder Ergänzung von übrig befestigen Flächen (Einfahrt Einstellhallen)',
 'Bahnareal: Bereinigung der Bodenbedeckung',
 'Bahnhof / Station: Bahnsteig erfassen',
 'Bei PNF-Bearbeitung neu festgestellte Fälle (sofort bereinigen)',
 'Bereinigung an Gemeinde- oder Losgrenzen',
 'Einzelobjekte: Bereinigung gemäss Handbuch (Flächen-, Linien- & Symbolobjekte)',
 'Löschen von überflüssigen Bodenbedeckungsgrenzen',
 'Gebäude < 12 m2 evt. Löschen',
 'neue BB ausscheiden, BB - Art ändern, BB - Abgrenzung anpassen',
 'fehlendes Silo / Wasserbecken / Gebäude etc.',
 'fehlende Brücke / Mast / schmaler Weg / eingedoltes Gewässer / Tunnel / Hochspannungsfreileitung',
 'fehlende Landwirtschaftswege',
 'Kontrolle Gebäude/Objekte (noch vorhanden)',
 'Trottoir bei Einfahrt unterbrechen',
 'Waldweg wird im Feld erhoben',
 'neuer Waldweg (laut Forst Klasse 2) wird nicht erhoben, da auf dem OF und auf der PK keine Grundlagen vorhanden sind. Feldaufnahmen werden nur bei Waldwege mit Klasse 1 ausgeführt',
 'EO mit Typ Brücke_Passarelle / Tunnel_Unterführung_Galerie / unterirdische Gebäude / Reservoir und Unterstand flächenmässig definieren (shapen)',
 'offene EO in NV und EE - Gebieten geschlossen definieren',
 'weiteres'
);

-- noinspection SqlNoDataSourceInspectionForFile
CREATE TABLE $$DBSCHEMA.t_maengel_punkt
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic NOT NULL,
 bemerkung varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bezeichnung $$DBSCHEMA.avor_bezeichnung NOT NULL,
 bemerkung_nfg text,
 forstorgan $$DBSCHEMA.maengel_bereinigen,
 bemerkung_forst text,
 verifikation $$DBSCHEMA.maengel_bereinigen,
 bemerkung_verifikation text,
 erledigt bool,
 the_geom geometry(POINT,$$EPSG),
 CONSTRAINT t_maengel_punkt_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_punkt TO $$USER;

CREATE TABLE $$DBSCHEMA.t_maengel_linie
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic NOT NULL,
 bemerkung varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bezeichnung $$DBSCHEMA.avor_bezeichnung NOT NULL,
 bemerkung_nfg text,
 forstorgan $$DBSCHEMA.maengel_bereinigen,
 bemerkung_forst text,
 verifikation $$DBSCHEMA.maengel_bereinigen,
 bemerkung_verifikation text,
 erledigt bool,
 the_geom geometry(LINESTRING,$$EPSG),
 CONSTRAINT t_maengel_linie_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_linie TO $$USER;


CREATE TABLE $$DBSCHEMA.t_maengel_polygon
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic NOT NULL,
 bemerkung varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bezeichnung $$DBSCHEMA.avor_bezeichnung NOT NULL,
 bemerkung_nfg text,
 forstorgan $$DBSCHEMA.maengel_bereinigen,
 bemerkung_forst text,
 verifikation $$DBSCHEMA.maengel_bereinigen,
 bemerkung_verifikation text,
 erledigt bool,
 the_geom geometry(POLYGON,$$EPSG),
 CONSTRAINT t_maengel_polygon_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_linie TO $$USER;
