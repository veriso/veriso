PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tables
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);
INSERT INTO "tables" VALUES(1,'CREATE TABLE $$DBSCHEMA.t_maengel_punkt 
(
 ogc_fid serial NOT NULL, 
 topic varchar NOT NULL, 
 bemerkung varchar, 
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 
 the_geom geometry(POINT,$$EPSG), 
 CONSTRAINT t_maengel_punkt_pkey PRIMARY KEY (ogc_fid)
) 
WITH (OIDS=FALSE); 
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_punkt TO $$USER;');
INSERT INTO "tables" VALUES(2,'CREATE TABLE $$DBSCHEMA.t_maengel_linie
(
 ogc_fid serial NOT NULL, 
 topic varchar NOT NULL, 
 bemerkung varchar, 
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 
 the_geom geometry(LINESTRING,$$EPSG), 
 CONSTRAINT t_maengel_linie_pkey PRIMARY KEY (ogc_fid)
) 
WITH (OIDS=FALSE); 
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_linie TO $$USER;');
INSERT INTO "tables" VALUES(3,'CREATE TABLE $$DBSCHEMA.t_maengel_topics
(
 ogc_fid serial NOT NULL, 
 topic_name varchar NOT NULL,
 topic_name_fr  varchar NOT NULL,
 CONSTRAINT t_maengel_topics_pkey PRIMARY KEY (ogc_fid)
) 
WITH (OIDS=FALSE); 
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_topics TO $$USER;');
INSERT INTO "tables" VALUES(4,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz
(
 ogc_fid serial NOT NULL,
 tid character varying,
 line geometry(LINESTRING,$$EPSG),
 hausnummer character varying,
 CONSTRAINT t_gebaeudeadressen_spinnennetz_pkey PRIMARY KEY (ogc_fid)
) 
WITH (OIDS=FALSE); 
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz TO $$USER;');
INSERT INTO "tables" VALUES(5,'CREATE TABLE $$DBSCHEMA.t_shortestline_hausnummerpos
(
 ogc_fid serial NOT NULL,
 strname character varying,
 hausnummer character varying,
 a_tid character varying,
 b_tid character varying,
 lok_tid character varying,
 the_geom geometry(LINESTRING,$$EPSG),
 CONSTRAINT t_shortestline_hausnummerpos_pkey PRIMARY KEY (ogc_fid)
) 
WITH (OIDS=FALSE); 
GRANT SELECT ON TABLE $$DBSCHEMA.t_shortestline_hausnummerpos TO $$USER;');
INSERT INTO "tables" VALUES(6,'CREATE TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang
(
  ogc_fid serial NOT NULL,
  tid character varying,
  entstehung character varying,
  geometrie geometry(POLYGON,$$EPSG),
  flaeche double precision,
  qualitaet integer,
  qualitaet_txt character varying,
  art integer,
  art_txt character varying,
  CONSTRAINT t_gebaeude_groesser_12m2_ohne_eingang_pkey PRIMARY KEY (ogc_fid)
)
WITH (
  OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang TO $$USER;');
INSERT INTO "tables" VALUES(7,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_ausserhalb
(
  ogc_fid serial NOT NULL,
  tid character varying,
  entstehung character varying,
  gebaeudeeingang_von character varying,
  status integer,
  status_txt character varying,
  inaenderung integer,
  inaenderung_txt character varying,
  attributeprovisorisch integer,
  attributeprovisorisch_txt character varying,
  istoffiziellebezeichnung integer,
  istoffiziellebezeichnung_txt character varying,
  lage geometry(POINT,$$EPSG),
  hoehenlage double precision,
  hausnummer character varying,
  im_gebaeude integer,
  im_gebaeude_txt character varying,
  gwr_egid double precision,
  gwr_edid double precision,
  CONSTRAINT t_gebaeudeadressen_gebaeudeeingang_ausserhalb_pkey PRIMARY KEY (ogc_fid)
)
WITH (
  OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_ausserhalb TO $$USER;');
INSERT INTO "tables" VALUES(8,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_innerhalb_centroidbuffer
(
  ogc_fid serial NOT NULL,
  tid character varying,
  entstehung character varying,
  gebaeudeeingang_von character varying,
  status integer,
  status_txt character varying,
  inaenderung integer,
  inaenderung_txt character varying,
  attributeprovisorisch integer,
  attributeprovisorisch_txt character varying,
  istoffiziellebezeichnung integer,
  istoffiziellebezeichnung_txt character varying,
  lage geometry(POINT,$$EPSG),
  hoehenlage double precision,
  hausnummer character varying,
  im_gebaeude integer,
  im_gebaeude_txt character varying,
  gwr_egid double precision,
  gwr_edid double precision,
  CONSTRAINT t_gebaeudeadressen_gebaeudeeingang_innerhalb_centroidbuffer_pkey PRIMARY KEY (ogc_fid)
)
WITH (
  OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_innerhalb_centroidbuffer TO $$USER;');
INSERT INTO "tables" VALUES(9,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_ausserhalb
(
  ogc_fid serial NOT NULL,
  tid character varying,
  hausnummerpos_von character varying,
  pos geometry(POINT,$$EPSG),
  ori double precision,
  hali integer,
  hali_txt character varying,
  vali integer,
  vali_txt character varying,
  groesse integer,
  groesse_txt character varying,
  CONSTRAINT t_gebaeudeadressen_hausnummerpos_ausserhalb_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_ausserhalb TO $$USER;');
INSERT INTO "tables" VALUES(10,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_doppelt
(
  ogc_fid serial NOT NULL,
  tid character varying,
  hausnummerpos_von character varying,
  pos geometry(POINT,$$EPSG),
  ori double precision,
  hali integer,
  hali_txt character varying,
  vali integer,
  vali_txt character varying,
  groesse integer,
  groesse_txt character varying,
  CONSTRAINT t_gebaeudeadressen_hausnummerpos_doppelt_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_doppelt TO $$USER;');
INSERT INTO "tables" VALUES(11,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos
(
  ogc_fid serial NOT NULL,
  tid character varying,
  entstehung character varying,
  gebaeudeeingang_von character varying,
  status integer,
  status_txt character varying,
  inaenderung integer,
  inaenderung_txt character varying,
  attributeprovisorisch integer,
  attributeprovisorisch_txt character varying,
  istoffiziellebezeichnung integer,
  istoffiziellebezeichnung_txt character varying,
  lage geometry(POINT,$$EPSG),
  hoehenlage double precision,
  hausnummer character varying,
  im_gebaeude integer,
  im_gebaeude_txt character varying,
  gwr_egid double precision,
  gwr_edid double precision,
  CONSTRAINT t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos TO $$USER;');
INSERT INTO "tables" VALUES(12,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok
(
  ogc_fid serial NOT NULL,
  tid character varying,
  entstehung character varying,
  gebaeudeeingang_von character varying,
  status integer,
  status_txt character varying,
  inaenderung integer,
  inaenderung_txt character varying,
  attributeprovisorisch integer,
  attributeprovisorisch_txt character varying,
  istoffiziellebezeichnung integer,
  istoffiziellebezeichnung_txt character varying,
  lage geometry(POINT,$$EPSG),
  hoehenlage double precision,
  hausnummer character varying,
  im_gebaeude integer,
  im_gebaeude_txt character varying,
  gwr_egid double precision,
  gwr_edid double precision,
  CONSTRAINT t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok_pkey PRIMARY KEY (ogc_fid)
)
WITH (
  OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok TO $$USER;');
INSERT INTO "tables" VALUES(101,'CREATE TABLE $$DBSCHEMA.z_v_bb_ts
(
  OGC_FID integer NOT NULL,
  geometrie geometry,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  bb_ogc_fid integer,
  bb_art integer,
  bb_art_txt character varying,
  ts_ogc_fid integer,
  ts_art integer,
  ts_art_txt character varying,
  flaeche double precision,
  CONSTRAINT z_v_bb_ts_pkey PRIMARY KEY (OGC_FID)
)
WITH (OIDS=TRUE);
ALTER TABLE $$DBSCHEMA.z_v_bb_ts OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_bb_ts TO $$USER;');

INSERT INTO "tables" VALUES(102,'CREATE TABLE $$DBSCHEMA.z_v_ls_nk
(
  z_ls_nk_fid integer NOT NULL,
  ls_fid integer NOT NULL,
  nk_fid integer NOT NULL,
  geometrie geometry NOT NULL,
  gem_bfs integer NOT NULL,
  los integer NOT NULL,
  lieferdatum date NOT NULL,
  flaeche double precision,
  CONSTRAINT z_v_ls_nk_pkey PRIMARY KEY (z_ls_nk_fid )
)
WITH (OIDS=TRUE);
ALTER TABLE $$DBSCHEMA.z_v_ls_nk OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_ls_nk TO $$USER;');
INSERT INTO "tables" VALUES(103,'CREATE TABLE $$DBSCHEMA.z_v_bb_ls
(
  ogc_fid serial NOT NULL,
  bb_ogc_fid integer,
  bb_qualitaet integer,
  bb_qualitaet_txt character varying,
  art integer,
  art_txt character varying,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  ls_ogc_fid serial NOT NULL,
  liegenschaft_von character varying,
  nummerteilgrundstueck character varying,
  flaechenmass double precision,
  geometrie geometry,
  flaeche double precision,
  CONSTRAINT z_v_bb_ls_pkey PRIMARY KEY (ogc_fid )
)
WITH (OIDS=TRUE);
ALTER TABLE $$DBSCHEMA.z_v_bb_ls OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_bb_ls TO $$USER;');

INSERT INTO "tables" VALUES(104,'CREATE TABLE $$DBSCHEMA.z_ls_entstehung
(
  ogc_fid integer NOT NULL,
  ls_ogc_fid integer,
  geometrie geometry,
  nummer character varying,
  entstehung character varying,
  gem_bfs integer,
  lieferdatum date,
  los integer,
  CONSTRAINT z_ls_entstehung_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_ls_entstehung
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_ls_entstehung TO $$USER;');

INSERT INTO "tables" VALUES(105,'CREATE TABLE $$DBSCHEMA.z_grenzen
(
  ogc_fid integer NOT NULL,
  geometrie geometry,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_grenzen_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE $$DBSCHEMA.z_grenzen
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_grenzen TO $$USER;');



INSERT INTO "tables" VALUES(107,'CREATE TABLE $$DBSCHEMA.z_v_gp_ts
(
  ogc_fid integer NOT NULL,
  tid character varying,
  entstehung character varying,
  identifikator character varying,
  geometrie geometry,
  lagegen double precision,
  lagezuv integer,
  lagezuv_txt character varying,
  punktzeichen integer,
  punktzeichen_txt character varying,
  exaktdefiniert integer,
  exaktdefiniert_txt character varying,
  hoheitsgrenzsteinalt integer,
  hoheitsgrenzsteinalt_txt character varying,
  art integer,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_v_gp_ts_2_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_v_gp_ts
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_gp_ts TO $$USER;');


INSERT INTO "tables" VALUES(108,'CREATE TABLE $$DBSCHEMA.z_liegenschaft_flaeche
(
  ogc_fid serial NOT NULL,
  tid character varying,
  liegenschaft_von character varying,
  nummerteilgrundstueck character varying,
  geometrie geometry,
  flaechenmass double precision,
  flaeche double precision,
  qualitaet integer,
  qualitaet_txt character varying,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_liegenschaft_flaeche_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_liegenschaft_flaeche
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_liegenschaft_flaeche TO $$USER;');

INSERT INTO "tables" VALUES(109,'CREATE TABLE $$DBSCHEMA.z_selbstrecht_flaeche
(
  ogc_fid serial NOT NULL,
  tid character varying,
  selbstrecht_von character varying,
  nummerteilgrundstueck character varying,
  geometrie geometry,
  flaechenmass double precision,
  flaeche double precision,
  qualitaet integer,
  qualitaet_txt character varying,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_selbstrecht_flaeche_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_selbstrecht_flaeche
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_selbstrecht_flaeche TO $$USER;');


INSERT INTO "tables" VALUES(110,'CREATE TABLE $$DBSCHEMA.z_hgp_ls_linie
(
  ogc_fid serial NOT NULL,
  geometrie geometry,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_hgp_ls_linie_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_hgp_ls_linie
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_hgp_ls_linie TO $$USER;');

INSERT INTO "tables" VALUES(111,'CREATE TABLE $$DBSCHEMA.z_nr_gs
(
  ogc_fid serial NOT NULL,
  nbident character varying,
  nummer character varying,
  egris_egrid character varying,
  gueltigkeit integer,
  gueltigkeit_txt character varying,
  vollstaendigkeit integer,
  vollstaendigkeit_txt character varying,
  art integer,
  art_txt character varying,
  gesamteflaechenmass double precision,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  nummerteilgrundstueck character varying,
  pos geometry,
  lin integer,
  CONSTRAINT liegenschaften_z_nr_gs_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_nr_gs
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_nr_gs TO $$USER;');


INSERT INTO "tables" VALUES(112,'CREATE TABLE $$DBSCHEMA.z_v_ls_nk_pkt
(
  z_ls_nk_pkt_fid integer NOT NULL,
  ls_fid integer NOT NULL,
  nk_fid integer NOT NULL,
  gem_bfs integer NOT NULL,
  los integer NOT NULL,
  lieferdatum date NOT NULL,
  flaeche double precision,
  geometrie geometry,
  CONSTRAINT z_v_ls_nk_pkt_pkey PRIMARY KEY (z_ls_nk_pkt_fid )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE $$DBSCHEMA.z_v_ls_nk_pkt
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_ls_nk_pkt TO $$USER;');

INSERT INTO "tables" VALUES(113,'CREATE TABLE $$DBSCHEMA.z_gebaeudenummer_pos
(
  ogc_fid serial NOT NULL,
  tid character varying,
  gebaeudenummer_von character varying,
  nummer character varying,
  gwr_egid double precision,
  nbident character varying,
  pos geometry,
  ori double precision,
  hali integer,
  hali_txt character varying,
  vali integer,
  vali_txt character varying,
  groesse integer,
  groesse_txt character varying,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_gebaeudenummer_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_gebaeudenummer_pos
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_gebaeudenummer_pos TO $$USER;');

-- DROP TABLE $$DBSCHEMA.z_objektnummer_pos;

INSERT INTO "tables" VALUES(114,'CREATE TABLE $$DBSCHEMA.z_objektnummer_pos
(
  ogc_fid serial NOT NULL,
  tid character varying,
  objektnummer_von character varying,
  nummer character varying,
  gwr_egid double precision,
  nbident character varying,
  pos geometry,
  ori double precision,
  hali integer,
  hali_txt character varying,
  vali integer,
  vali_txt character varying,
  groesse integer,
  groesse_txt character varying,
  gem_bfs integer,
  los integer,
  lieferdatum date,
  CONSTRAINT z_objektnummer_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_objektnummer_pos
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_objektnummer_pos TO $$USER;');



CREATE TABLE views
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);
INSERT INTO "views" VALUES(1,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_lfp3_ausserhalb_gemeinde AS 
 SELECT a.*
 FROM $$DBSCHEMA.fixpunktekategorie3_lfp3 a, 
 (
  SELECT (ST_Union(geometrie)) as geometrie
  FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze
 ) b
 WHERE ST_Distance(a.geometrie, b.geometrie) > 0;
GRANT SELECT ON TABLE $$DBSCHEMA.v_lfp3_ausserhalb_gemeinde TO $$USER;');
INSERT INTO "views" VALUES(2,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_flaechenelement AS
SELECT b.*, a.art, a.art_txt, a.tid as eo_tid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_flaechenelement as b
WHERE b.flaechenelement_von = a.tid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_flaechenelement TO $$USER;');
INSERT INTO "views" VALUES(3,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_linienelement AS
SELECT b.*, a.art, a.art_txt, a.tid as eo_tid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_linienelement as b
WHERE b.linienelement_von = a.tid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_linienelement TO $$USER;');
INSERT INTO "views" VALUES(4,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_punktelement AS
SELECT b.*, a.art, a.art_txt, a.tid as eo_tid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_punktelement as b
WHERE b.punktelement_von = a.tid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_punktelement TO $$USER;');
INSERT INTO "views" VALUES(5,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos AS 
SELECT b.ogc_fid, b.tid, b.hausnummerpos_von, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, ST_X(b.pos) AS y, ST_Y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.hausnummer, a.gebaeudeeingang_von as lok_tid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, $$DBSCHEMA.gebaeudeadressen_hausnummerpos b
WHERE a.tid::text = b.hausnummerpos_von::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos TO $$USER;');
INSERT INTO "views" VALUES(6,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos AS 
 SELECT b.ogc_fid, b.tid, b.lokalisationsnamepos_von, b.anfindex, b.endindex, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, b.hilfslinie, ST_X(b.pos) AS y, ST_Y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.benannte, a.text
FROM $$DBSCHEMA.gebaeudeadressen_lokalisationsname a, $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos b
WHERE a.tid::text = b.lokalisationsnamepos_von::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos TO $$USER;');
INSERT INTO "views" VALUES(7,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_distanz_gebaeudeeingang_lokalisationsnamepos AS 
SELECT a.tid AS atid, b.tid AS btid, min(ST_Length(ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(b.pos)::text) || '' ''::text) || ST_Y(b.pos)::text) || '')''::text, $$EPSG))) AS min
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, $$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos b
WHERE a.gebaeudeeingang_von::text = b.benannte::text 
GROUP BY a.tid, b.tid
ORDER BY a.tid, min(ST_Length(ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(b.pos)::text) || '' ''::text) || ST_Y(b.pos)::text) || '')''::text, $$EPSG)));

GRANT SELECT ON TABLE $$DBSCHEMA.v_distanz_gebaeudeeingang_lokalisationsnamepos TO $$USER;');
INSERT INTO "views" VALUES(8,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_lokalisationsname_ohne_gebaeudeeingaenge AS 

SELECT a.ogc_fid, a.tid, a.entstehung, a.nummerierungsprinzip, a.nummerierungsprinzip_txt, 
       a.lokalisationnummer, a.attributeprovisorisch, a.attributeprovisorisch_txt, 
       a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.status, a.status_txt, 
       a.inaenderung, a.inaenderung_txt, a.art, a.art_txt, b.text
FROM 
( 
  SELECT a.ogc_fid, a.tid, a.entstehung, a.nummerierungsprinzip, a.nummerierungsprinzip_txt, 
         a.lokalisationnummer, a.attributeprovisorisch, a.attributeprovisorisch_txt, 
         a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.status, a.status_txt, 
         a.inaenderung, a.inaenderung_txt, a.art, a.art_txt
  FROM $$DBSCHEMA.gebaeudeadressen_lokalisation a
  LEFT JOIN 
  ( 
    SELECT DISTINCT ON (gebaeudeadressen_gebaeudeeingang.gebaeudeeingang_von) 
           gebaeudeadressen_gebaeudeeingang.ogc_fid, gebaeudeadressen_gebaeudeeingang.tid, 
           gebaeudeadressen_gebaeudeeingang.entstehung, gebaeudeadressen_gebaeudeeingang.gebaeudeeingang_von, 
           gebaeudeadressen_gebaeudeeingang.status, gebaeudeadressen_gebaeudeeingang.status_txt, 
           gebaeudeadressen_gebaeudeeingang.inaenderung, gebaeudeadressen_gebaeudeeingang.inaenderung_txt, 
           gebaeudeadressen_gebaeudeeingang.attributeprovisorisch, 
           gebaeudeadressen_gebaeudeeingang.attributeprovisorisch_txt, 
           gebaeudeadressen_gebaeudeeingang.istoffiziellebezeichnung, 
           gebaeudeadressen_gebaeudeeingang.istoffiziellebezeichnung_txt, 
           gebaeudeadressen_gebaeudeeingang.lage, gebaeudeadressen_gebaeudeeingang.hoehenlage, 
           gebaeudeadressen_gebaeudeeingang.hausnummer, gebaeudeadressen_gebaeudeeingang.im_gebaeude, 
           gebaeudeadressen_gebaeudeeingang.im_gebaeude_txt, gebaeudeadressen_gebaeudeeingang.gwr_egid, 
           gebaeudeadressen_gebaeudeeingang.gwr_edid
     FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang
  ) b ON a.tid::text = b.gebaeudeeingang_von::text 
  WHERE b.gebaeudeeingang_von IS NULL
) a, 
$$DBSCHEMA.gebaeudeadressen_lokalisationsname b
WHERE a.tid::text = b.benannte::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_lokalisationsname_ohne_gebaeudeeingaenge TO $$USER;');
INSERT INTO "views" VALUES(10,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_ohne_nummer_attribute AS 
SELECT a.ogc_fid, a.tid, a.entstehung, a.gebaeudeeingang_von, a.status, a.status_txt, 
       a.inaenderung, a.inaenderung_txt, a.attributeprovisorisch, a.attributeprovisorisch_txt, 
       a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.lage, a.hoehenlage, 
       a.hausnummer, a.im_gebaeude, a.im_gebaeude_txt, a.gwr_egid, a.gwr_edid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a
WHERE a.gebaeudeeingang_von IS NOT NULL 
AND a.hausnummer IS NULL 
AND (a.status <> 1 OR a.inaenderung <> 1 OR a.attributeprovisorisch <> 1 OR a.istoffiziellebezeichnung <> 1);

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_ohne_nummer_attribute TO $$USER;');
INSERT INTO "views" VALUES(11,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_mit_nummer_attribute AS 
SELECT a.ogc_fid, a.tid, a.entstehung, a.gebaeudeeingang_von, a.status, a.status_txt, 
       a.inaenderung, a.inaenderung_txt, a.attributeprovisorisch, a.attributeprovisorisch_txt, 
       a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.lage, a.hoehenlage, 
       a.hausnummer, a.im_gebaeude, a.im_gebaeude_txt, a.gwr_egid, a.gwr_edid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a
WHERE a.gebaeudeeingang_von IS NOT NULL 
AND a.hausnummer IS NOT NULL 
AND (a.status <> 1 OR a.inaenderung <> 1 OR a.attributeprovisorisch <> 1 OR a.istoffiziellebezeichnung <> 0);

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_mit_nummer_attribute TO $$USER;');
INSERT INTO "views" VALUES(12,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos_ohne_nummer AS 
SELECT a.ogc_fid, a.tid, a.hausnummerpos_von, a.pos, a.ori, a.hali, a.hali_txt, 
       a.vali, a.vali_txt, a.groesse, a.groesse_txt
FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos a, $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang b
WHERE a.hausnummerpos_von::text = b.tid::text 
AND b.hausnummer IS NULL;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos_ohne_nummer TO $$USER;');
CREATE TABLE inserts
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);
INSERT INTO "inserts" VALUES(1,'INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''FixpunkteKategorie1'', ''Points_fixesCategorie1'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''FixpunkteKategorie2'', ''Points_fixesCategorie2'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''FixpunkteKategorie3'', ''Points_fixesCategorie3'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Bodenbedeckung'', ''Couverture_du_sol'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Einzelobjekte'', ''Objets_divers'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Hoehen'', ''Altimetrie'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Nomenklatur'', ''Nomenclature'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Liegenschaften'', ''Nomenclature'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Rohrleitungen'', ''Conduites'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Nummerierungsbereiche'', ''Domaines_numerotation'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Gemeindegrenzen'', ''Limites_commune'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Bezirksgrenzen'', ''Limites_district'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Kantonsgrenzen'', ''Limites_canton'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Landesgrenzen'', ''Limites_nationales'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Planeinteilungen'', ''Repartitions_plans'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''TSEinteilung'', ''RepartitionNT'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Rutschgebiete'', ''Zones_glissement'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''PLZOrtschaft'', ''NPA_Localite'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Gebaeudeadressen'', ''Adresses_des_batiments'');
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Planrahmen'', ''Bords_de_plan'');');
INSERT INTO "inserts" VALUES(2,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_spinnennetz (ogc_fid, tid, line, hausnummer) 
SELECT a.ogc_fid, a.tid, ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(c.pos)::text) || '' ''::text) || ST_Y(c.pos)::text) || '')''::text, $$EPSG) AS line, a.hausnummer

FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, 
( 
 SELECT a.atid, a.btid, a.min 
 FROM $$DBSCHEMA.v_distanz_gebaeudeeingang_lokalisationsnamepos a, 
  ( 
    SELECT v_distanz_gebaeudeeingang_lokalisationsnamepos.atid, min(v_distanz_gebaeudeeingang_lokalisationsnamepos.min) AS min
    FROM $$DBSCHEMA.v_distanz_gebaeudeeingang_lokalisationsnamepos 
    GROUP BY v_distanz_gebaeudeeingang_lokalisationsnamepos.atid
  ) b 
 WHERE a.min = b.min 
 AND a.atid::text = b.atid::text
) b, 
$$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos c 
WHERE b.atid::text = a.tid::text 
AND b.btid::text = c.tid::text;');
INSERT INTO "inserts" VALUES(3,'INSERT INTO $$DBSCHEMA.t_shortestline_hausnummerpos (ogc_fid, strname, hausnummer, a_tid, b_tid, lok_tid, the_geom) 
SELECT a.ogc_fid, d."text" as strnam, b.hausnummer, a.tid as a_tid, b.tid as b_tid, 
       b.gebaeudeeingang_von as lok_tid, ST_ShortestLine(a.pos, c.geometrie) as the_geom
FROM $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos as a, 
     $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang as b,
     (
       SELECT ST_Union(geometrie) as geometrie, strassenstueck_von
       FROM $$DBSCHEMA.gebaeudeadressen_strassenstueck
       GROUP BY strassenstueck_von
     ) as c,
     $$DBSCHEMA.gebaeudeadressen_lokalisationsname as d
WHERE a.hausnummerpos_von = b.tid
AND b.gebaeudeeingang_von = c.strassenstueck_von
AND d.benannte = b.gebaeudeeingang_von;');
INSERT INTO "inserts" VALUES(4,'INSERT INTO $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang (tid, entstehung, geometrie, flaeche, qualitaet, qualitaet_txt, art, art_txt)

SELECT c.tid, c.entstehung, c.geometrie, ST_Area(c.geometrie) as flaeche, c.qualitaet, c.qualitaet_txt, c.art, c.art_txt
FROM 
(
 SELECT bodenbedeckung_boflaeche.ogc_fid, bodenbedeckung_boflaeche.tid, bodenbedeckung_boflaeche.entstehung, 
        bodenbedeckung_boflaeche.geometrie, bodenbedeckung_boflaeche.qualitaet, 
        bodenbedeckung_boflaeche.qualitaet_txt, bodenbedeckung_boflaeche.art, bodenbedeckung_boflaeche.art_txt
 FROM $$DBSCHEMA.bodenbedeckung_boflaeche
 WHERE bodenbedeckung_boflaeche.art = 0 
 AND ST_Area(bodenbedeckung_boflaeche.geometrie) > 12::double precision

EXCEPT 

 SELECT DISTINCT ON (a.ogc_fid) a.ogc_fid, a.tid, a.entstehung, a.geometrie, a.qualitaet, a.qualitaet_txt, 
        a.art, a.art_txt
 FROM $$DBSCHEMA.bodenbedeckung_boflaeche a, $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang b
 WHERE a.art = 0 AND ST_Area(a.geometrie) > 12::double precision 
 AND a.geometrie && b.lage 
 AND ST_Distance(a.geometrie, b.lage) = 0::double precision
) as c;');
INSERT INTO "inserts" VALUES(5,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_ausserhalb 
SELECT * 
FROM 
(
 SELECT a.*
 FROM
 (
  SELECT * 
  FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang

  EXCEPT

  SELECT a.* 
  FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang as a, $$DBSCHEMA.bodenbedeckung_boflaeche as b
  WHERE b.art_txt = ''Gebaeude''
  AND a.lage && b.geometrie
  AND ST_Distance(a.lage, b.geometrie) = 0
 ) as a

EXCEPT

 SELECT a.*
 FROM
 (
  SELECT * 
  FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang

  EXCEPT

  SELECT a.* 
  FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang as a, $$DBSCHEMA.bodenbedeckung_boflaeche as b
  WHERE b.art_txt = ''Gebaeude''
  AND a.lage && b.geometrie
  AND ST_Distance(a.lage, b.geometrie) = 0
 ) as a,
 $$DBSCHEMA.v_einzelobjekte_flaechenelement as b
 WHERE b.art_txt IN (''unterirdisches_Gebaeude'', ''uebriger_Gebaeudeteil'', ''Unterstand'', ''Reservoir'') 
 AND a.lage && b.geometrie
 AND ST_Distance(a.lage, b.geometrie) = 0
) as c;');
INSERT INTO "inserts" VALUES(6,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_innerhalb_centroidbuffer
SELECT a.*
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang as a, $$DBSCHEMA.bodenbedeckung_boflaeche as b
WHERE a.lage && b.geometrie
AND ST_Distance(a.lage, ST_Buffer(ST_Centroid(b.geometrie),1)) = 0;');
INSERT INTO "inserts" VALUES(7,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_ausserhalb 
SELECT * 
FROM 
(
 SELECT a.*
 FROM
 (
  SELECT * 
  FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos 

  EXCEPT

  SELECT a.* 
  FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos as a, $$DBSCHEMA.bodenbedeckung_boflaeche as b
  WHERE b.art_txt = ''Gebaeude''
  AND a.pos && b.geometrie
  AND ST_Distance(a.pos, b.geometrie) = 0
 ) as a

EXCEPT

 SELECT a.*
 FROM
 (
  SELECT * 
  FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos

  EXCEPT

  SELECT a.* 
  FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos as a, $$DBSCHEMA.bodenbedeckung_boflaeche as b
  WHERE b.art_txt = ''Gebaeude''
  AND a.pos && b.geometrie
  AND ST_Distance(a.pos, b.geometrie) = 0
 ) as a,
 $$DBSCHEMA.v_einzelobjekte_flaechenelement as b
 WHERE b.art_txt IN (''unterirdisches_Gebaeude'', ''uebriger_Gebaeudeteil'', ''Unterstand'', ''Reservoir'') 

 AND a.pos && b.geometrie
 AND ST_Distance(a.pos, b.geometrie) = 0
) as c;');
INSERT INTO "inserts" VALUES(8,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_doppelt
SELECT a.*
FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos as a, 
(
 SELECT gebaeudeadressen_hausnummerpos.ogc_fid, gebaeudeadressen_hausnummerpos.tid, 
        gebaeudeadressen_hausnummerpos.hausnummerpos_von, gebaeudeadressen_hausnummerpos.pos, 
        gebaeudeadressen_hausnummerpos.ori, gebaeudeadressen_hausnummerpos.hali, 
        gebaeudeadressen_hausnummerpos.hali_txt, gebaeudeadressen_hausnummerpos.vali, 
        gebaeudeadressen_hausnummerpos.vali_txt, gebaeudeadressen_hausnummerpos.groesse, 
        gebaeudeadressen_hausnummerpos.groesse_txt
 FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos
  
 EXCEPT 

 SELECT DISTINCT ON (hausnummerpos_von) *
 FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos
) as b
WHERE a.hausnummerpos_von::text = b.hausnummerpos_von::text;');
INSERT INTO "inserts" VALUES(9,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos
SELECT a.*
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, 
(
 SELECT tid
 FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang
 WHERE gebaeudeadressen_gebaeudeeingang.hausnummer IS NOT NULL 

  EXCEPT 

 SELECT hausnummerpos_von
 FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos

) b
WHERE a.tid::text = b.tid::text;');
INSERT INTO "inserts" VALUES(10,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok
SELECT a.*
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, 
(
  SELECT gebaeudeadressen_gebaeudeeingang.ogc_fid, gebaeudeadressen_gebaeudeeingang.tid, 
         gebaeudeadressen_gebaeudeeingang.entstehung, gebaeudeadressen_gebaeudeeingang.gebaeudeeingang_von,
         gebaeudeadressen_gebaeudeeingang.status, gebaeudeadressen_gebaeudeeingang.status_txt, 
         gebaeudeadressen_gebaeudeeingang.inaenderung, gebaeudeadressen_gebaeudeeingang.inaenderung_txt,
         gebaeudeadressen_gebaeudeeingang.attributeprovisorisch, gebaeudeadressen_gebaeudeeingang.attributeprovisorisch_txt,
         gebaeudeadressen_gebaeudeeingang.istoffiziellebezeichnung, gebaeudeadressen_gebaeudeeingang.istoffiziellebezeichnung_txt,
         gebaeudeadressen_gebaeudeeingang.lage, gebaeudeadressen_gebaeudeeingang.hoehenlage, 
         gebaeudeadressen_gebaeudeeingang.hausnummer, gebaeudeadressen_gebaeudeeingang.im_gebaeude,
         gebaeudeadressen_gebaeudeeingang.im_gebaeude_txt, gebaeudeadressen_gebaeudeeingang.gwr_egid, 
         gebaeudeadressen_gebaeudeeingang.gwr_edid
  FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang
  WHERE gebaeudeadressen_gebaeudeeingang.hausnummer IS NOT NULL
 
    EXCEPT 

  SELECT DISTINCT ON (gebaeudeeingang_von, hausnummer) gebaeudeadressen_gebaeudeeingang.ogc_fid, 
         gebaeudeadressen_gebaeudeeingang.tid, gebaeudeadressen_gebaeudeeingang.entstehung,
         gebaeudeadressen_gebaeudeeingang.gebaeudeeingang_von, gebaeudeadressen_gebaeudeeingang.status,
         gebaeudeadressen_gebaeudeeingang.status_txt, gebaeudeadressen_gebaeudeeingang.inaenderung,
         gebaeudeadressen_gebaeudeeingang.inaenderung_txt, gebaeudeadressen_gebaeudeeingang.attributeprovisorisch,
         gebaeudeadressen_gebaeudeeingang.attributeprovisorisch_txt, gebaeudeadressen_gebaeudeeingang.istoffiziellebezeichnung,
         gebaeudeadressen_gebaeudeeingang.istoffiziellebezeichnung_txt, gebaeudeadressen_gebaeudeeingang.lage,
         gebaeudeadressen_gebaeudeeingang.hoehenlage, gebaeudeadressen_gebaeudeeingang.hausnummer, 
         gebaeudeadressen_gebaeudeeingang.im_gebaeude, gebaeudeadressen_gebaeudeeingang.im_gebaeude_txt,
         gebaeudeadressen_gebaeudeeingang.gwr_egid, gebaeudeadressen_gebaeudeeingang.gwr_edid
  FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang
  WHERE gebaeudeadressen_gebaeudeeingang.hausnummer IS NOT NULL
) b
WHERE a.hausnummer::text = b.hausnummer::text 
AND a.gebaeudeeingang_von::text = b.gebaeudeeingang_von::text;');
INSERT INTO "inserts" VALUES(101,'INSERT INTO $$DBSCHEMA.z_v_bb_ts 
SELECT 
  ST_intersection(ts.geometrie,bb.geometrie) as geometrie, 
  bb.gem_bfs as gem_bfs,
  bb.los as los,
  bb.lieferdatum as lieferdatum,
  bb.ogc_fid as bb_ogc_fid,
  bb.art as bb_art,
  bb.art_txt as bb_art_txt,
  ts.ogc_fid as ts_ogc_fid,
  ts.art as ts_art,
  ts.art_txt as ts_art_txt,
 st_area (ST_intersection(ts.geometrie,bb.geometrie)) as flaeche
FROM 
  $$DBSCHEMA.bodenbedeckung_boflaeche as bb, 
  $$DBSCHEMA.tseinteilung_toleranzstufe as ts
WHERE 
  ST_Intersects (bb.geometrie,ts.geometrie)=true AND
  bb.los = ts.los AND 
  bb.gem_bfs = ts.gem_bfs AND
  bb.lieferdatum = ts.lieferdatum;');
INSERT INTO "inserts" VALUES(102,'INSERT INTO $$DBSCHEMA.z_grenzen 
SELECT DISTINCT b.ogc_fid,b.geometrie,b.gem_bfs,b.los,b.lieferdatum
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b
where b.gem_bfs = ___GEM_BFS AND 
b.los = ___LOS AND 
b.lieferdatum = ___LIEFERDATUM

except 
(
SELECT DISTINCT a.ogc_fid,a.geometrie,a.gem_bfs,a.los,a.lieferdatum
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt a, $$DBSCHEMA.liegenschaften_liegenschaft
  WHERE a.gem_bfs = liegenschaften_liegenschaft.gem_bfs AND 
a.los = liegenschaften_liegenschaft.los AND 
a.lieferdatum = liegenschaften_liegenschaft.lieferdatum AND 
st_touches(a.geometrie, liegenschaften_liegenschaft.geometrie) IS TRUE
Union 
SELECT DISTINCT b.ogc_fid,b.geometrie,b.gem_bfs,b.los,b.lieferdatum
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_selbstrecht
  WHERE b.gem_bfs = liegenschaften_selbstrecht.gem_bfs AND 
b.los = liegenschaften_selbstrecht.los AND 
b.lieferdatum = liegenschaften_selbstrecht.lieferdatum AND 
st_touches(b.geometrie, liegenschaften_selbstrecht.geometrie) IS TRUE
Union
SELECT DISTINCT b.ogc_fid,b.geometrie,b.gem_bfs,b.los,b.lieferdatum
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projliegenschaft
  WHERE b.gem_bfs = liegenschaften_projliegenschaft.gem_bfs AND 
b.los = liegenschaften_projliegenschaft.los AND 
b.lieferdatum = liegenschaften_projliegenschaft.lieferdatum AND 
st_touches(b.geometrie, liegenschaften_projliegenschaft.geometrie) IS TRUE
UNION
SELECT DISTINCT b.ogc_fid,b.geometrie,b.gem_bfs,b.los,b.lieferdatum
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projselbstrecht
  WHERE b.gem_bfs = liegenschaften_projselbstrecht.gem_bfs AND 
b.los = liegenschaften_projselbstrecht.los AND 
b.lieferdatum = liegenschaften_projselbstrecht.lieferdatum AND 
st_touches(b.geometrie, liegenschaften_projselbstrecht.geometrie) IS TRUE
)');
INSERT INTO "inserts" VALUES(103,'INSERT INTO $$DBSCHEMA.gebaeudeadressen_spinnennetz
SELECT a.ogc_fid, a.tid, geometryfromtext((((((((''LINESTRING(''::text || x(a.lage)::text) || '' ''::text) || y(a.lage)::text) || '',''::text) || x(c.pos)::text) || '' ''::text) || y(c.pos)::text) || '')''::text, 21781) AS line, a.hausnummer, a.gem_bfs, a.los, a.lieferdatum 

FROM dm01avch24d.gebaeudeadressen_gebaeudeeingang a, 
( 
 SELECT a.atid, a.btid, a.min, a.gem_bfs, a.los, a.lieferdatum FROM dm01avch24d.distanz_gebaeudeeingang_lokalisationsnamepos_v a, 
  ( SELECT distanz_gebaeudeeingang_lokalisationsnamepos_v.atid, min(distanz_gebaeudeeingang_lokalisationsnamepos_v.min) AS min, distanz_gebaeudeeingang_lokalisationsnamepos_v.gem_bfs, distanz_gebaeudeeingang_lokalisationsnamepos_v.los, distanz_gebaeudeeingang_lokalisationsnamepos_v.lieferdatum FROM dm01avch24d.distanz_gebaeudeeingang_lokalisationsnamepos_v WHERE gem_bfs = ___GEM_BFS AND los = ___LOS AND lieferdatum = ___LIEFERDATUM GROUP BY distanz_gebaeudeeingang_lokalisationsnamepos_v.atid, distanz_gebaeudeeingang_lokalisationsnamepos_v.gem_bfs, distanz_gebaeudeeingang_lokalisationsnamepos_v.los, distanz_gebaeudeeingang_lokalisationsnamepos_v.lieferdatum) b 
 WHERE a.min = b.min AND a.atid::text = b.atid::text AND a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum
) b, 
dm01avch24d.gebaeudeadressen_lokalisationsnamepos_v c 

WHERE a.gem_bfs = ___GEM_BFS AND a.los = ___LOS AND a.lieferdatum = ___LIEFERDATUM AND b.gem_bfs = ___GEM_BFS AND b.los = ___LOS AND b.lieferdatum = ___LIEFERDATUM AND c.gem_bfs = ___GEM_BFS AND c.los = ___LOS AND c.lieferdatum = ___LIEFERDATUM AND b.atid::text = a.tid::text AND b.btid::text = c.tid::text AND b.gem_bfs = a.gem_bfs AND b.gem_bfs = c.gem_bfs AND b.los = a.los AND b.los = c.los AND b.lieferdatum = a.lieferdatum AND b.lieferdatum = c.lieferdatum');
INSERT INTO "inserts" VALUES(104,'INSERT INTO $$DBSCHEMA.z_v_bb_ls (bb_ogc_fid,bb_qualitaet,bb_qualitaet_txt,art,art_txt,ls_ogc_fid,liegenschaft_von,nummerteilgrundstueck,flaechenmass,geometrie,flaeche,ls_flaeche)  
SELECT 
  bodenbedeckung_boflaeche.ogc_fid as bb_ogc_fid, 
  bodenbedeckung_boflaeche.qualitaet as bb_qualitaet, 
  bodenbedeckung_boflaeche.qualitaet_txt as bb_qualitaet_txt, 
  bodenbedeckung_boflaeche.art, 
  bodenbedeckung_boflaeche.art_txt, 
  liegenschaften_liegenschaft.ogc_fid as ls_ogc_fid, 
  liegenschaften_liegenschaft.liegenschaft_von, 
  liegenschaften_liegenschaft.nummerteilgrundstueck, 
  liegenschaften_liegenschaft.flaechenmass, 
  ST_intersection(bodenbedeckung_boflaeche.geometrie,liegenschaften_liegenschaft.geometrie) as geometrie,
  ST_area (ST_intersection(bodenbedeckung_boflaeche.geometrie,liegenschaften_liegenschaft.geometrie)) as flaeche,
ST_area (liegenschaften_liegenschaft.geometrie) as ls_flaeche
FROM 
  $$DBSCHEMA.bodenbedeckung_boflaeche, 
  $$DBSCHEMA.liegenschaften_liegenschaft
WHERE 
  ST_intersects(bodenbedeckung_boflaeche.geometrie,liegenschaften_liegenschaft.geometrie)=true');
INSERT INTO "inserts" VALUES(106,'INSERT INTO $$DBSCHEMA.z_ls_entstehung
SELECT ls.ogc_fid, ls.geometrie,
gs.nummer, gs.entstehung,
ls.gem_bfs,
ls.lieferdatum, ls.los
FROM $$DBSCHEMA.liegenschaften_grundstueck gs, $$DBSCHEMA.liegenschaften_liegenschaft ls
WHERE 
ls.liegenschaft_von=gs.tid AND 
ls.los=gs.los AND 
ls.gem_bfs=gs.gem_bfs AND
ls.lieferdatum=gs.lieferdatum AND
ls.gem_bfs = ___GEM_BFS AND 
ls.los = ___LOS AND 
ls.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(107,'INSERT INTO $$DBSCHEMA.z_v_gp_ts
SELECT
  gp.tid, gp.entstehung, gp.identifikator, gp.geometrie, gp.lagegen,gp.lagezuv, gp.lagezuv_txt, gp.punktzeichen, gp.punktzeichen_txt, gp.exaktdefiniert, 
       gp.exaktdefiniert_txt, gp.hoheitsgrenzsteinalt, gp.hoheitsgrenzsteinalt_txt,
 gp.gem_bfs,
  gp.los,
  gp.lieferdatum,
  ts.art
FROM 
  $$DBSCHEMA.liegenschaften_grenzpunkt as gp, 
  $$DBSCHEMA.tseinteilung_toleranzstufe as ts
WHERE 
  ST_Intersects (gp.geometrie,ts.geometrie)=true AND
  gp.los = ts.los AND
  gp.gem_bfs = ts.gem_bfs AND
  gp.lieferdatum = ts.lieferdatum AND
  gp.gem_bfs = ___GEM_BFS AND 
  gp.los = ___LOS AND 
  gp.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(108,'INSERT INTO $$DBSCHEMA.z_liegenschaft_flaeche
SELECT tid, liegenschaft_von, nummerteilgrundstueck, geometrie, 
       flaechenmass, st_area(geometrie) as flaeche, qualitaet, qualitaet_txt, gem_bfs, los, 
       lieferdatum
  FROM $$DBSCHEMA.liegenschaften_liegenschaft where
liegenschaften_liegenschaft.gem_bfs = ___GEM_BFS AND 
liegenschaften_liegenschaft.los = ___LOS AND 
liegenschaften_liegenschaft.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(109,'INSERT INTO $$DBSCHEMA.z_selbstrecht_flaeche
SELECT tid, selbstrecht_von, nummerteilgrundstueck, geometrie, 
       flaechenmass, st_area(geometrie) as flaeche, qualitaet, qualitaet_txt, gem_bfs, los,lieferdatum
  FROM $$DBSCHEMA.liegenschaften_selbstrecht where
liegenschaften_selbstrecht.gem_bfs = ___GEM_BFS AND 
liegenschaften_selbstrecht.los = ___LOS AND 
liegenschaften_selbstrecht.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(110,'INSERT INTO $$DBSCHEMA.z_hgp_ls_linie
SELECT 
 gemeindegrenzen_hoheitsgrenzpunkt.ogc_fid, gemeindegrenzen_hoheitsgrenzpunkt.geometrie, 
 gemeindegrenzen_hoheitsgrenzpunkt.gem_bfs, 
 gemeindegrenzen_hoheitsgrenzpunkt.los, gemeindegrenzen_hoheitsgrenzpunkt.lieferdatum
 FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze, $$DBSCHEMA.gemeindegrenzen_hoheitsgrenzpunkt
 WHERE gemeindegrenzen_gemeindegrenze.gem_bfs = gemeindegrenzen_hoheitsgrenzpunkt.gem_bfs AND 
 gemeindegrenzen_gemeindegrenze.los = gemeindegrenzen_hoheitsgrenzpunkt.los 
 AND gemeindegrenzen_gemeindegrenze.lieferdatum = gemeindegrenzen_hoheitsgrenzpunkt.lieferdatum AND 
  st_touches(gemeindegrenzen_gemeindegrenze.geometrie, gemeindegrenzen_hoheitsgrenzpunkt.geometrie) IS False
 AND
gemeindegrenzen_hoheitsgrenzpunkt.gem_bfs = ___GEM_BFS AND 
gemeindegrenzen_hoheitsgrenzpunkt.los = ___LOS AND 
gemeindegrenzen_hoheitsgrenzpunkt.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(111,'INSERT INTO $$DBSCHEMA.z_v_ls_nk
SELECT 
  liegenschaften_liegenschaft.ogc_fid as ls_fid, 
  nomenklatur_flurname.ogc_fid as nk_fid,
 st_intersection(nomenklatur_flurname.geometrie,   liegenschaften_liegenschaft.geometrie) as geometrie,
  liegenschaften_liegenschaft.gem_bfs, 
  liegenschaften_liegenschaft.los, 
  liegenschaften_liegenschaft.lieferdatum,
 st_area ( st_intersection(nomenklatur_flurname.geometrie,   liegenschaften_liegenschaft.geometrie)) as flaeche

FROM 
  $$DBSCHEMA.liegenschaften_liegenschaft, 
  $$DBSCHEMA.nomenklatur_flurname
WHERE 
  liegenschaften_liegenschaft.gem_bfs = nomenklatur_flurname.gem_bfs AND
  liegenschaften_liegenschaft.los = nomenklatur_flurname.los AND
  liegenschaften_liegenschaft.lieferdatum = nomenklatur_flurname.lieferdatum and
  st_intersects(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie)=true and
  ST_IsValid(st_intersection(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie))=true AND
nomenklatur_flurname.gem_bfs = ___GEM_BFS AND 
nomenklatur_flurname.los = ___LOS AND 
nomenklatur_flurname.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(112,'INSERT INTO $$DBSCHEMA.z_nr_gs
SELECT DISTINCT
  liegenschaften_grundstueck.nbident, 
  liegenschaften_grundstueck.nummer, 
  liegenschaften_grundstueck.egris_egrid, 
  liegenschaften_grundstueck.gueltigkeit, 
  liegenschaften_grundstueck.gueltigkeit_txt, 
  liegenschaften_grundstueck.vollstaendigkeit, 
  liegenschaften_grundstueck.vollstaendigkeit_txt, 
  liegenschaften_grundstueck.art, 
  liegenschaften_grundstueck.art_txt, 
  liegenschaften_grundstueck.gesamteflaechenmass, 
  liegenschaften_grundstueck.gem_bfs, 
  liegenschaften_grundstueck.los, 
  liegenschaften_grundstueck.lieferdatum, 
  liegenschaften_selbstrecht.nummerteilgrundstueck, 
  liegenschaften_grundstueckpos.pos,
  (case(st_contains(liegenschaften_selbstrecht.geometrie,liegenschaften_grundstueckpos.pos)) when false then 1 else 0 end) as lin
FROM 
  $$DBSCHEMA.liegenschaften_selbstrecht, 
  $$DBSCHEMA.liegenschaften_grundstueck, 
  $$DBSCHEMA.liegenschaften_grundstueckpos
WHERE 
  liegenschaften_grundstueck.gesamteflaechenmass is NULL AND
  liegenschaften_grundstueck.tid = liegenschaften_selbstrecht.selbstrecht_von AND
  liegenschaften_grundstueckpos.grundstueckpos_von = liegenschaften_grundstueck.tid AND
  liegenschaften_grundstueck.gem_bfs = ___GEM_BFS AND 
  liegenschaften_grundstueck.los = ___LOS AND 
  liegenschaften_grundstueck.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_selbstrecht.gem_bfs = ___GEM_BFS AND 
  liegenschaften_selbstrecht.los = ___LOS AND 
  liegenschaften_selbstrecht.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_grundstueckpos.gem_bfs = ___GEM_BFS AND 
  liegenschaften_grundstueckpos.los = ___LOS AND 
  liegenschaften_grundstueckpos.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(113,'INSERT INTO $$DBSCHEMA.z_nr_gs
SELECT DISTINCT
  liegenschaften_grundstueck.nbident, 
  liegenschaften_grundstueck.nummer, 
  liegenschaften_grundstueck.egris_egrid, 
  liegenschaften_grundstueck.gueltigkeit, 
  liegenschaften_grundstueck.gueltigkeit_txt, 
  liegenschaften_grundstueck.vollstaendigkeit, 
  liegenschaften_grundstueck.vollstaendigkeit_txt, 
  liegenschaften_grundstueck.art, 
  liegenschaften_grundstueck.art_txt, 
  liegenschaften_grundstueck.gesamteflaechenmass, 
  liegenschaften_grundstueck.gem_bfs, 
  liegenschaften_grundstueck.los, 
  liegenschaften_grundstueck.lieferdatum, 
  liegenschaften_liegenschaft.nummerteilgrundstueck, 
  liegenschaften_grundstueckpos.pos,
  (case (st_contains(liegenschaften_liegenschaft.geometrie,liegenschaften_grundstueckpos.pos)) When False Then 1 Else 0 End) as lin
FROM 
  $$DBSCHEMA.liegenschaften_liegenschaft, 
  $$DBSCHEMA.liegenschaften_grundstueck, 
  $$DBSCHEMA.liegenschaften_grundstueckpos
WHERE 
  liegenschaften_grundstueck.gesamteflaechenmass is NULL AND
  liegenschaften_grundstueck.tid = liegenschaften_liegenschaft.liegenschaft_von AND
  liegenschaften_grundstueckpos.grundstueckpos_von = liegenschaften_grundstueck.tid AND
  liegenschaften_grundstueck.gem_bfs = ___GEM_BFS AND 
  liegenschaften_grundstueck.los = ___LOS AND 
  liegenschaften_grundstueck.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_liegenschaft.gem_bfs = ___GEM_BFS AND 
  liegenschaften_liegenschaft.los = ___LOS AND 
  liegenschaften_liegenschaft.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_grundstueckpos.gem_bfs = ___GEM_BFS AND 
  liegenschaften_grundstueckpos.los = ___LOS AND 
  liegenschaften_grundstueckpos.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(114,'INSERT INTO $$DBSCHEMA.z_v_ls_nk_pkt
SELECT 
  liegenschaften_liegenschaft.ogc_fid as ls_fid, 
  nomenklatur_flurname.ogc_fid as nk_fid,
  liegenschaften_liegenschaft.gem_bfs, 
  liegenschaften_liegenschaft.los, 
  liegenschaften_liegenschaft.lieferdatum,
 st_area ( st_intersection(nomenklatur_flurname.geometrie,   liegenschaften_liegenschaft.geometrie)) as flaeche, 
 st_PointonSurface(st_intersection(nomenklatur_flurname.geometrie,liegenschaften_liegenschaft.geometrie)) as geometrie
 from $$DBSCHEMA.liegenschaften_liegenschaft, 
  $$DBSCHEMA.nomenklatur_flurname
WHERE 
  liegenschaften_liegenschaft.gem_bfs = nomenklatur_flurname.gem_bfs AND
  liegenschaften_liegenschaft.los = nomenklatur_flurname.los AND
  liegenschaften_liegenschaft.lieferdatum = nomenklatur_flurname.lieferdatum and
  st_intersects(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie)=true and
  ST_IsValid(st_intersection(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie))=true AND
nomenklatur_flurname.gem_bfs = ___GEM_BFS AND 
nomenklatur_flurname.los = ___LOS AND 
nomenklatur_flurname.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(115,'INSERT INTO $$DBSCHEMA.z_nr_gs
SELECT DISTINCT
  liegenschaften_grundstueck.nbident, 
  liegenschaften_grundstueck.nummer, 
  liegenschaften_grundstueck.egris_egrid, 
  liegenschaften_grundstueck.gueltigkeit, 
  liegenschaften_grundstueck.gueltigkeit_txt, 
  liegenschaften_grundstueck.vollstaendigkeit, 
  liegenschaften_grundstueck.vollstaendigkeit_txt, 
  liegenschaften_grundstueck.art, 
  liegenschaften_grundstueck.art_txt, 
  liegenschaften_grundstueck.gesamteflaechenmass, 
  liegenschaften_grundstueck.gem_bfs, 
  liegenschaften_grundstueck.los, 
  liegenschaften_grundstueck.lieferdatum, 
  liegenschaften_selbstrecht.nummerteilgrundstueck, 
  liegenschaften_teilsrpos.pos,
  (case(st_contains(liegenschaften_selbstrecht.geometrie,liegenschaften_teilsrpos.pos))when false then 1 else 0 end) as Lin
FROM 
  $$DBSCHEMA.liegenschaften_selbstrecht, 
  $$DBSCHEMA.liegenschaften_grundstueck, 
  $$DBSCHEMA.liegenschaften_teilsrpos
WHERE 
  liegenschaften_grundstueck.gesamteflaechenmass >0 AND
  liegenschaften_grundstueck.tid = liegenschaften_selbstrecht.selbstrecht_von AND
  liegenschaften_teilsrpos.teilsrpos_von = liegenschaften_selbstrecht.tid AND
  liegenschaften_grundstueck.gem_bfs = ___GEM_BFS AND 
  liegenschaften_grundstueck.los = ___LOS AND 
  liegenschaften_grundstueck.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_selbstrecht.gem_bfs = ___GEM_BFS AND 
  liegenschaften_selbstrecht.los = ___LOS AND 
  liegenschaften_selbstrecht.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_teilsrpos.gem_bfs = ___GEM_BFS AND 
  liegenschaften_teilsrpos.los = ___LOS AND 
  liegenschaften_teilsrpos.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(116,'INSERT INTO $$DBSCHEMA.z_nr_gs
SELECT DISTINCT
  liegenschaften_grundstueck.nbident, 
  liegenschaften_grundstueck.nummer, 
  liegenschaften_grundstueck.egris_egrid, 
  liegenschaften_grundstueck.gueltigkeit, 
  liegenschaften_grundstueck.gueltigkeit_txt, 
  liegenschaften_grundstueck.vollstaendigkeit, 
  liegenschaften_grundstueck.vollstaendigkeit_txt, 
  liegenschaften_grundstueck.art, 
  liegenschaften_grundstueck.art_txt, 
  liegenschaften_grundstueck.gesamteflaechenmass, 
  liegenschaften_grundstueck.gem_bfs, 
  liegenschaften_grundstueck.los, 
  liegenschaften_grundstueck.lieferdatum, 
  liegenschaften_liegenschaft.nummerteilgrundstueck, 
  liegenschaften_teillspos.pos,
  (case(st_contains(liegenschaften_liegenschaft.geometrie,liegenschaften_teillspos.pos)) when false Then 1 else 0 end) as Lin
FROM 
  $$DBSCHEMA.liegenschaften_liegenschaft, 
  $$DBSCHEMA.liegenschaften_grundstueck, 
  $$DBSCHEMA.liegenschaften_teillspos
WHERE 
  liegenschaften_grundstueck.gesamteflaechenmass >0 AND
  liegenschaften_grundstueck.tid = liegenschaften_liegenschaft.liegenschaft_von AND
  liegenschaften_teillspos.teillspos_von = liegenschaften_liegenschaft.tid AND
  liegenschaften_grundstueck.gem_bfs = ___GEM_BFS AND 
  liegenschaften_grundstueck.los = ___LOS AND 
  liegenschaften_grundstueck.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_liegenschaft.gem_bfs = ___GEM_BFS AND 
  liegenschaften_liegenschaft.los = ___LOS AND 
  liegenschaften_liegenschaft.lieferdatum = ___LIEFERDATUM AND
  liegenschaften_teillspos.gem_bfs = ___GEM_BFS AND 
  liegenschaften_teillspos.los = ___LOS AND 
  liegenschaften_teillspos.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(117,'INSERT INTO $$DBSCHEMA.z_objektnummer_pos
SELECT 
  einzelobjekte_objektnummer.nummer, 
  einzelobjekte_objektnummer.gwr_egid, 
  einzelobjekte_objektnummer.nbident, 
  einzelobjekte_objektnummerpos.pos, 
  einzelobjekte_objektnummerpos.ori, 
  einzelobjekte_objektnummerpos.groesse, 
  einzelobjekte_objektnummerpos.vali_txt, 
  einzelobjekte_objektnummerpos.vali, 
  einzelobjekte_objektnummerpos.hali_txt, 
  einzelobjekte_objektnummerpos.hali, 
  einzelobjekte_objektnummerpos.groesse_txt,
  einzelobjekte_objektnummer.gem_bfs,
  einzelobjekte_objektnummer.los,
  einzelobjekte_objektnummer.lieferdatum
FROM 
  $$DBSCHEMA.einzelobjekte_objektnummer, 
  $$DBSCHEMA.einzelobjekte_objektnummerpos
WHERE 
  einzelobjekte_objektnummer.gem_bfs = einzelobjekte_objektnummerpos.gem_bfs AND
  einzelobjekte_objektnummer.los = einzelobjekte_objektnummerpos.los AND
  einzelobjekte_objektnummer.lieferdatum = einzelobjekte_objektnummerpos.lieferdatum AND
  einzelobjekte_objektnummer.tid = einzelobjekte_objektnummerpos.objektnummerpos_von AND
  einzelobjekte_objektnummer.gem_bfs = ___GEM_BFS AND 
  einzelobjekte_objektnummer.los = ___LOS AND 
  einzelobjekte_objektnummer.lieferdatum = ___LIEFERDATUM');
INSERT INTO "inserts" VALUES(118,'INSERT INTO $$DBSCHEMA.z_gebaeudenummer_pos
SELECT 
  bodenbedeckung_gebaeudenummer.nummer, 
  bodenbedeckung_gebaeudenummer.gwr_egid, 
  bodenbedeckung_gebaeudenummer.nbident, 
  bodenbedeckung_gebaeudenummerpos.pos, 
  bodenbedeckung_gebaeudenummerpos.ori, 
  bodenbedeckung_gebaeudenummerpos.groesse, 
  bodenbedeckung_gebaeudenummerpos.vali_txt, 
  bodenbedeckung_gebaeudenummerpos.vali, 
  bodenbedeckung_gebaeudenummerpos.hali_txt, 
  bodenbedeckung_gebaeudenummerpos.hali, 
  bodenbedeckung_gebaeudenummerpos.groesse_txt,
  bodenbedeckung_gebaeudenummer.gem_bfs,
  bodenbedeckung_gebaeudenummer.los,
  bodenbedeckung_gebaeudenummer.lieferdatum
FROM 
  $$DBSCHEMA.bodenbedeckung_gebaeudenummer, 
  $$DBSCHEMA.bodenbedeckung_gebaeudenummerpos
WHERE 
  bodenbedeckung_gebaeudenummer.gem_bfs = bodenbedeckung_gebaeudenummerpos.gem_bfs AND
  bodenbedeckung_gebaeudenummer.los = bodenbedeckung_gebaeudenummerpos.los AND
  bodenbedeckung_gebaeudenummer.lieferdatum = bodenbedeckung_gebaeudenummerpos.lieferdatum AND
  bodenbedeckung_gebaeudenummer.tid = bodenbedeckung_gebaeudenummerpos.gebaeudenummerpos_von AND
  bodenbedeckung_gebaeudenummer.gem_bfs = ___GEM_BFS AND 
  bodenbedeckung_gebaeudenummer.los = ___LOS AND 
  bodenbedeckung_gebaeudenummer.lieferdatum = ___LIEFERDATUM');

  INSERT INTO "views" VALUES(101,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_flaechenelement_v AS 
 SELECT b.ogc_fid, b.tid, b.flaechenelement_von, b.geometrie, b.gem_bfs, b.los, b.lieferdatum, a.art, a.art_txt, a.qualitaet_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt a, $$DBSCHEMA.einzelobjekte_flaechenelement b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND b.flaechenelement_von::text = a.tid::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_flaechenelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_flaechenelement_v TO $$USER;');


INSERT INTO "views" VALUES(102,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_linienelement_v AS 
 SELECT b.ogc_fid, b.tid, b.linienelement_von, b.geometrie, b.gem_bfs, b.los, b.lieferdatum, a.art, a.art_txt, a.qualitaet_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt a, $$DBSCHEMA.einzelobjekte_linienelement b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND b.linienelement_von::text = a.tid::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_linienelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_linienelement_v TO $$USER;');


INSERT INTO "views" VALUES(103,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_objektnamepos_v AS 
 SELECT einzelobjekte_objektname.lieferdatum, einzelobjekte_objektname.los, einzelobjekte_objektname.gem_bfs, einzelobjekte_objektname.name, einzelobjekte_objektnamepos.pos, einzelobjekte_objektnamepos.ogc_fid
   FROM $$DBSCHEMA.einzelobjekte_objektname, $$DBSCHEMA.einzelobjekte_objektnamepos
  WHERE einzelobjekte_objektname.tid::text = einzelobjekte_objektnamepos.objektnamepos_von::text AND einzelobjekte_objektname.gem_bfs = einzelobjekte_objektnamepos.gem_bfs AND einzelobjekte_objektname.los = einzelobjekte_objektnamepos.los AND einzelobjekte_objektname.lieferdatum = einzelobjekte_objektnamepos.lieferdatum;

ALTER TABLE $$DBSCHEMA.einzelobjekte_objektnamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_objektnamepos_v TO $$USER;');


INSERT INTO "views" VALUES(104,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_punktelement_v AS 
 SELECT b.ogc_fid, b.tid, b.punktelement_von, b.geometrie, b.gem_bfs, b.los, b.lieferdatum, a.art, a.art_txt, a.qualitaet_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt a, $$DBSCHEMA.einzelobjekte_punktelement b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND b.punktelement_von::text = a.tid::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_punktelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_punktelement_v TO $$USER;');


INSERT INTO "views" VALUES(105,'CREATE OR REPLACE VIEW $$DBSCHEMA.fixpunktekategorie3_lfp3_ausserhalb_perimeter_v AS 
 SELECT a.ogc_fid, a.tid, a.entstehung, a.nbident, a.nummer, a.geometrie, a.hoehegeom, a.lagegen, a.lagezuv, a.lagezuv_txt, a.hoehegen, a.hoehezuv, a.hoehezuv_txt, a.punktzeichen, a.punktzeichen_txt, a.protokoll, a.protokoll_txt, a.gem_bfs, a.los, a.lieferdatum, st_distance(a.geometrie, b.geometrie) AS distance
   FROM $$DBSCHEMA.fixpunktekategorie3_lfp3 a, ( SELECT tseinteilung_toleranzstufe.gem_bfs, tseinteilung_toleranzstufe.los, tseinteilung_toleranzstufe.lieferdatum, st_multi(st_union(tseinteilung_toleranzstufe.geometrie)) AS geometrie
           FROM $$DBSCHEMA.tseinteilung_toleranzstufe
          GROUP BY tseinteilung_toleranzstufe.gem_bfs, tseinteilung_toleranzstufe.los, tseinteilung_toleranzstufe.lieferdatum) b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND st_distance(a.geometrie, b.geometrie) > 0::double precision;

ALTER TABLE $$DBSCHEMA.fixpunktekategorie3_lfp3_ausserhalb_perimeter_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.fixpunktekategorie3_lfp3_ausserhalb_perimeter_v TO $$USER;
GRANT SELECT ON TABLE $$DBSCHEMA.fixpunktekategorie3_lfp3_ausserhalb_perimeter_v TO mspublic;
COMMENT ON VIEW $$DBSCHEMA.fixpunktekategorie3_lfp3_ausserhalb_perimeter_v
  IS 'LFP3 ausserhalb des Gemeindeperimeters.';');

INSERT INTO "views" VALUES(106,'CREATE OR REPLACE VIEW $$DBSCHEMA.fixpunktekategorie3_lfp3_pro_toleranzstufe_v AS 
 SELECT a.ogc_fid, a.art + 1 AS toleranzstufe, round((area(a.geometrie) / 10000::double precision)::numeric, 2) AS ts_hektare, count(b.tid) AS ist, 
        CASE
            WHEN a.art = 0 THEN round(150::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 1 THEN round(70::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 2 THEN round(20::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 3 THEN round(10::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 4 THEN round(2::double precision * area(a.geometrie) / 1000000::double precision)
            ELSE NULL::double precision
        END AS soll, 
        CASE
            WHEN a.art = 0 THEN count(b.tid)::double precision - round(150::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 1 THEN count(b.tid)::double precision - round(70::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 2 THEN count(b.tid)::double precision - round(20::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 3 THEN count(b.tid)::double precision - round(10::double precision * area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 4 THEN count(b.tid)::double precision - round(2::double precision * area(a.geometrie) / 1000000::double precision)
            ELSE NULL::double precision
        END AS diff, a.gem_bfs, a.los, a.lieferdatum
   FROM $$DBSCHEMA.tseinteilung_toleranzstufe a, $$DBSCHEMA.fixpunktekategorie3_lfp3 b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND st_distance(a.geometrie, b.geometrie) = 0::double precision
  GROUP BY a.art, a.geometrie, a.ogc_fid, a.gem_bfs, a.los, a.lieferdatum
  ORDER BY a.art;

ALTER TABLE $$DBSCHEMA.fixpunktekategorie3_lfp3_pro_toleranzstufe_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.fixpunktekategorie3_lfp3_pro_toleranzstufe_v TO $$USER;
GRANT SELECT ON TABLE $$DBSCHEMA.fixpunktekategorie3_lfp3_pro_toleranzstufe_v TO mspublic;
COMMENT ON VIEW $$DBSCHEMA.fixpunktekategorie3_lfp3_pro_toleranzstufe_v
  IS 'LFP3 pro Toleranzstufe.';');


INSERT INTO "views" VALUES(107,'CREATE OR REPLACE VIEW $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v AS 
 SELECT b.ogc_fid, b.tid, b.lokalisationsnamepos_von, b.anfindex, b.endindex, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, b.hilfslinie, b.gem_bfs, b.los, b.lieferdatum, st_x(b.pos) AS y, st_y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS ori_neu, a.benannte, a.text
   FROM $$DBSCHEMA.gebaeudeadressen_lokalisationsname a, $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.lokalisationsnamepos_von::text;

ALTER TABLE $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v TO $$USER;
COMMENT ON VIEW $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v
  IS 'LokalisationsNamePos View mit verschiedenen Attributen von Lokalisationsname.';');


INSERT INTO "views" VALUES(108,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_liegenschaft_v AS 
 SELECT a.ogc_fid, a.tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, a.gem_bfs, a.los, a.lieferdatum, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_liegenschaft b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.liegenschaft_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v TO $$USER;');


INSERT INTO "views" VALUES(109,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_liegenschaft_v2 AS 
 SELECT b.ogc_fid, a.tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, a.gem_bfs, a.los, a.lieferdatum, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_liegenschaft b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.liegenschaft_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v2
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v2 TO $$USER;');


INSERT INTO "views" VALUES(110,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_projliegenschaft_v AS 
 SELECT a.ogc_fid, a.tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, a.gem_bfs, a.los, a.lieferdatum, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_projliegenschaft b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.projliegenschaft_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_projliegenschaft_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_projliegenschaft_v TO $$USER;');


INSERT INTO "views" VALUES(111,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_projselbstrecht_v AS 
 SELECT a.ogc_fid, a.tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, a.gem_bfs, a.los, a.lieferdatum, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_projselbstrecht b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.projselbstrecht_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_projselbstrecht_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_projselbstrecht_v TO $$USER;');


INSERT INTO "views" VALUES(112,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_selbstrecht_v AS 
 SELECT a.ogc_fid, a.tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, a.gem_bfs, a.los, a.lieferdatum, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_selbstrecht b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.selbstrecht_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_selbstrecht_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_selbstrecht_v TO $$USER;');

INSERT INTO "views" VALUES(113,'CREATE OR REPLACE VIEW $$DBSCHEMA.nomenklatur_gelaendenamepos_v AS 
 SELECT b.ogc_fid, b.tid, b.gelaendenamepos_von, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, b.stil, b.stil_txt, b.gem_bfs, b.los, b.lieferdatum, st_x(b.pos) AS y, st_y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.name
   FROM $$DBSCHEMA.nomenklatur_gelaendename a, $$DBSCHEMA.nomenklatur_gelaendenamepos b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.gelaendenamepos_von::text;

ALTER TABLE $$DBSCHEMA.nomenklatur_gelaendenamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.nomenklatur_gelaendenamepos_v TO $$USER;');


INSERT INTO "views" VALUES(114,'CREATE OR REPLACE VIEW $$DBSCHEMA.planeinteilungen_plan_v AS 
 SELECT a.ogc_fid, a.tid, a.nbident, a.nummer, a.techdossier, a.gueltigereintrag, a.gem_bfs, a.los, a.lieferdatum, b.geometrie
   FROM $$DBSCHEMA.planeinteilungen_plan a, $$DBSCHEMA.planeinteilungen_plangeometrie b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.plangeometrie_von::text;

ALTER TABLE $$DBSCHEMA.planeinteilungen_plan_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.planeinteilungen_plan_v TO $$USER;
COMMENT ON VIEW $$DBSCHEMA.planeinteilungen_plan_v
  IS 'Planeinteilung.';');


INSERT INTO "views" VALUES(115,'CREATE OR REPLACE VIEW $$DBSCHEMA.rohrleitungen_leitungsobjekt_v AS 
 SELECT rohrleitungen_leitungsobjekt.qualitaet_txt, rohrleitungen_leitungsobjekt.betreiber, rohrleitungen_leitungsobjekt.tid, rohrleitungen_leitungsobjekt.art_txt, rohrleitungen_leitungsobjektpos.ogc_fid, rohrleitungen_leitungsobjektpos.pos, rohrleitungen_leitungsobjektpos.gem_bfs, rohrleitungen_leitungsobjektpos.los, rohrleitungen_leitungsobjektpos.lieferdatum, rohrleitungen_leitungsobjektpos.leitungsobjektpos_von
   FROM $$DBSCHEMA.rohrleitungen_leitungsobjekt, $$DBSCHEMA.rohrleitungen_leitungsobjektpos
  WHERE rohrleitungen_leitungsobjekt.tid::text = rohrleitungen_leitungsobjektpos.leitungsobjektpos_von::text AND rohrleitungen_leitungsobjekt.gem_bfs = rohrleitungen_leitungsobjektpos.gem_bfs AND rohrleitungen_leitungsobjekt.los = rohrleitungen_leitungsobjektpos.los AND rohrleitungen_leitungsobjekt.lieferdatum = rohrleitungen_leitungsobjektpos.lieferdatum;

ALTER TABLE $$DBSCHEMA.rohrleitungen_leitungsobjekt_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.rohrleitungen_leitungsobjekt_v TO $$USER;');


INSERT INTO "views" VALUES(116,'CREATE OR REPLACE VIEW $$DBSCHEMA.rohrleitungen_linienelement_v AS 
 SELECT b.ogc_fid, b.tid, b.linienelement_von, b.geometrie, b.linienart, b.linienart_txt, b.gem_bfs, b.los, b.lieferdatum, a.betreiber, a.qualitaet, a.qualitaet_txt, a.art, a.art_txt
   FROM $$DBSCHEMA.rohrleitungen_leitungsobjekt a, $$DBSCHEMA.rohrleitungen_linienelement b
  WHERE a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum AND a.tid::text = b.linienelement_von::text;

ALTER TABLE $$DBSCHEMA.rohrleitungen_linienelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.rohrleitungen_linienelement_v TO $$USER;');


INSERT INTO "views" VALUES(117,'CREATE OR REPLACE VIEW $$DBSCHEMA.spiderweb_v AS 
 SELECT a.ogc_fid, a.tid, geometryfromtext(((((((('LINESTRING('::text || x(a.lage)::text) || ' '::text) || y(a.lage)::text) || ','::text) || x(c.pos)::text) || ' '::text) || y(c.pos)::text) || ')'::text, 21781) AS line, a.hausnummer, a.gem_bfs, a.los, a.lieferdatum
   FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, ( SELECT a.atid, a.btid, a.min, a.gem_bfs, a.los, a.lieferdatum
           FROM $$DBSCHEMA.distanz_gebaeudeeingang_lokalisationsnamepos_v a, ( SELECT distanz_gebaeudeeingang_lokalisationsnamepos_v.atid, min(distanz_gebaeudeeingang_lokalisationsnamepos_v.min) AS min, distanz_gebaeudeeingang_lokalisationsnamepos_v.gem_bfs, distanz_gebaeudeeingang_lokalisationsnamepos_v.los, distanz_gebaeudeeingang_lokalisationsnamepos_v.lieferdatum
                   FROM $$DBSCHEMA.distanz_gebaeudeeingang_lokalisationsnamepos_v
                  GROUP BY distanz_gebaeudeeingang_lokalisationsnamepos_v.atid, distanz_gebaeudeeingang_lokalisationsnamepos_v.gem_bfs, distanz_gebaeudeeingang_lokalisationsnamepos_v.los, distanz_gebaeudeeingang_lokalisationsnamepos_v.lieferdatum) b
          WHERE a.min = b.min AND a.atid::text = b.atid::text AND a.gem_bfs = b.gem_bfs AND a.los = b.los AND a.lieferdatum = b.lieferdatum) b, $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v c
  WHERE b.atid::text = a.tid::text AND b.btid::text = c.tid::text AND b.gem_bfs = a.gem_bfs AND b.gem_bfs = c.gem_bfs AND b.los = a.los AND b.los = c.los AND b.lieferdatum = a.lieferdatum AND b.lieferdatum = c.lieferdatum;

ALTER TABLE $$DBSCHEMA.spiderweb_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.spiderweb_v TO $$USER;
COMMENT ON VIEW $$DBSCHEMA.spiderweb_v
  IS 'Spinnennetz: Linie vom Gebäudeeingang zum nächsten LokalisationsnamePos.';');


INSERT INTO "views" VALUES(118,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp AS 
 SELECT a.ogc_fid, a.tid, a.entstehung, a.identifikator, a.geometrie, a.lagegen, a.lagezuv, a.lagezuv_txt, a.punktzeichen, a.punktzeichen_txt, a.exaktdefiniert, a.exaktdefiniert_txt, a.hoheitsgrenzsteinalt, a.hoheitsgrenzsteinalt_txt, a.gem_bfs, a.los, a.lieferdatum
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt a
  WHERE NOT (a.ogc_fid IN (        (        (         SELECT b.ogc_fid
                                   FROM $$DBSCHEMA.test_gp_ls b
                        UNION 
                                 SELECT c.ogc_fid
                                   FROM $$DBSCHEMA.test_gp_sdr c)
                UNION 
                         SELECT d.ogc_fid
                           FROM $$DBSCHEMA.test_gp_projls d)
        UNION 
                 SELECT e.ogc_fid
                   FROM $$DBSCHEMA.test_gp_projsdr e));

ALTER TABLE $$DBSCHEMA.test_gp
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp TO $$USER;');


INSERT INTO "views" VALUES(119,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_ls AS 
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_liegenschaft ls
  WHERE b.gem_bfs = ls.gem_bfs AND b.los = ls.los AND b.lieferdatum = ls.lieferdatum AND st_touches(b.geometrie, ls.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_ls TO $$USER;');

INSERT INTO "views" VALUES(120,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_projls AS 
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projliegenschaft
  WHERE b.gem_bfs = liegenschaften_projliegenschaft.gem_bfs AND b.los = liegenschaften_projliegenschaft.los AND b.lieferdatum = liegenschaften_projliegenschaft.lieferdatum AND st_touches(b.geometrie, liegenschaften_projliegenschaft.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_projls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_projls TO $$USER;');


INSERT INTO "views" VALUES(121,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_projsdr AS 
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projselbstrecht
  WHERE b.gem_bfs = liegenschaften_projselbstrecht.gem_bfs AND b.los = liegenschaften_projselbstrecht.los AND b.lieferdatum = liegenschaften_projselbstrecht.lieferdatum AND st_touches(b.geometrie, liegenschaften_projselbstrecht.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_projsdr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_projsdr TO $$USER;');


INSERT INTO "views" VALUES(122,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_sdr AS 
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_selbstrecht
  WHERE b.gem_bfs = liegenschaften_selbstrecht.gem_bfs AND b.los = liegenschaften_selbstrecht.los AND b.lieferdatum = liegenschaften_selbstrecht.lieferdatum AND st_touches(b.geometrie, liegenschaften_selbstrecht.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_sdr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_sdr TO $$USER;');


INSERT INTO "views" VALUES(123,'CREATE OR REPLACE VIEW $$DBSCHEMA.verschnitt_ls_bb AS 
 SELECT nextval('$$DBSCHEMA.bodenbedeckung_boflaeche_ogc_fid_seq'::regclass)::oid AS fid_oid, bb.art, ls.liegenschaft_von, area(intersection(bb.geometrie, ls.geometrie)) AS flaeche, intersection(bb.geometrie, ls.geometrie) AS geometrie, ls.gem_bfs, ls.los, ls.lieferdatum, nextval('$$DBSCHEMA.v_pkey'::regclass)::oid AS pkey
   FROM $$DBSCHEMA.bodenbedeckung_boflaeche bb, $$DBSCHEMA.liegenschaften_liegenschaft ls
  WHERE isempty(intersection(bb.geometrie, ls.geometrie)) = false AND ls.gem_bfs = bb.gem_bfs AND ls.los = bb.los AND ls.lieferdatum = bb.lieferdatum;

ALTER TABLE $$DBSCHEMA.verschnitt_ls_bb
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.verschnitt_ls_bb TO $$USER;');

INSERT INTO "views" VALUES(124,'CREATE OR REPLACE VIEW $$DBSCHEMA."z_Geb_Strassen_Ortschaft" AS 
 SELECT gebaeudeadressen_strassenstueck.gem_bfs, gebaeudeadressen_strassenstueck.los, gebaeudeadressen_strassenstueck.lieferdatum, gebaeudeadressen_strassenstueck.geometrie, gebaeudeadressen_strassenstueck.ogc_fid
   FROM $$DBSCHEMA.plzortschaft_ortschaft, $$DBSCHEMA.gebaeudeadressen_strassenstueck
  WHERE plzortschaft_ortschaft.gem_bfs = gebaeudeadressen_strassenstueck.gem_bfs AND plzortschaft_ortschaft.los = gebaeudeadressen_strassenstueck.los AND plzortschaft_ortschaft.lieferdatum = gebaeudeadressen_strassenstueck.lieferdatum AND st_touches(gebaeudeadressen_strassenstueck.geometrie, plzortschaft_ortschaft.flaeche) IS TRUE;

ALTER TABLE $$DBSCHEMA."z_Geb_Strassen_Ortschaft"
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA."z_Geb_Strassen_Ortschaft" TO $$USER;');


INSERT INTO "views" VALUES(125,'CREATE OR REPLACE VIEW $$DBSCHEMA."z_benGeb_Ortschaft" AS 
 SELECT gebaeudeadressen_benanntesgebiet.ogc_fid, gebaeudeadressen_benanntesgebiet.gem_bfs, gebaeudeadressen_benanntesgebiet.los, gebaeudeadressen_benanntesgebiet.lieferdatum, gebaeudeadressen_benanntesgebiet.flaeche
   FROM $$DBSCHEMA.gebaeudeadressen_benanntesgebiet, $$DBSCHEMA.plzortschaft_ortschaft
  WHERE gebaeudeadressen_benanntesgebiet.gem_bfs = plzortschaft_ortschaft.gem_bfs AND gebaeudeadressen_benanntesgebiet.los = plzortschaft_ortschaft.los AND gebaeudeadressen_benanntesgebiet.lieferdatum = plzortschaft_ortschaft.lieferdatum AND st_touches(gebaeudeadressen_benanntesgebiet.flaeche, plzortschaft_ortschaft.flaeche) IS TRUE;

ALTER TABLE $$DBSCHEMA."z_benGeb_Ortschaft"
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA."z_benGeb_Ortschaft" TO $$USER;');


INSERT INTO "views" VALUES(126,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_eo_flaeche AS 
 SELECT einzelobjekte_flaechenelement.ogc_fid AS ctid, einzelobjekte_flaechenelement.geometrie, einzelobjekte_einzelobjekt.tid, einzelobjekte_einzelobjekt.entstehung, einzelobjekte_einzelobjekt.qualitaet, einzelobjekte_einzelobjekt.qualitaet_txt, einzelobjekte_einzelobjekt.art, einzelobjekte_einzelobjekt.los, einzelobjekte_einzelobjekt.gem_bfs, einzelobjekte_einzelobjekt.art_txt, einzelobjekte_einzelobjekt.lieferdatum
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt, $$DBSCHEMA.einzelobjekte_flaechenelement
  WHERE einzelobjekte_flaechenelement.flaechenelement_von::text = einzelobjekte_einzelobjekt.tid::text AND einzelobjekte_flaechenelement.gem_bfs = einzelobjekte_einzelobjekt.gem_bfs AND einzelobjekte_flaechenelement.los = einzelobjekte_einzelobjekt.los AND einzelobjekte_flaechenelement.lieferdatum = einzelobjekte_einzelobjekt.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_eo_flaeche
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_eo_flaeche TO $$USER;');


INSERT INTO "views" VALUES(127,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_eo_linie AS 
 SELECT einzelobjekte_einzelobjekt.entstehung, einzelobjekte_einzelobjekt.tid, einzelobjekte_einzelobjekt.qualitaet, einzelobjekte_einzelobjekt.qualitaet_txt, einzelobjekte_einzelobjekt.art, einzelobjekte_einzelobjekt.art_txt, einzelobjekte_einzelobjekt.gem_bfs, einzelobjekte_einzelobjekt.los, einzelobjekte_einzelobjekt.lieferdatum, einzelobjekte_linienelement.geometrie, einzelobjekte_linienelement.ogc_fid AS ctid
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt, $$DBSCHEMA.einzelobjekte_linienelement
  WHERE einzelobjekte_linienelement.linienelement_von::text = einzelobjekte_einzelobjekt.tid::text AND einzelobjekte_linienelement.gem_bfs = einzelobjekte_einzelobjekt.gem_bfs AND einzelobjekte_linienelement.los = einzelobjekte_einzelobjekt.los AND einzelobjekte_linienelement.lieferdatum = einzelobjekte_einzelobjekt.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_eo_linie
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_eo_linie TO $$USER;');


INSERT INTO "views" VALUES(128,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_eo_punkt AS 
 SELECT einzelobjekte_punktelement.ogc_fid AS ctid, einzelobjekte_punktelement.geometrie, einzelobjekte_einzelobjekt.tid, einzelobjekte_einzelobjekt.entstehung, einzelobjekte_einzelobjekt.qualitaet, einzelobjekte_einzelobjekt.qualitaet_txt, einzelobjekte_einzelobjekt.art, einzelobjekte_einzelobjekt.los, einzelobjekte_einzelobjekt.gem_bfs, einzelobjekte_einzelobjekt.art_txt, einzelobjekte_einzelobjekt.lieferdatum
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt, $$DBSCHEMA.einzelobjekte_punktelement
  WHERE einzelobjekte_punktelement.punktelement_von::text = einzelobjekte_einzelobjekt.tid::text AND einzelobjekte_punktelement.gem_bfs = einzelobjekte_einzelobjekt.gem_bfs AND einzelobjekte_punktelement.los = einzelobjekte_einzelobjekt.los AND einzelobjekte_punktelement.lieferdatum = einzelobjekte_einzelobjekt.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_eo_punkt
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_eo_punkt TO $$USER;');
;

INSERT INTO "views" VALUES(129,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_gs_ls AS 
 SELECT DISTINCT liegenschaften_grundstueck.ogc_fid, liegenschaften_liegenschaft.tid, liegenschaften_grundstueck.nummer, liegenschaften_liegenschaft.geometrie, liegenschaften_grundstueck.entstehung
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_liegenschaft
  WHERE liegenschaften_liegenschaft.liegenschaft_von::text = liegenschaften_grundstueck.tid::text AND liegenschaften_liegenschaft.lieferdatum = liegenschaften_grundstueck.lieferdatum AND liegenschaften_liegenschaft.los = liegenschaften_grundstueck.los AND liegenschaften_liegenschaft.gem_bfs = liegenschaften_grundstueck.gem_bfs;

ALTER TABLE $$DBSCHEMA.z_gs_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_gs_ls TO $$USER;');


INSERT INTO "views" VALUES(130,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_gs_nr AS 
 SELECT liegenschaften_grundstueckpos.pos, liegenschaften_grundstueck.nummer, liegenschaften_grundstueck.lieferdatum, liegenschaften_grundstueck.los, liegenschaften_grundstueck.gem_bfs, liegenschaften_grundstueck.gesamteflaechenmass, liegenschaften_grundstueck.art_txt, liegenschaften_grundstueck.art, liegenschaften_grundstueck.vollstaendigkeit_txt, liegenschaften_grundstueck.vollstaendigkeit, liegenschaften_grundstueck.gueltigkeit_txt, liegenschaften_grundstueck.gueltigkeit, liegenschaften_grundstueck.egris_egrid, liegenschaften_grundstueckpos.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_grundstueckpos
  WHERE liegenschaften_grundstueck.tid::text = liegenschaften_grundstueckpos.grundstueckpos_von::text AND liegenschaften_grundstueck.gem_bfs = liegenschaften_grundstueckpos.gem_bfs AND liegenschaften_grundstueck.los = liegenschaften_grundstueckpos.los AND liegenschaften_grundstueck.lieferdatum = liegenschaften_grundstueckpos.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_gs_nr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_gs_nr TO $$USER;');


INSERT INTO "views" VALUES(131,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_hgp_linie AS 
 SELECT gemeindegrenzen_hoheitsgrenzpunkt.ogc_fid, gemeindegrenzen_hoheitsgrenzpunkt.entstehung, gemeindegrenzen_hoheitsgrenzpunkt.identifikator, gemeindegrenzen_hoheitsgrenzpunkt.geometrie, gemeindegrenzen_hoheitsgrenzpunkt.lagegen, gemeindegrenzen_hoheitsgrenzpunkt.lagezuv, gemeindegrenzen_hoheitsgrenzpunkt.lagezuv_txt, gemeindegrenzen_hoheitsgrenzpunkt.punktzeichen, gemeindegrenzen_hoheitsgrenzpunkt.punktzeichen_txt, gemeindegrenzen_hoheitsgrenzpunkt.hoheitsgrenzstein, gemeindegrenzen_hoheitsgrenzpunkt.hoheitsgrenzstein_txt, gemeindegrenzen_hoheitsgrenzpunkt.exaktdefiniert, gemeindegrenzen_hoheitsgrenzpunkt.exaktdefiniert_txt, gemeindegrenzen_hoheitsgrenzpunkt.gem_bfs, gemeindegrenzen_hoheitsgrenzpunkt.los, gemeindegrenzen_hoheitsgrenzpunkt.lieferdatum, gemeindegrenzen_hoheitsgrenzpunktpos.pos
   FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze, $$DBSCHEMA.gemeindegrenzen_hoheitsgrenzpunkt, $$DBSCHEMA.gemeindegrenzen_hoheitsgrenzpunktpos
  WHERE gemeindegrenzen_gemeindegrenze.gem_bfs = gemeindegrenzen_hoheitsgrenzpunkt.gem_bfs AND gemeindegrenzen_gemeindegrenze.los = gemeindegrenzen_hoheitsgrenzpunkt.los AND gemeindegrenzen_gemeindegrenze.lieferdatum = gemeindegrenzen_hoheitsgrenzpunkt.lieferdatum AND gemeindegrenzen_hoheitsgrenzpunktpos.hoheitsgrenzpunktpos_von::text = gemeindegrenzen_hoheitsgrenzpunkt.tid::text AND st_touches(gemeindegrenzen_gemeindegrenze.geometrie, gemeindegrenzen_hoheitsgrenzpunktpos.pos) IS FALSE;

ALTER TABLE $$DBSCHEMA.z_hgp_linie
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_hgp_linie TO $$USER;');


INSERT INTO "views" VALUES(132,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_lineatt_ls AS 
 SELECT liegenschaften_liegenschaft.tid, liegenschaften_lineattrib1.ogc_fid, liegenschaften_liegenschaft.geometrie, liegenschaften_liegenschaft.gem_bfs, liegenschaften_liegenschaft.los, liegenschaften_liegenschaft.lieferdatum, liegenschaften_liegenschaft.qualitaet, liegenschaften_liegenschaft.flaechenmass, liegenschaften_liegenschaft.liegenschaft_von, liegenschaften_liegenschaft.nummerteilgrundstueck, liegenschaften_liegenschaft.qualitaet_txt, liegenschaften_lineattrib1.linienart, liegenschaften_lineattrib1.linienart_txt
   FROM $$DBSCHEMA.liegenschaften_liegenschaft, $$DBSCHEMA.liegenschaften_lineattrib1
  WHERE liegenschaften_liegenschaft.gem_bfs = liegenschaften_lineattrib1.gem_bfs AND liegenschaften_liegenschaft.los = liegenschaften_lineattrib1.los AND liegenschaften_liegenschaft.lieferdatum = liegenschaften_lineattrib1.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_lineatt_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_lineatt_ls TO $$USER;');


INSERT INTO "views" VALUES(133,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_lineatt_sdr AS 
 SELECT liegenschaften_selbstrecht.lieferdatum, liegenschaften_selbstrecht.los, liegenschaften_selbstrecht.gem_bfs, liegenschaften_selbstrecht.qualitaet_txt, liegenschaften_selbstrecht.qualitaet, liegenschaften_selbstrecht.flaechenmass, liegenschaften_selbstrecht.geometrie, liegenschaften_selbstrecht.nummerteilgrundstueck, liegenschaften_selbstrecht.selbstrecht_von, liegenschaften_selbstrecht.tid, liegenschaften_selbstrecht.ogc_fid, liegenschaften_lineattrib2.linienart, liegenschaften_lineattrib2.linienart_txt
   FROM $$DBSCHEMA.liegenschaften_selbstrecht, $$DBSCHEMA.liegenschaften_lineattrib2
  WHERE liegenschaften_selbstrecht.tid::text = liegenschaften_lineattrib2.tid::text AND liegenschaften_selbstrecht.gem_bfs = liegenschaften_lineattrib2.gem_bfs AND liegenschaften_selbstrecht.los = liegenschaften_lineattrib2.los AND liegenschaften_selbstrecht.lieferdatum = liegenschaften_lineattrib2.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_lineatt_sdr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_lineatt_sdr TO $$USER;');


INSERT INTO "views" VALUES(134,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_nr_ls AS 
 SELECT liegenschaften_grundstueckpos.pos, liegenschaften_grundstueck.nummer, liegenschaften_grundstueck.lieferdatum, liegenschaften_grundstueck.los, liegenschaften_grundstueck.gem_bfs, liegenschaften_grundstueck.gesamteflaechenmass, liegenschaften_grundstueck.art_txt, liegenschaften_grundstueck.art, liegenschaften_grundstueck.vollstaendigkeit_txt, liegenschaften_grundstueck.vollstaendigkeit, liegenschaften_grundstueck.gueltigkeit_txt, liegenschaften_grundstueck.gueltigkeit, liegenschaften_grundstueck.egris_egrid, liegenschaften_grundstueckpos.ogc_fid, liegenschaften_liegenschaft.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_grundstueckpos, $$DBSCHEMA.liegenschaften_liegenschaft
  WHERE liegenschaften_liegenschaft.liegenschaft_von::text = liegenschaften_grundstueck.tid::text AND liegenschaften_grundstueck.tid::text = liegenschaften_grundstueckpos.grundstueckpos_von::text AND liegenschaften_grundstueck.gem_bfs = liegenschaften_grundstueckpos.gem_bfs AND liegenschaften_grundstueck.los = liegenschaften_grundstueckpos.los AND liegenschaften_grundstueck.lieferdatum = liegenschaften_grundstueckpos.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_nr_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_nr_ls TO $$USER;');


INSERT INTO "views" VALUES(135,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_nr_sdr AS 
 SELECT liegenschaften_grundstueckpos.pos, liegenschaften_grundstueck.nummer, liegenschaften_grundstueck.lieferdatum, liegenschaften_grundstueck.los, liegenschaften_grundstueck.gem_bfs, liegenschaften_grundstueck.gesamteflaechenmass, liegenschaften_grundstueck.art_txt, liegenschaften_grundstueck.art, liegenschaften_grundstueck.vollstaendigkeit_txt, liegenschaften_grundstueck.vollstaendigkeit, liegenschaften_grundstueck.gueltigkeit_txt, liegenschaften_grundstueck.gueltigkeit, liegenschaften_grundstueck.egris_egrid, liegenschaften_grundstueckpos.ogc_fid, liegenschaften_selbstrecht.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_grundstueckpos, $$DBSCHEMA.liegenschaften_selbstrecht
  WHERE liegenschaften_selbstrecht.selbstrecht_von::text = liegenschaften_grundstueck.tid::text AND liegenschaften_grundstueck.tid::text = liegenschaften_grundstueckpos.grundstueckpos_von::text AND liegenschaften_grundstueck.gem_bfs = liegenschaften_grundstueckpos.gem_bfs AND liegenschaften_grundstueck.los = liegenschaften_grundstueckpos.los AND liegenschaften_grundstueck.lieferdatum = liegenschaften_grundstueckpos.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_nr_sdr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_nr_sdr TO $$USER;');

INSERT INTO "views" VALUES(136,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_ortschaftsnamen_geom AS 
 SELECT plzortschaft_ortschaftsname.text, plzortschaft_ortschaftsname.kurztext, plzortschaft_ortschaftsname.indextext, plzortschaft_ortschaftsname.sprache_txt, plzortschaft_ortschaftsname.sprache, plzortschaft_ortschaft.status, plzortschaft_ortschaft.status_txt, plzortschaft_ortschaft.ogc_fid, plzortschaft_ortschaft.inaenderung_txt, plzortschaft_ortschaft.inaenderung, plzortschaft_ortschaft.flaeche, plzortschaft_ortschaft.gem_bfs, plzortschaft_ortschaft.los, plzortschaft_ortschaft.lieferdatum
   FROM $$DBSCHEMA.plzortschaft_ortschaft, $$DBSCHEMA.plzortschaft_ortschaftsname
  WHERE plzortschaft_ortschaft.lieferdatum = plzortschaft_ortschaftsname.lieferdatum AND plzortschaft_ortschaft.los = plzortschaft_ortschaftsname.los AND plzortschaft_ortschaft.gem_bfs = plzortschaft_ortschaftsname.gem_bfs AND plzortschaft_ortschaftsname.ortschaftsname_von::text = plzortschaft_ortschaft.tid::text;

ALTER TABLE $$DBSCHEMA.z_ortschaftsnamen_geom
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_ortschaftsnamen_geom TO $$USER;');


INSERT INTO "views" VALUES(137,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_projgs_nr AS 
 SELECT liegenschaften_projgrundstueckpos.pos, liegenschaften_projgrundstueck.nummer, liegenschaften_projgrundstueck.lieferdatum, liegenschaften_projgrundstueck.los, liegenschaften_projgrundstueck.gem_bfs, liegenschaften_projgrundstueck.gesamteflaechenmass, liegenschaften_projgrundstueck.art_txt, liegenschaften_projgrundstueck.art, liegenschaften_projgrundstueck.vollstaendigkeit_txt, liegenschaften_projgrundstueck.vollstaendigkeit, liegenschaften_projgrundstueck.gueltigkeit_txt, liegenschaften_projgrundstueck.gueltigkeit, liegenschaften_projgrundstueck.egris_egrid, liegenschaften_projgrundstueckpos.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_projgrundstueck, $$DBSCHEMA.liegenschaften_projgrundstueckpos
  WHERE liegenschaften_projgrundstueck.tid::text = liegenschaften_projgrundstueckpos.projgrundstueckpos_von::text AND liegenschaften_projgrundstueck.gem_bfs = liegenschaften_projgrundstueckpos.gem_bfs AND liegenschaften_projgrundstueck.los = liegenschaften_projgrundstueckpos.los AND liegenschaften_projgrundstueck.lieferdatum = liegenschaften_projgrundstueckpos.lieferdatum;

ALTER TABLE $$DBSCHEMA.z_projgs_nr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_projgs_nr TO $$USER;');

CREATE TABLE updates
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);
COMMIT;
