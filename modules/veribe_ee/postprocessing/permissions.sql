-- EXAMPLE file, this is included in postprocessing.db fid = 98

CREATE ROLE geometerbuero;
CREATE ROLE forst;
CREATE ROLE verifikation;
CREATE ROLE agi;
CREATE ROLE olpnf;
GRANT verifikation to agi, olpnf;

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

GRANT UPDATE (bezeichnung, bemerkung_nfg, erledigt) ON $$DBSCHEMA.t_maengel_punkt TO
geometerbuero;
GRANT UPDATE (forstorgan, bemerkung_forst) ON $$DBSCHEMA.t_maengel_punkt TO
forst;
GRANT UPDATE (verifikation, bemerkung_verifikation) ON $$DBSCHEMA.t_maengel_punkt TO
verifikation;


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

GRANT UPDATE (bezeichnung, bemerkung_nfg, erledigt) ON $$DBSCHEMA.t_maengel_linie TO
geometerbuero;
GRANT UPDATE (forstorgan, bemerkung_forst) ON $$DBSCHEMA.t_maengel_linie TO
forst;
GRANT UPDATE (verifikation, bemerkung_verifikation) ON $$DBSCHEMA.t_maengel_linie TO
verifikation;



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
GRANT UPDATE (bezeichnung, bemerkung_nfg, erledigt) ON $$DBSCHEMA.t_maengel_polygon TO
geometerbuero;
GRANT UPDATE (forstorgan, bemerkung_forst) ON $$DBSCHEMA.t_maengel_polygon TO
forst;
GRANT UPDATE (verifikation, bemerkung_verifikation) ON $$DBSCHEMA.t_maengel_polygon TO
verifikation;