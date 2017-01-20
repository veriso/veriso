-- EXAMPLE file, this is included in postprocessing.db fid = 98

CREATE ROLE geometerbuero;
CREATE ROLE forst;
CREATE ROLE agi;
CREATE ROLE olpnf;

CREATE TABLE $$DBSCHEMA.t_maengel_punkt
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic,
 bemerkung varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bezeichnung $$DBSCHEMA.avor_bezeichnung,
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
GRANT ALL ON TABLE $$DBSCHEMA.t_maengel_punkt TO $$USER;

-- LINES
CREATE TABLE $$DBSCHEMA.t_maengel_linie
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic,
 bemerkung varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bezeichnung $$DBSCHEMA.avor_bezeichnung,
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
GRANT ALL ON TABLE $$DBSCHEMA.t_maengel_linie TO $$USER;


CREATE TABLE $$DBSCHEMA.t_maengel_polygon
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic,
 bemerkung varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bezeichnung $$DBSCHEMA.avor_bezeichnung,
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
GRANT ALL ON TABLE $$DBSCHEMA.t_maengel_polygon TO $$USER;