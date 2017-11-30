BEGIN TRANSACTION;
CREATE TABLE "postprocessing" (
	ogc_fid	INTEGER NOT NULL,
	sql_query	TEXT,
	`order`	INTEGER,
	comment	TEXT,
	lang	TEXT,
	apply INTEGER DEFAULT 1,
	PRIMARY KEY(ogc_fid)
);
INSERT INTO `postprocessing` (ogc_fid,sql_query,order,comment,lang,apply) VALUES (1,'CREATE TYPE $$DBSCHEMA.maengel_topic AS ENUM
(
 ''Bodenbedeckung'',
 ''Einzelobjekte''
 );',1,'German enum type for t_maengel_topic.','de',1),
 (2,'CREATE TYPE $$DBSCHEMA.maengel_topic AS ENUM
(''Couverture_du_sol'',
 ''Objets_divers''
 );',1,'French enum type for t_maengel_topic','fr',1),
 (3,'CREATE TABLE $$DBSCHEMA.t_maengel_topics
(
 ogc_fid serial NOT NULL,
 topic_name varchar NOT NULL,
 topic_name_fr  varchar NOT NULL,
 CONSTRAINT t_maengel_topics_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_topics TO $$USER;',1,'Was in table tables',NULL,1),
 (4,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz
(
 ogc_fid serial NOT NULL,
 tid character varying,
 line geometry(LINESTRING,$$EPSG),
 hausnummer character varying,
 CONSTRAINT t_gebaeudeadressen_spinnennetz_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz TO $$USER;',1,'Was in table tables',NULL,1),
 (5,'CREATE TABLE $$DBSCHEMA.t_shortestline_hausnummerpos
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
GRANT SELECT ON TABLE $$DBSCHEMA.t_shortestline_hausnummerpos TO $$USER;',1,'Was in table tables',NULL,1),
 (6,'CREATE TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang
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
  OIDS=FALSE
);

GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang TO $$USER;',1,'Was in table tables',NULL,1),
 (7,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_ausserhalb
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
  OIDS=FALSE
);

GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_ausserhalb TO $$USER;',1,'Was in table tables',NULL,1),
 (8,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_innerhalb_centroidbuffer
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
  OIDS=FALSE
);

GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_innerhalb_centroidbuffer TO $$USER;',1,'Was in table tables',NULL,1),
 (9,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_ausserhalb
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
WITH (
  OIDS=FALSE
);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_ausserhalb TO $$USER;',1,'Was in table tables',NULL,1),
 (10,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_doppelt
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
WITH (
  OIDS=FALSE
);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_doppelt TO $$USER;',1,'Was in table tables',NULL,1),
 (11,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos
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
WITH (
  OIDS=FALSE
);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos TO $$USER;',1,'Was in table tables',NULL,1),
 (12,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok
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
  OIDS=FALSE
);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok TO $$USER;
',1,'Was in table tables',NULL,1),
 (13,'CREATE TABLE $$DBSCHEMA.z_v_bb_ts
(
  OGC_FID serial NOT NULL,
  geometrie geometry(MultiPolygon,$$EPSG),
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
GRANT ALL ON TABLE $$DBSCHEMA.z_v_bb_ts TO $$USER;',1,'Was in table tables',NULL,1),
 (14,'CREATE TABLE $$DBSCHEMA.z_v_ls_nk
(
  ogc_fid serial NOT NULL,
  ls_fid integer,
  nk_fid integer,
  geometrie geometry(MultiPolygon,$$EPSG),
  flaeche double precision,
  CONSTRAINT z_v_ls_nk_pkey PRIMARY KEY (ogc_fid )
)
WITH (OIDS=TRUE);
ALTER TABLE $$DBSCHEMA.z_v_ls_nk OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_ls_nk TO $$USER;',1,'Was in table tables',NULL,1),
 (15,'CREATE TABLE $$DBSCHEMA.z_v_bb_ls
(
  ogc_fid serial NOT NULL,
  bb_ogc_fid integer,
  bb_qualitaet integer,
  bb_qualitaet_txt character varying,
  art integer,
  art_txt character varying,
  ls_ogc_fid serial NOT NULL,
  liegenschaft_von character varying,
  nummerteilgrundstueck character varying,
  flaechenmass double precision,
  geometrie geometry(MultiPolygon,$$EPSG),
  flaeche double precision,
  ls_flaeche double precision,
  CONSTRAINT z_v_bb_ls_pkey PRIMARY KEY (ogc_fid )
)
WITH (OIDS=TRUE);
ALTER TABLE $$DBSCHEMA.z_v_bb_ls OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_bb_ls TO $$USER;',1,'Was in table tables',NULL,1),
 (16,'CREATE TABLE $$DBSCHEMA.z_ls_entstehung
(
  ogc_fid serial NOT NULL,
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
GRANT ALL ON TABLE $$DBSCHEMA.z_ls_entstehung TO $$USER;',1,'Was in table tables',NULL,1),
 (17,'CREATE TABLE $$DBSCHEMA.z_grenzen
(
  ogc_fid serial NOT NULL,
  geometrie geometry(Point,$$EPSG),
  CONSTRAINT z_grenzen_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE $$DBSCHEMA.z_grenzen
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_grenzen TO $$USER;',1,'Was in table tables',NULL,1),
 (18,'CREATE TABLE $$DBSCHEMA.z_v_gp_ts
(
  ogc_fid serial NOT NULL,
  tid character varying,
  entstehung character varying,
  identifikator character varying,
  geometrie geometry(Point,$$EPSG),
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
GRANT ALL ON TABLE $$DBSCHEMA.z_v_gp_ts TO $$USER;',1,'Was in table tables',NULL,1),
 (19,'CREATE TABLE $$DBSCHEMA.z_liegenschaft_flaeche
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
GRANT ALL ON TABLE $$DBSCHEMA.z_liegenschaft_flaeche TO $$USER;',1,'Was in table tables',NULL,1),
 (20,'CREATE TABLE $$DBSCHEMA.z_selbstrecht_flaeche
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
GRANT ALL ON TABLE $$DBSCHEMA.z_selbstrecht_flaeche TO $$USER;',1,'Was in table tables',NULL,1),
 (21,'CREATE TABLE $$DBSCHEMA.z_hgp_ls_linie
(
  ogc_fid serial NOT NULL,
  geometrie geometry(Point,$$EPSG),
  CONSTRAINT z_hgp_ls_linie_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_hgp_ls_linie
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_hgp_ls_linie TO $$USER;',1,'Was in table tables',NULL,1),
 (22,'CREATE TABLE $$DBSCHEMA.z_nr_gs
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
  pos geometry(Point,$$EPSG),
  lin integer,
  CONSTRAINT liegenschaften_z_nr_gs_pkey PRIMARY KEY (ogc_fid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE $$DBSCHEMA.z_nr_gs
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_nr_gs TO $$USER;',1,'Was in table tables',NULL,1),
 (23,'CREATE TABLE $$DBSCHEMA.z_v_ls_nk_pkt
(
  z_ls_nk_pkt_fid serial NOT NULL,
  ls_fid integer,
  nk_fid integer,
  flaeche double precision,
  geometrie geometry(Point,$$EPSG),
  CONSTRAINT z_v_ls_nk_pkt_pkey PRIMARY KEY (z_ls_nk_pkt_fid )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE $$DBSCHEMA.z_v_ls_nk_pkt
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_v_ls_nk_pkt TO $$USER;',1,'Was in table tables',NULL,1),
 (24,'CREATE TABLE $$DBSCHEMA.z_gebaeudenummer_pos
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
GRANT ALL ON TABLE $$DBSCHEMA.z_gebaeudenummer_pos TO $$USER;',1,'Was in table tables',NULL,1),
 (25,'CREATE TABLE $$DBSCHEMA.z_objektnummer_pos
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
GRANT ALL ON TABLE $$DBSCHEMA.z_objektnummer_pos TO $$USER;',1,'Was in table tables',NULL,1),
 (26,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_lfp3_ausserhalb_gemeinde AS
 SELECT a.*
 FROM $$DBSCHEMA.fixpunktekatgrie3_lfp3 a,
 (
  SELECT (ST_Union(geometrie)) as geometrie
  FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze
 ) b
 WHERE ST_Distance(a.geometrie, b.geometrie) > 0;
GRANT SELECT ON TABLE $$DBSCHEMA.v_lfp3_ausserhalb_gemeinde TO $$USER;',2,'Was in table views',NULL,1),
 (27,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_flaechenelement AS
SELECT b.*, a.art, a.art_txt, a.t_ili_tid as eo_tid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_flaechenelement as b
WHERE b.flaechenelement_von::text = a.ogc_fid::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_flaechenelement TO $$USER;',2,'Was in table views',NULL,1),
 (28,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_linienelement AS
SELECT b.*, a.art, a.art_txt, a.t_ili_tid as eo_tid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_linienelement as b
WHERE b.linienelement_von::text = a.ogc_fid::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_linienelement TO $$USER;',2,'Was in table views',NULL,1),
 (29,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_punktelement AS
SELECT b.*, a.art, a.art_txt, a.t_ili_tid as eo_tid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_punktelement as b
WHERE b.punktelement_von::text = a.ogc_fid::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_punktelement TO $$USER;',2,'Was in table views',NULL,1),
 (30,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos AS
SELECT b.ogc_fid, b.t_ili_tid, b.hausnummerpos_von::text, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, ST_X(b.pos) AS y, ST_Y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.hausnummer, a.gebaeudeeingang_von::text as lok_tid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, $$DBSCHEMA.gebaeudeadressen_hausnummerpos b
WHERE a.ogc_fid::text::text = b.hausnummerpos_von::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos TO $$USER;',2,'Was in table views',NULL,1),
 (31,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos AS
 SELECT b.ogc_fid, b.t_ili_tid, b.lokalisationsnamepos_von::text, b.anfindex, b.endindex, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, b.hilfslinie, ST_X(b.pos) AS y, ST_Y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.benannte, a.atext
FROM $$DBSCHEMA.gebaeudeadressen_lokalisationsname a, $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos b
WHERE a.ogc_fid::text::text = b.lokalisationsnamepos_von::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos TO $$USER;',2,'Was in table views',NULL,1),
 (32,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_distanz_gebaeudeeingang_lokalisationsnamepos AS
SELECT a.t_ili_tid AS atid, b.t_ili_tid AS btid, min(ST_Length(ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(b.pos)::text) || '' ''::text) || ST_Y(b.pos)::text) || '')''::text, $$EPSG))) AS min
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, $$DBSCHEMA.v_gebaeudeadressen_lokalisationsnamepos b
WHERE a.gebaeudeeingang_von::text = b.benannte::text
GROUP BY a.t_ili_tid, b.t_ili_tid
ORDER BY a.t_ili_tid, min(ST_Length(ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(b.pos)::text) || '' ''::text) || ST_Y(b.pos)::text) || '')''::text, $$EPSG)));

GRANT SELECT ON TABLE $$DBSCHEMA.v_distanz_gebaeudeeingang_lokalisationsnamepos TO $$USER;',2,'Was in table views',NULL,1),
 (33,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_lokalisationsname_ohne_gebaeudeeingaenge AS

SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nummerierungsprinzip, a.nummerierungsprinzip_txt,
       a.lokalisationnummer, a.attributeprovisorisch, a.attributeprovisorisch_txt,
       a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.status, a.status_txt,
       a.inaenderung, a.inaenderung_txt, a.art, a.art_txt, b.atext
FROM
(
  SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nummerierungsprinzip, a.nummerierungsprinzip_txt,
         a.lokalisationnummer, a.attributeprovisorisch, a.attributeprovisorisch_txt,
         a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.status, a.status_txt,
         a.inaenderung, a.inaenderung_txt, a.art, a.art_txt
  FROM $$DBSCHEMA.gebaeudeadressen_lokalisation a
  LEFT JOIN
  (
    SELECT DISTINCT ON (gebaeudeadressen_gebaeudeeingang.gebaeudeeingang_von::text)
           gebaeudeadressen_gebaeudeeingang.ogc_fid, gebaeudeadressen_gebaeudeeingang.t_ili_tid,
           gebaeudeadressen_gebaeudeeingang.entstehung, gebaeudeadressen_gebaeudeeingang.gebaeudeeingang_von::text,
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
  ) b ON a.t_ili_tid::text = b.gebaeudeeingang_von::text
  WHERE b.gebaeudeeingang_von::text IS NULL
) a,
$$DBSCHEMA.gebaeudeadressen_lokalisationsname b
WHERE a.t_ili_tid::text = b.benannte::text;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_lokalisationsname_ohne_gebaeudeeingaenge TO $$USER;',2,'Was in table views',NULL,1),
 (34,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_ohne_nummer_attribute AS
SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.gebaeudeeingang_von::text, a.status, a.status_txt,
       a.inaenderung, a.inaenderung_txt, a.attributeprovisorisch, a.attributeprovisorisch_txt,
       a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.lage, a.hoehenlage,
       a.hausnummer, a.im_gebaeude, a.im_gebaeude_txt, a.gwr_egid, a.gwr_edid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a
WHERE a.gebaeudeeingang_von::text IS NOT NULL
AND a.hausnummer IS NULL
AND (a.status <> 1 OR a.inaenderung <> 1 OR a.attributeprovisorisch <> 1 OR a.istoffiziellebezeichnung <> 1);

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_ohne_nummer_attribute TO $$USER;',2,'Was in table views',NULL,1),
 (35,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_mit_nummer_attribute AS
SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.gebaeudeeingang_von::text, a.status, a.status_txt,
       a.inaenderung, a.inaenderung_txt, a.attributeprovisorisch, a.attributeprovisorisch_txt,
       a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.lage, a.hoehenlage,
       a.hausnummer, a.im_gebaeude, a.im_gebaeude_txt, a.gwr_egid, a.gwr_edid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a
WHERE a.gebaeudeeingang_von::text IS NOT NULL
AND a.hausnummer IS NOT NULL
AND (a.status <> 1 OR a.inaenderung <> 1 OR a.attributeprovisorisch <> 1 OR a.istoffiziellebezeichnung <> 0);

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_gebaeudeeingang_mit_nummer_attribute TO $$USER;',2,'Was in table views',NULL,1),
 (36,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos_ohne_nummer AS
SELECT a.ogc_fid, a.t_ili_tid, a.hausnummerpos_von::text, a.pos, a.ori, a.hali, a.hali_txt,
       a.vali, a.vali_txt, a.groesse, a.groesse_txt
FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos a, $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang b
WHERE a.hausnummerpos_von::text = b.ogc_fid::text
AND b.hausnummer IS NULL;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos_ohne_nummer TO $$USER;',2,'Was in table views',NULL,1),
 (37,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_flaechenelement_v AS
 SELECT b.ogc_fid, b.t_ili_tid, b.flaechenelement_von::text, b.geometrie,a.art, a.art_txt, a.qualitaet_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt a, $$DBSCHEMA.einzelobjekte_flaechenelement b
  WHERE b.flaechenelement_von::text = a.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_flaechenelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_flaechenelement_v TO $$USER;',2,'Was in table views',NULL,1),
 (38,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_linienelement_v AS
 SELECT b.ogc_fid, b.t_ili_tid, b.linienelement_von::text, b.geometrie, a.art, a.art_txt, a.qualitaet_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt a, $$DBSCHEMA.einzelobjekte_linienelement b
  WHERE b.linienelement_von::text = a.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_linienelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_linienelement_v TO $$USER;',2,'Was in table views',NULL,1),
 (39,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_objektnamepos_v AS
 SELECT einzelobjekte_objektname.aname, einzelobjekte_objektnamepos.pos, einzelobjekte_objektnamepos.ogc_fid
   FROM $$DBSCHEMA.einzelobjekte_objektname, $$DBSCHEMA.einzelobjekte_objektnamepos
  WHERE einzelobjekte_objektname.ogc_fid::text = einzelobjekte_objektnamepos.objektnamepos_von::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_objektnamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_objektnamepos_v TO $$USER;',2,'Was in table views',NULL,1),
 (40,'CREATE OR REPLACE VIEW $$DBSCHEMA.einzelobjekte_punktelement_v AS
 SELECT b.ogc_fid, b.t_ili_tid, b.punktelement_von::text, b.geometrie, a.art, a.art_txt, a.qualitaet_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt a, $$DBSCHEMA.einzelobjekte_punktelement b
  WHERE b.punktelement_von::text = a.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.einzelobjekte_punktelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.einzelobjekte_punktelement_v TO $$USER;',2,'Was in table views',NULL,1),
 (41,'CREATE OR REPLACE VIEW $$DBSCHEMA.fixpunktekatgrie3_lfp3_ausserhalb_perimeter_v AS
 SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.geometrie, a.hoehegeom, a.lagegen, a.lagezuv, a.lagezuv_txt, a.hoehegen, a.hoehezuv, a.hoehezuv_txt, a.punktzeichen, a.punktzeichen_txt, a.protokoll, a.protokoll_txt, st_distance(a.geometrie, b.geometrie) AS distance
   FROM $$DBSCHEMA.fixpunktekatgrie3_lfp3 a, ( SELECT st_multi(st_union(tseinteilung_toleranzstufe.geometrie)) AS geometrie
           FROM $$DBSCHEMA.tseinteilung_toleranzstufe) b
  WHERE st_distance(a.geometrie, b.geometrie) > 0::double precision;

ALTER TABLE $$DBSCHEMA.fixpunktekatgrie3_lfp3_ausserhalb_perimeter_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.fixpunktekatgrie3_lfp3_ausserhalb_perimeter_v TO $$USER;
',2,'Was in table views',NULL,1),
 (42,'CREATE OR REPLACE VIEW $$DBSCHEMA.fixpunktekatgrie3_lfp3_pro_toleranzstufe_v AS
 SELECT a.ogc_fid, a.art + 1 AS toleranzstufe, round((st_area(a.geometrie) / 10000::double precision)::numeric, 2) AS ts_hektare, count(b.t_ili_tid) AS ist,
        CASE
            WHEN a.art = 0 THEN round(150::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 1 THEN round(70::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 2 THEN round(20::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 3 THEN round(10::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 4 THEN round(2::double precision * st_area(a.geometrie) / 1000000::double precision)
            ELSE NULL::double precision
        END AS soll,
        CASE
            WHEN a.art = 0 THEN count(b.t_ili_tid)::double precision - round(150::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 1 THEN count(b.t_ili_tid)::double precision - round(70::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 2 THEN count(b.t_ili_tid)::double precision - round(20::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 3 THEN count(b.t_ili_tid)::double precision - round(10::double precision * st_area(a.geometrie) / 1000000::double precision)
            WHEN a.art = 4 THEN count(b.t_ili_tid)::double precision - round(2::double precision * st_area(a.geometrie) / 1000000::double precision)
            ELSE NULL::double precision
        END AS diff
   FROM $$DBSCHEMA.tseinteilung_toleranzstufe a, $$DBSCHEMA.fixpunktekatgrie3_lfp3 b
  WHERE st_distance(a.geometrie, b.geometrie) = 0::double precision
  GROUP BY a.art, a.geometrie, a.ogc_fid
  ORDER BY a.art;

ALTER TABLE $$DBSCHEMA.fixpunktekatgrie3_lfp3_pro_toleranzstufe_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.fixpunktekatgrie3_lfp3_pro_toleranzstufe_v TO $$USER;',2,'Was in table views',NULL,1),
 (43,'CREATE OR REPLACE VIEW $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v AS
 SELECT b.ogc_fid, b.t_ili_tid, b.lokalisationsnamepos_von::text, b.anfindex, b.endindex, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, b.hilfslinie, st_x(b.pos) AS y, st_y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS ori_neu, a.benannte, a.atext
   FROM $$DBSCHEMA.gebaeudeadressen_lokalisationsname a, $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos b
  WHERE a.ogc_fid::text = b.lokalisationsnamepos_von::text;

ALTER TABLE $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos_v TO $$USER;',2,'Was in table views',NULL,1),
 (44,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_liegenschaft_v AS
 SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_liegenschaft b
  WHERE a.ogc_fid::text = b.liegenschaft_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v TO $$USER;',2,'Was in table views',NULL,1),
 (45,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_liegenschaft_v2 AS
 SELECT b.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_liegenschaft b
  WHERE a.ogc_fid::text = b.liegenschaft_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v2
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_liegenschaft_v2 TO $$USER;',2,'Was in table views',NULL,1),
 (46,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_projliegenschaft_v AS
 SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass,b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_projliegenschaft b
  WHERE a.ogc_fid::text = b.projliegenschaft_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_projliegenschaft_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_projliegenschaft_v TO $$USER;',2,'Was in table views',NULL,1),
 (47,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_projselbstrecht_v AS
 SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_projselbstrecht b
  WHERE a.ogc_fid::text = b.projselbstrecht_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_projselbstrecht_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_projselbstrecht_v TO $$USER;',2,'Was in table views',NULL,1),
 (48,'CREATE OR REPLACE VIEW $$DBSCHEMA.liegenschaften_selbstrecht_v AS
 SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.egris_egrid, a.gueltigkeit, a.gueltigkeit_txt, a.vollstaendigkeit, a.vollstaendigkeit_txt, a.art, a.art_txt, a.gesamteflaechenmass, b.geometrie, b.flaechenmass, b.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck a, $$DBSCHEMA.liegenschaften_selbstrecht b
  WHERE a.ogc_fid::text = b.selbstrecht_von::text;

ALTER TABLE $$DBSCHEMA.liegenschaften_selbstrecht_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.liegenschaften_selbstrecht_v TO $$USER;',2,'Was in table views',NULL,1),
 (49,'CREATE OR REPLACE VIEW $$DBSCHEMA.nomenklatur_gelaendenamepos_v AS
 SELECT b.ogc_fid, b.t_ili_tid, b.gelaendenamepos_von::text, b.pos, b.ori, b.hali, b.hali_txt, b.vali, b.vali_txt, b.groesse, b.groesse_txt, b.stil, b.stil_txt,st_x(b.pos) AS y, st_y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.aname
   FROM $$DBSCHEMA.nomenklatur_gelaendename a, $$DBSCHEMA.nomenklatur_gelaendenamepos b
  WHERE a.ogc_fid::text = b.gelaendenamepos_von::text;

ALTER TABLE $$DBSCHEMA.nomenklatur_gelaendenamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.nomenklatur_gelaendenamepos_v TO $$USER;',2,'Was in table views',NULL,1),
 (50,'CREATE OR REPLACE VIEW $$DBSCHEMA.planeinteilungen_plan_v AS
 SELECT a.ogc_fid, a.t_ili_tid, a.nbident, a.nummer, a.techdossier, a.gueltigereintrag,  b.geometrie
   FROM $$DBSCHEMA.planeinteilungen_plan a, $$DBSCHEMA.planeinteilungen_plangeometrie b
  WHERE a.ogc_fid::text = b.plangeometrie_von::text;

ALTER TABLE $$DBSCHEMA.planeinteilungen_plan_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.planeinteilungen_plan_v TO $$USER;',2,'Was in table views',NULL,1),
 (51,'CREATE OR REPLACE VIEW $$DBSCHEMA.rohrleitungen_leitungsobjekt_v AS
 SELECT rohrleitungen_leitungsobjekt.qualitaet_txt, rohrleitungen_leitungsobjekt.betreiber, rohrleitungen_leitungsobjekt.t_ili_tid, rohrleitungen_leitungsobjekt.art_txt, rohrleitungen_leitungsobjektpos.ogc_fid, rohrleitungen_leitungsobjektpos.pos, rohrleitungen_leitungsobjektpos.leitungsobjektpos_von::text
   FROM $$DBSCHEMA.rohrleitungen_leitungsobjekt, $$DBSCHEMA.rohrleitungen_leitungsobjektpos
  WHERE rohrleitungen_leitungsobjekt.ogc_fid::text = rohrleitungen_leitungsobjektpos.leitungsobjektpos_von::text;

ALTER TABLE $$DBSCHEMA.rohrleitungen_leitungsobjekt_v OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.rohrleitungen_leitungsobjekt_v TO $$USER;',2,'Was in table views',NULL,1),
 (52,'CREATE OR REPLACE VIEW $$DBSCHEMA.rohrleitungen_linienelement_v AS
 SELECT b.ogc_fid, b.t_ili_tid, b.linienelement_von::text, b.geometrie, b.linienart, b.linienart_txt, a.betreiber, a.qualitaet, a.qualitaet_txt, a.art, a.art_txt
   FROM $$DBSCHEMA.rohrleitungen_leitungsobjekt a, $$DBSCHEMA.rohrleitungen_linienelement b
  WHERE a.ogc_fid::text = b.linienelement_von::text;

ALTER TABLE $$DBSCHEMA.rohrleitungen_linienelement_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.rohrleitungen_linienelement_v TO $$USER;',2,'Was in table views',NULL,1),
 (53,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_ls AS
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_liegenschaft ls
  WHERE st_touches(b.geometrie, ls.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_ls TO $$USER;',2,'Was in table views',NULL,1),
 (54,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_projls AS
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projliegenschaft
  WHERE st_touches(b.geometrie, liegenschaften_projliegenschaft.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_projls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_projls TO $$USER;',2,'Was in table views',NULL,1),
 (55,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_projsdr AS
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projselbstrecht
  WHERE st_touches(b.geometrie, liegenschaften_projselbstrecht.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_projsdr OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_projsdr TO $$USER;',2,'Was in table views',NULL,1),
 (56,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp_sdr AS
 SELECT DISTINCT b.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_selbstrecht
  WHERE st_touches(b.geometrie, liegenschaften_selbstrecht.geometrie) IS TRUE;

ALTER TABLE $$DBSCHEMA.test_gp_sdr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.test_gp_sdr TO $$USER;',2,'Was in table views',NULL,1),
 (57,'CREATE OR REPLACE VIEW $$DBSCHEMA."z_Geb_Strassen_Ortschaft" AS
 SELECT gebaeudeadressen_strassenstueck.geometrie, gebaeudeadressen_strassenstueck.ogc_fid
   FROM $$DBSCHEMA.plzortschaft_ortschaft, $$DBSCHEMA.gebaeudeadressen_strassenstueck
  WHERE st_touches(gebaeudeadressen_strassenstueck.geometrie, plzortschaft_ortschaft.flaeche) IS TRUE;

ALTER TABLE $$DBSCHEMA."z_Geb_Strassen_Ortschaft"
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA."z_Geb_Strassen_Ortschaft" TO $$USER;',2,'Was in table views',NULL,1),
 (58,'CREATE OR REPLACE VIEW $$DBSCHEMA."z_benGeb_Ortschaft" AS
 SELECT gebaeudeadressen_benanntesgebiet.ogc_fid, gebaeudeadressen_benanntesgebiet.flaeche
   FROM $$DBSCHEMA.gebaeudeadressen_benanntesgebiet, $$DBSCHEMA.plzortschaft_ortschaft
  WHERE st_touches(gebaeudeadressen_benanntesgebiet.flaeche, plzortschaft_ortschaft.flaeche) IS TRUE;

ALTER TABLE $$DBSCHEMA."z_benGeb_Ortschaft"
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA."z_benGeb_Ortschaft" TO $$USER;',2,'Was in table views',NULL,1),
 (59,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_eo_flaeche AS
 SELECT einzelobjekte_flaechenelement.ogc_fid AS ctid, einzelobjekte_flaechenelement.geometrie, einzelobjekte_einzelobjekt.t_ili_tid, einzelobjekte_einzelobjekt.entstehung, einzelobjekte_einzelobjekt.qualitaet, einzelobjekte_einzelobjekt.qualitaet_txt, einzelobjekte_einzelobjekt.art, einzelobjekte_einzelobjekt.art_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt, $$DBSCHEMA.einzelobjekte_flaechenelement
  WHERE einzelobjekte_flaechenelement.flaechenelement_von::text = einzelobjekte_einzelobjekt.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.z_eo_flaeche
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_eo_flaeche TO $$USER;',2,'Was in table views',NULL,1),
 (60,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_eo_linie AS
 SELECT einzelobjekte_einzelobjekt.entstehung, einzelobjekte_einzelobjekt.t_ili_tid, einzelobjekte_einzelobjekt.qualitaet, einzelobjekte_einzelobjekt.qualitaet_txt, einzelobjekte_einzelobjekt.art, einzelobjekte_einzelobjekt.art_txt, einzelobjekte_linienelement.geometrie, einzelobjekte_linienelement.ogc_fid AS ctid
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt, $$DBSCHEMA.einzelobjekte_linienelement
  WHERE einzelobjekte_linienelement.linienelement_von::text = einzelobjekte_einzelobjekt.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.z_eo_linie
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_eo_linie TO $$USER;',2,'Was in table views',NULL,1),
 (61,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_eo_punkt AS
 SELECT einzelobjekte_punktelement.ogc_fid AS ctid, einzelobjekte_punktelement.geometrie, einzelobjekte_einzelobjekt.t_ili_tid, einzelobjekte_einzelobjekt.entstehung, einzelobjekte_einzelobjekt.qualitaet, einzelobjekte_einzelobjekt.qualitaet_txt, einzelobjekte_einzelobjekt.art,einzelobjekte_einzelobjekt.art_txt
   FROM $$DBSCHEMA.einzelobjekte_einzelobjekt, $$DBSCHEMA.einzelobjekte_punktelement
  WHERE einzelobjekte_punktelement.punktelement_von::text = einzelobjekte_einzelobjekt.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.z_eo_punkt
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_eo_punkt TO $$USER;',2,'Was in table views',NULL,1),
 (62,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_gs_ls AS
 SELECT DISTINCT liegenschaften_grundstueck.ogc_fid, liegenschaften_liegenschaft.t_ili_tid, liegenschaften_grundstueck.nummer, liegenschaften_liegenschaft.geometrie, liegenschaften_grundstueck.entstehung
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_liegenschaft
  WHERE liegenschaften_liegenschaft.liegenschaft_von::text = liegenschaften_grundstueck.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.z_gs_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_gs_ls TO $$USER;',2,'Was in table views',NULL,1),
 (63,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_gs_nr AS
 SELECT liegenschaften_grundstueckpos.pos, liegenschaften_grundstueck.nummer, liegenschaften_grundstueck.gesamteflaechenmass, liegenschaften_grundstueck.art_txt, liegenschaften_grundstueck.art, liegenschaften_grundstueck.vollstaendigkeit_txt, liegenschaften_grundstueck.vollstaendigkeit, liegenschaften_grundstueck.gueltigkeit_txt, liegenschaften_grundstueck.gueltigkeit, liegenschaften_grundstueck.egris_egrid, liegenschaften_grundstueckpos.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_grundstueckpos
  WHERE liegenschaften_grundstueck.ogc_fid::text = liegenschaften_grundstueckpos.grundstueckpos_von::text;

ALTER TABLE $$DBSCHEMA.z_gs_nr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_gs_nr TO $$USER;',2,'Was in table views',NULL,1),
 (64,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_hgp_linie AS
 SELECT gemeindegrenzen_hoheitsgrenzpunkt.ogc_fid, gemeindegrenzen_hoheitsgrenzpunkt.entstehung, gemeindegrenzen_hoheitsgrenzpunkt.identifikator, gemeindegrenzen_hoheitsgrenzpunkt.geometrie, gemeindegrenzen_hoheitsgrenzpunkt.lagegen, gemeindegrenzen_hoheitsgrenzpunkt.lagezuv, gemeindegrenzen_hoheitsgrenzpunkt.lagezuv_txt, gemeindegrenzen_hoheitsgrenzpunkt.punktzeichen, gemeindegrenzen_hoheitsgrenzpunkt.punktzeichen_txt, gemeindegrenzen_hoheitsgrenzpunkt.hoheitsgrenzstein, gemeindegrenzen_hoheitsgrenzpunkt.hoheitsgrenzstein_txt, gemeindegrenzen_hoheitsgrenzpunkt.exaktdefiniert, gemeindegrenzen_hoheitsgrenzpunkt.exaktdefiniert_txt,gemeindegrenzen_hoheitsgrenzpunktpos.pos
   FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze, $$DBSCHEMA.gemeindegrenzen_hoheitsgrenzpunkt, $$DBSCHEMA.gemeindegrenzen_hoheitsgrenzpunktpos
  WHERE gemeindegrenzen_hoheitsgrenzpunktpos.hoheitsgrenzpunktpos_von::text = gemeindegrenzen_hoheitsgrenzpunkt.ogc_fid::text AND st_touches(gemeindegrenzen_gemeindegrenze.geometrie, gemeindegrenzen_hoheitsgrenzpunktpos.pos) IS FALSE;

ALTER TABLE $$DBSCHEMA.z_hgp_linie
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_hgp_linie TO $$USER;',2,'Was in table views',NULL,1),
 (65,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_nr_ls AS
 SELECT liegenschaften_grundstueckpos.pos, liegenschaften_grundstueck.nummer, liegenschaften_grundstueck.gesamteflaechenmass, liegenschaften_grundstueck.art_txt, liegenschaften_grundstueck.art, liegenschaften_grundstueck.vollstaendigkeit_txt, liegenschaften_grundstueck.vollstaendigkeit, liegenschaften_grundstueck.gueltigkeit_txt, liegenschaften_grundstueck.gueltigkeit, liegenschaften_grundstueck.egris_egrid, liegenschaften_grundstueckpos.ogc_fid, liegenschaften_liegenschaft.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_grundstueckpos, $$DBSCHEMA.liegenschaften_liegenschaft
  WHERE liegenschaften_liegenschaft.liegenschaft_von::text = liegenschaften_grundstueck.ogc_fid::text AND liegenschaften_grundstueck.ogc_fid::text = liegenschaften_grundstueckpos.grundstueckpos_von::text;

ALTER TABLE $$DBSCHEMA.z_nr_ls
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_nr_ls TO $$USER;',2,'Was in table views',NULL,1),
 (66,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_nr_sdr AS
 SELECT liegenschaften_grundstueckpos.pos, liegenschaften_grundstueck.nummer, liegenschaften_grundstueck.gesamteflaechenmass, liegenschaften_grundstueck.art_txt, liegenschaften_grundstueck.art, liegenschaften_grundstueck.vollstaendigkeit_txt, liegenschaften_grundstueck.vollstaendigkeit, liegenschaften_grundstueck.gueltigkeit_txt, liegenschaften_grundstueck.gueltigkeit, liegenschaften_grundstueck.egris_egrid, liegenschaften_grundstueckpos.ogc_fid, liegenschaften_selbstrecht.nummerteilgrundstueck
   FROM $$DBSCHEMA.liegenschaften_grundstueck, $$DBSCHEMA.liegenschaften_grundstueckpos, $$DBSCHEMA.liegenschaften_selbstrecht
  WHERE liegenschaften_selbstrecht.selbstrecht_von::text = liegenschaften_grundstueck.ogc_fid::text AND liegenschaften_grundstueck.ogc_fid::text = liegenschaften_grundstueckpos.grundstueckpos_von::text;

ALTER TABLE $$DBSCHEMA.z_nr_sdr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_nr_sdr TO $$USER;',2,'Was in table views',NULL,1),
 (67,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_ortschaftsnamen_geom AS
 SELECT plzortschaft_ortschaftsname.atext, plzortschaft_ortschaftsname.kurztext, plzortschaft_ortschaftsname.indextext, plzortschaft_ortschaftsname.sprache_txt, plzortschaft_ortschaftsname.sprache, plzortschaft_ortschaft.status, plzortschaft_ortschaft.status_txt, plzortschaft_ortschaft.ogc_fid, plzortschaft_ortschaft.inaenderung_txt, plzortschaft_ortschaft.inaenderung, plzortschaft_ortschaft.flaeche
   FROM $$DBSCHEMA.plzortschaft_ortschaft, $$DBSCHEMA.plzortschaft_ortschaftsname
  WHERE plzortschaft_ortschaftsname.ortschaftsname_von::text = plzortschaft_ortschaft.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.z_ortschaftsnamen_geom
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_ortschaftsnamen_geom TO $$USER;',2,'Was in table views',NULL,1),
 (68,'CREATE OR REPLACE VIEW $$DBSCHEMA.z_projgs_nr AS
 SELECT liegenschaften_projgrundstueckpos.pos, liegenschaften_projgrundstueck.nummer, liegenschaften_projgrundstueck.gesamteflaechenmass, liegenschaften_projgrundstueck.art_txt, liegenschaften_projgrundstueck.art, liegenschaften_projgrundstueck.vollstaendigkeit_txt, liegenschaften_projgrundstueck.vollstaendigkeit, liegenschaften_projgrundstueck.gueltigkeit_txt, liegenschaften_projgrundstueck.gueltigkeit, liegenschaften_projgrundstueck.egris_egrid, liegenschaften_projgrundstueckpos.ogc_fid
   FROM $$DBSCHEMA.liegenschaften_projgrundstueck, $$DBSCHEMA.liegenschaften_projgrundstueckpos
  WHERE liegenschaften_projgrundstueck.ogc_fid::text = liegenschaften_projgrundstueckpos.projgrundstueckpos_von::text;

ALTER TABLE $$DBSCHEMA.z_projgs_nr
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.z_projgs_nr TO $$USER;',2,'Was in table views',NULL,1),
 (69,'CREATE OR REPLACE VIEW $$DBSCHEMA.test_gp AS
 SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.identifikator, a.geometrie, a.lagegen, a.lagezuv, a.lagezuv_txt, a.punktzeichen, a.punktzeichen_txt, a.exaktdefiniert, a.exaktdefiniert_txt, a.hoheitsgrenzsteinalt, a.hoheitsgrenzsteinalt_txt
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
GRANT ALL ON TABLE $$DBSCHEMA.test_gp TO $$USER;',2,'Was in table views',NULL,1),
 (70,'CREATE OR REPLACE VIEW $$DBSCHEMA.bodenbedeckung_objektnamepos_v AS
 SELECT bodenbedeckung_objektname.aname,
    bodenbedeckung_objektnamepos.pos,
    bodenbedeckung_objektnamepos.ogc_fid
   FROM $$DBSCHEMA.bodenbedeckung_objektname,
    $$DBSCHEMA.bodenbedeckung_objektnamepos
  WHERE bodenbedeckung_objektname.ogc_fid::text = bodenbedeckung_objektnamepos.objektnamepos_von::text;

ALTER TABLE $$DBSCHEMA.bodenbedeckung_objektnamepos_v
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.bodenbedeckung_objektnamepos_v TO $$USER;',2,'Was in table views',NULL,1),
 (71,'CREATE OR REPLACE VIEW $$DBSCHEMA.t_bb_sym AS
 SELECT sym.ogc_fid,
    sym.boflaechesymbol_von::text,
    sym.pos,
    sym.ori,
    sym.ori * 0.9::double precision AS altori,
    bb.art,
    bb.art_txt
   FROM $$DBSCHEMA.bodenbedeckung_boflaechesymbol sym,
    $$DBSCHEMA.bodenbedeckung_boflaeche bb
  WHERE sym.boflaechesymbol_von::text = bb.ogc_fid::text;

ALTER TABLE $$DBSCHEMA.t_bb_sym
  OWNER TO $$USER;
GRANT ALL ON TABLE $$DBSCHEMA.t_bb_sym TO $$USER;
GRANT SELECT ON TABLE $$DBSCHEMA.t_bb_sym TO public;',2,'Was in table views',NULL,1),
 (72,'INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''FixpunkteKategorie1'', ''Points_fixesCategorie1'');
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
INSERT INTO $$DBSCHEMA.t_maengel_topics (topic_name, topic_name_fr) VALUES(''Planrahmen'', ''Bords_de_plan'');',3,'Was in table inserts',NULL,1),
 (73,'INSERT INTO $$DBSCHEMA.t_shortestline_hausnummerpos (ogc_fid, strname, hausnummer, a_tid, b_tid, lok_tid, the_geom)
SELECT a.ogc_fid, d."atext" as strnam, b.hausnummer, a.t_ili_tid as a_tid, b.t_ili_tid as b_tid,
       b.gebaeudeeingang_von::text as lok_tid, ST_ShortestLine(a.pos, c.geometrie) as the_geom
FROM $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos as a,
     $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang as b,
     (
       SELECT ST_Union(geometrie) as geometrie, strassenstueck_von::text
       FROM $$DBSCHEMA.gebaeudeadressen_strassenstueck
       GROUP BY strassenstueck_von::text
     ) as c,
     $$DBSCHEMA.gebaeudeadressen_lokalisationsname as d
WHERE a.hausnummerpos_von::text = b.ogc_fid::text
AND b.gebaeudeeingang_von::text = c.strassenstueck_von::text
AND d.benannte = b.gebaeudeeingang_von;',3,'Was in table inserts',NULL,1),
 (74,'INSERT INTO $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang (tid, entstehung, geometrie, flaeche, qualitaet, qualitaet_txt, art, art_txt)

SELECT c.t_ili_tid, c.entstehung, c.geometrie, ST_Area(c.geometrie) as flaeche, c.qualitaet, c.qualitaet_txt, c.art, c.art_txt
FROM
(
 SELECT bodenbedeckung_boflaeche.ogc_fid, bodenbedeckung_boflaeche.t_ili_tid, bodenbedeckung_boflaeche.entstehung,
        bodenbedeckung_boflaeche.geometrie, bodenbedeckung_boflaeche.qualitaet,
        bodenbedeckung_boflaeche.qualitaet_txt, bodenbedeckung_boflaeche.art, bodenbedeckung_boflaeche.art_txt
 FROM $$DBSCHEMA.bodenbedeckung_boflaeche
 WHERE bodenbedeckung_boflaeche.art = 0
 AND ST_Area(bodenbedeckung_boflaeche.geometrie) > 12::double precision

EXCEPT

 SELECT DISTINCT ON (a.ogc_fid) a.ogc_fid, a.t_ili_tid, a.entstehung, a.geometrie, a.qualitaet, a.qualitaet_txt,
        a.art, a.art_txt
 FROM $$DBSCHEMA.bodenbedeckung_boflaeche a, $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang b
 WHERE a.art = 0 AND ST_Area(a.geometrie) > 12::double precision
 AND a.geometrie && b.lage
 AND ST_Distance(a.geometrie, b.lage) = 0::double precision
) as c;',3,'Was in table inserts',NULL,1),
 (75,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_ausserhalb
(ogc_fid, tid, ori, hali, hali_txt, vali, vali_txt, groesse, groesse_txt, hausnummerpos_von, pos)
SELECT c.ogc_fid, c.t_ili_tid, c.ori, c.hali, c.hali_txt, c.vali, c.vali_txt, c.groesse, c.groesse_txt, c.hausnummerpos_von::text, c.pos
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
) as c;',3,'Was in table inserts',NULL,1),
 (76,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_hausnummerpos_doppelt
(ogc_fid, tid, hausnummerpos_von, pos, ori, hali, hali_txt, vali, vali_txt, groesse, groesse_txt)
SELECT a.ogc_fid, a.t_ili_tid, a.hausnummerpos_von, a.pos, a.ori, a.hali, a.hali_txt, a.vali, a.vali_txt, a.groesse, a.groesse_txt
FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos as a,
(
 SELECT gebaeudeadressen_hausnummerpos.ogc_fid, gebaeudeadressen_hausnummerpos.t_ili_tid,
        gebaeudeadressen_hausnummerpos.hausnummerpos_von, gebaeudeadressen_hausnummerpos.pos,
        gebaeudeadressen_hausnummerpos.ori, gebaeudeadressen_hausnummerpos.hali,
        gebaeudeadressen_hausnummerpos.hali_txt, gebaeudeadressen_hausnummerpos.vali,
        gebaeudeadressen_hausnummerpos.vali_txt, gebaeudeadressen_hausnummerpos.groesse,
        gebaeudeadressen_hausnummerpos.groesse_txt
 FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos

 EXCEPT

 SELECT DISTINCT ON (hausnummerpos_von) ogc_fid, t_ili_tid, hausnummerpos_von, pos, ori, hali, hali_txt, vali, vali_txt, groesse, groesse_txt
 FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos
) as b
WHERE a.hausnummerpos_von = b.hausnummerpos_von;',3,'Was in table inserts',NULL,1),
 (77,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_mit_nummer_ohne_pos
(ogc_fid, tid, entstehung, gebaeudeeingang_von, status, status_txt, inaenderung, inaenderung_txt, attributeprovisorisch,
  attributeprovisorisch_txt, istoffiziellebezeichnung, istoffiziellebezeichnung_txt, lage, hoehenlage, hausnummer, im_gebaeude,
  im_gebaeude_txt, gwr_egid, gwr_edid)

SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.gebaeudeeingang_von, a.status, a.status_txt, a.inaenderung, a.inaenderung_txt, a.attributeprovisorisch,
  a.attributeprovisorisch_txt, a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.lage, a.hoehenlage, a.hausnummer, a.im_gebaeude,
  a.im_gebaeude_txt, a.gwr_egid, a.gwr_edid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a,
(
 SELECT t_ili_tid
 FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang
 WHERE gebaeudeadressen_gebaeudeeingang.hausnummer IS NOT NULL

  EXCEPT

 SELECT hausnummerpos_von::text
 FROM $$DBSCHEMA.gebaeudeadressen_hausnummerpos

) b
WHERE a.t_ili_tid::text = b.t_ili_tid::text;
 ',3,'Was in table inserts',NULL,1),
 (78,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_gebaeudeeingang_gleiche_nummer_und_lok
(ogc_fid, tid, entstehung, gebaeudeeingang_von, status, status_txt, inaenderung, inaenderung_txt, attributeprovisorisch,
  attributeprovisorisch_txt, istoffiziellebezeichnung, istoffiziellebezeichnung_txt, lage, hoehenlage, hausnummer, im_gebaeude, im_gebaeude_txt,
  gwr_egid, gwr_edid)
SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.gebaeudeeingang_von, a.status, a.status_txt, a.inaenderung, a.inaenderung_txt, a.attributeprovisorisch,
  a.attributeprovisorisch_txt, a.istoffiziellebezeichnung, a.istoffiziellebezeichnung_txt, a.lage, a.hoehenlage, a.hausnummer, a.im_gebaeude, a.im_gebaeude_txt,
  a.gwr_egid, a.gwr_edid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a,
(
  SELECT gebaeudeadressen_gebaeudeeingang.ogc_fid, gebaeudeadressen_gebaeudeeingang.t_ili_tid,
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
         gebaeudeadressen_gebaeudeeingang.t_ili_tid, gebaeudeadressen_gebaeudeeingang.entstehung,
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
AND a.gebaeudeeingang_von = b.gebaeudeeingang_von;',3,'Was in table inserts',NULL,1),
 (79,'INSERT INTO $$DBSCHEMA.z_v_bb_ts  (geometrie,bb_ogc_fid, bb_art, bb_art_txt, ts_ogc_fid,ts_art, ts_art_txt,flaeche)
(select * from
(SELECT
  ST_Multi(ST_CollectionExtract(ST_intersection(ST_MakeValid(ts.geometrie),ST_MakeValid(bb.geometrie)),3)) as geometrie,
  bb.ogc_fid as bb_ogc_fid,
  bb.art as bb_art,
  bb.art_txt as bb_art_txt,
  ts.ogc_fid as ts_ogc_fid,
  ts.art as ts_art,
  ts.art_txt as ts_art_txt,
 st_area (ST_intersection(ST_MakeValid(ts.geometrie),ST_MakeValid(bb.geometrie))) as flaeche
FROM
$$DBSCHEMA.bodenbedeckung_boflaeche as bb,
$$DBSCHEMA.tseinteilung_toleranzstufe as ts
WHERE
ST_IsValid(St_Intersection(ST_MakeValid(bb.geometrie), ST_MakeValid(ts.geometrie)))=true and
St_Intersects(ST_MakeValid(bb.geometrie), ST_MakeValid(ts.geometrie))=true) as foo
WHERE (geometrytype(geometrie) = ''POLYGON'' OR geometrytype(geometrie) = ''MULTIPOLYGON'') AND NOT ST_IsEmpty(geometrie))',3,'Was in table inserts',NULL,1),
 (80,'INSERT INTO $$DBSCHEMA.z_grenzen (ogc_fid, geometrie)
SELECT DISTINCT b.ogc_fid,b.geometrie
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b
except
(
SELECT DISTINCT a.ogc_fid,a.geometrie
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt a, $$DBSCHEMA.liegenschaften_liegenschaft
  WHERE st_touches(a.geometrie, liegenschaften_liegenschaft.geometrie) IS TRUE
Union
SELECT DISTINCT b.ogc_fid,b.geometrie
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_selbstrecht
  WHERE st_touches(b.geometrie, liegenschaften_selbstrecht.geometrie) IS TRUE
Union
SELECT DISTINCT b.ogc_fid,b.geometrie
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projliegenschaft
  WHERE st_touches(b.geometrie, liegenschaften_projliegenschaft.geometrie) IS TRUE
UNION
SELECT DISTINCT b.ogc_fid,b.geometrie
   FROM $$DBSCHEMA.liegenschaften_grenzpunkt b, $$DBSCHEMA.liegenschaften_projselbstrecht
  WHERE st_touches(b.geometrie, liegenschaften_projselbstrecht.geometrie) IS TRUE
);',3,'Was in table inserts',NULL,1),
 (81,'INSERT INTO $$DBSCHEMA.z_v_bb_ls (bb_ogc_fid,bb_qualitaet,bb_qualitaet_txt,art,art_txt,ls_ogc_fid,liegenschaft_von,nummerteilgrundstueck,flaechenmass,geometrie,flaeche,ls_flaeche)

SELECT *
FROM
(
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
  ST_Multi(ST_CollectionExtract(ST_intersection(ST_MakeValid(bodenbedeckung_boflaeche.geometrie),ST_MakeValid(liegenschaften_liegenschaft.geometrie)),3)) as geometrie,
  ST_area (ST_intersection(ST_MakeValid(bodenbedeckung_boflaeche.geometrie),ST_MakeValid(liegenschaften_liegenschaft.geometrie))) as flaeche,
ST_area (ST_MakeValid(liegenschaften_liegenschaft.geometrie)) as ls_flaeche
FROM
  $$DBSCHEMA.bodenbedeckung_boflaeche,
  $$DBSCHEMA.liegenschaften_liegenschaft
WHERE
  ST_intersects(ST_MakeValid(bodenbedeckung_boflaeche.geometrie),ST_MakeValid(liegenschaften_liegenschaft.geometrie))=true --and
  --geometrytype(ST_intersection(bodenbedeckung_boflaeche.geometrie,liegenschaften_liegenschaft.geometrie)) = ''POLYGON''
 ) as foo
 WHERE (geometrytype(geometrie) = ''POLYGON'' OR geometrytype(geometrie) = ''MULTIPOLYGON'') AND NOT ST_IsEmpty(geometrie)',3,'Was in table inserts',NULL,1),
 (82,'INSERT INTO $$DBSCHEMA.z_ls_entstehung (ls_ogc_fid, geometrie,nummer, entstehung)
SELECT ls.ogc_fid, ls.geometrie,
gs.nummer, gs.entstehung
FROM $$DBSCHEMA.liegenschaften_grundstueck gs, $$DBSCHEMA.liegenschaften_liegenschaft ls
WHERE
ls.liegenschaft_von::text=gs.ogc_fid::text',3,'Was in table inserts',NULL,1),
 (83,'INSERT INTO $$DBSCHEMA.z_v_gp_ts (tid,entstehung,identifikator,geometrie,lagegen,lagezuv,lagezuv_txt,punktzeichen,punktzeichen_txt,exaktdefiniert,exaktdefiniert_txt,hoheitsgrenzsteinalt,
  hoheitsgrenzsteinalt_txt,art)
SELECT
  gp.t_ili_tid, gp.entstehung, gp.identifikator, gp.geometrie, gp.lagegen,gp.lagezuv, gp.lagezuv_txt, gp.punktzeichen, gp.punktzeichen_txt, gp.exaktdefiniert, gp.exaktdefiniert_txt, gp.hoheitsgrenzsteinalt, gp.hoheitsgrenzsteinalt_txt,ts.art
FROM
  $$DBSCHEMA.liegenschaften_grenzpunkt as gp,
  $$DBSCHEMA.tseinteilung_toleranzstufe as ts
WHERE
  ST_Intersects (gp.geometrie,ts.geometrie)=true',3,'Was in table inserts',NULL,1),
 (84,'INSERT INTO $$DBSCHEMA.z_liegenschaft_flaeche (tid, liegenschaft_von, nummerteilgrundstueck, geometrie,flaechenmass, flaeche, qualitaet, qualitaet_txt)
SELECT t_ili_tid, liegenschaft_von, nummerteilgrundstueck, geometrie,
       flaechenmass, st_area(geometrie) as flaeche, qualitaet, qualitaet_txt
  FROM $$DBSCHEMA.liegenschaften_liegenschaft',3,'Was in table inserts',NULL,1),
 (85,'INSERT INTO $$DBSCHEMA.z_selbstrecht_flaeche (tid, selbstrecht_von, nummerteilgrundstueck, geometrie,flaechenmass, flaeche, qualitaet, qualitaet_txt)
SELECT t_ili_tid, selbstrecht_von, nummerteilgrundstueck, geometrie,
       flaechenmass, st_area(geometrie) as flaeche, qualitaet, qualitaet_txt
  FROM $$DBSCHEMA.liegenschaften_selbstrecht',3,'Was in table inserts',NULL,1),
 (86,'INSERT INTO $$DBSCHEMA.z_hgp_ls_linie (ogc_fid, geometrie)
select * from(
SELECT DISTINCT
 gemeindegrenzen_hoheitsgrenzpunkt.ogc_fid,  st_CollectionExtract(gemeindegrenzen_hoheitsgrenzpunkt.geometrie,1) as geometrie
 FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze, $$DBSCHEMA.gemeindegrenzen_hoheitsgrenzpunkt
 WHERE st_touches(gemeindegrenzen_gemeindegrenze.geometrie, gemeindegrenzen_hoheitsgrenzpunkt.geometrie) IS False) as foo where geometrytype(geometrie) = ''POINT''',3,'Was in table inserts',NULL,1),
 (87,'INSERT INTO $$DBSCHEMA.z_v_ls_nk (ls_fid,nk_fid,geometrie,flaeche)
SELECT *
FROM
(SELECT
  liegenschaften_liegenschaft.ogc_fid as ls_fid,
  nomenklatur_flurname.ogc_fid as nk_fid,
 ST_Multi(ST_CollectionExtract(st_intersection(nomenklatur_flurname.geometrie,   liegenschaften_liegenschaft.geometrie),3)) as geometrie,
 st_area ( st_intersection(nomenklatur_flurname.geometrie,   liegenschaften_liegenschaft.geometrie)) as flaeche
FROM
  $$DBSCHEMA.liegenschaften_liegenschaft,
  $$DBSCHEMA.nomenklatur_flurname
WHERE
  st_intersects(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie)=true and
  ST_IsValid(st_intersection(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie))=true) as foo  WHERE (geometrytype(geometrie) = ''POLYGON'' OR geometrytype(geometrie) = ''MULTIPOLYGON'') AND NOT ST_IsEmpty(geometrie)',3,'Was in table inserts',NULL,1),
 (88,'INSERT INTO $$DBSCHEMA.z_nr_gs (nbident,nummer,egris_egrid,gueltigkeit,gueltigkeit_txt,vollstaendigkeit,vollstaendigkeit_txt,art,art_txt,gesamteflaechenmass,nummerteilgrundstueck,Pos,lin)
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
  liegenschaften_selbstrecht.nummerteilgrundstueck,
  liegenschaften_grundstueckpos.pos,
  (case(st_contains(liegenschaften_selbstrecht.geometrie,liegenschaften_grundstueckpos.pos)) when false then 1 else 0 end) as lin
FROM
  $$DBSCHEMA.liegenschaften_selbstrecht,
  $$DBSCHEMA.liegenschaften_grundstueck,
  $$DBSCHEMA.liegenschaften_grundstueckpos
WHERE
  liegenschaften_grundstueck.gesamteflaechenmass is NULL AND
  liegenschaften_grundstueck.ogc_fid::text = liegenschaften_selbstrecht.selbstrecht_von::text AND
  liegenschaften_grundstueckpos.grundstueckpos_von::text = liegenschaften_grundstueck.ogc_fid::text',3,'Was in table inserts',NULL,1),
 (89,'INSERT INTO $$DBSCHEMA.z_nr_gs  (nbident,nummer,egris_egrid,gueltigkeit,gueltigkeit_txt,vollstaendigkeit,vollstaendigkeit_txt,art,art_txt,gesamteflaechenmass,nummerteilgrundstueck,Pos,lin)
select * from (
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
  liegenschaften_liegenschaft.nummerteilgrundstueck,
  st_CollectionExtract(liegenschaften_grundstueckpos.pos,1) as pos,
  (case (st_contains(liegenschaften_liegenschaft.geometrie,liegenschaften_grundstueckpos.pos)) When False Then 1 Else 0 End) as lin
FROM
  $$DBSCHEMA.liegenschaften_liegenschaft,
  $$DBSCHEMA.liegenschaften_grundstueck,
  $$DBSCHEMA.liegenschaften_grundstueckpos
WHERE
  liegenschaften_grundstueck.gesamteflaechenmass is NULL AND
  liegenschaften_grundstueck.ogc_fid::text = liegenschaften_liegenschaft.liegenschaft_von::text AND
  liegenschaften_grundstueckpos.grundstueckpos_von::text = liegenschaften_grundstueck.ogc_fid::text) as foo
where geometrytype(pos) = ''POINT'' ',3,'Was in table inserts',NULL,1),
 (90,'INSERT INTO $$DBSCHEMA.z_v_ls_nk_pkt (ls_fid,nk_fid,flaeche,geometrie)
SELECT
  liegenschaften_liegenschaft.ogc_fid as ls_fid,
  nomenklatur_flurname.ogc_fid as nk_fid,
 st_area ( st_intersection(nomenklatur_flurname.geometrie,   liegenschaften_liegenschaft.geometrie)) as flaeche,
 st_PointonSurface(st_intersection(nomenklatur_flurname.geometrie,liegenschaften_liegenschaft.geometrie)) as geometrie
 from $$DBSCHEMA.liegenschaften_liegenschaft,
  $$DBSCHEMA.nomenklatur_flurname
WHERE
  st_intersects(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie)=true and
  ST_IsValid(st_intersection(nomenklatur_flurname.geometrie, liegenschaften_liegenschaft.geometrie))=true',3,'Was in table inserts',NULL,1),
 (91,'INSERT INTO $$DBSCHEMA.z_nr_gs (nbident,nummer,egris_egrid,gueltigkeit,gueltigkeit_txt,vollstaendigkeit,vollstaendigkeit_txt,art,art_txt,gesamteflaechenmass,nummerteilgrundstueck,Pos,lin)
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
  liegenschaften_selbstrecht.nummerteilgrundstueck,
  liegenschaften_teilsrpos.pos,
  (case(st_contains(liegenschaften_selbstrecht.geometrie,liegenschaften_teilsrpos.pos))when false then 1 else 0 end) as Lin
FROM
  $$DBSCHEMA.liegenschaften_selbstrecht,
  $$DBSCHEMA.liegenschaften_grundstueck,
  $$DBSCHEMA.liegenschaften_teilsrpos
WHERE
  liegenschaften_grundstueck.gesamteflaechenmass >0 AND
  liegenschaften_grundstueck.ogc_fid::text = liegenschaften_selbstrecht.selbstrecht_von::text AND
  liegenschaften_teilsrpos.teilsrpos_von::text = liegenschaften_selbstrecht.ogc_fid::text',3,'Was in table inserts',NULL,1),
 (92,'INSERT INTO $$DBSCHEMA.z_nr_gs (nbident,nummer,egris_egrid,gueltigkeit,gueltigkeit_txt,vollstaendigkeit,vollstaendigkeit_txt,art,art_txt,gesamteflaechenmass,nummerteilgrundstueck,Pos,lin)
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
  liegenschaften_liegenschaft.nummerteilgrundstueck,
  liegenschaften_teillspos.pos,
  (case(st_contains(liegenschaften_liegenschaft.geometrie,liegenschaften_teillspos.pos)) when false Then 1 else 0 end) as Lin
FROM
  $$DBSCHEMA.liegenschaften_liegenschaft,
  $$DBSCHEMA.liegenschaften_grundstueck,
  $$DBSCHEMA.liegenschaften_teillspos
WHERE
  liegenschaften_grundstueck.gesamteflaechenmass >0 AND
  liegenschaften_grundstueck.ogc_fid::text = liegenschaften_liegenschaft.liegenschaft_von::text AND
  liegenschaften_teillspos.teillspos_von::text = liegenschaften_liegenschaft.ogc_fid::text',3,'Was in table inserts',NULL,1),
 (93,'INSERT INTO $$DBSCHEMA.z_objektnummer_pos (nummer,gwr_egid,nbident,pos,ori,groesse,vali_txt,vali,hali_txt,hali,groesse_txt)
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
  einzelobjekte_objektnummerpos.groesse_txt
FROM
  $$DBSCHEMA.einzelobjekte_objektnummer,
  $$DBSCHEMA.einzelobjekte_objektnummerpos
WHERE
  einzelobjekte_objektnummer.ogc_fid::text = einzelobjekte_objektnummerpos.objektnummerpos_von::text',3,'Was in table inserts',NULL,1),
 (94,'INSERT INTO $$DBSCHEMA.z_gebaeudenummer_pos (nummer,gwr_egid,nbident,pos,ori,groesse,vali_txt,vali,hali_txt,hali,groesse_txt)
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
  bodenbedeckung_gebaeudenummerpos.groesse_txt
FROM
  $$DBSCHEMA.bodenbedeckung_gebaeudenummer,
  $$DBSCHEMA.bodenbedeckung_gebaeudenummerpos
WHERE
  bodenbedeckung_gebaeudenummer.ogc_fid::text = bodenbedeckung_gebaeudenummerpos.gebaeudenummerpos_von::text',3,'Was in table inserts',NULL,1),
 (95,'INSERT INTO $$DBSCHEMA.t_gebaeudeadressen_spinnennetz (ogc_fid, tid, line, hausnummer)
SELECT distinct a.ogc_fid, a.t_ili_tid, ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(c.pos)::text) || '' ''::text) || ST_Y(c.pos)::text) || '')''::text, $$EPSG) AS line, a.hausnummer

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
WHERE b.atid::text = a.t_ili_tid::text
AND b.btid::text = c.t_ili_tid::text;',3,'Was in table inserts',NULL,1),
 (96,'GRANT USAGE ON SCHEMA $$DBSCHEMA TO $$USER;
GRANT SELECT ON ALL TABLES IN SCHEMA $$DBSCHEMA TO $$USER;',5,'Was in table postprocessing',NULL,1),
 (97,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_uebriger_gebaeudeteil_isolierte_flaeche AS
SELECT elem.ogc_fid, elem.t_ili_tid, elem.geometrie
FROM $$DBSCHEMA.einzelobjekte_flaechenelement AS elem
JOIN $$DBSCHEMA.einzelobjekte_einzelobjekt AS obj ON elem.flaechenelement_von = obj.ogc_fid
LEFT JOIN
(SELECT DISTINCT elem.ogc_fid FROM $$DBSCHEMA.einzelobjekte_flaechenelement AS elem
JOIN $$DBSCHEMA.bodenbedeckung_boflaeche AS boden ON ST_DWithin(ST_BUFFER(elem.geometrie, -0.05), boden.geometrie, 0)
WHERE boden.art_txt = ''Gebaeude'') touches
ON touches.ogc_fid = elem.ogc_fid WHERE touches.ogc_fid IS NULL AND obj.art_txt = ''uebriger_Gebaeudeteil'';
GRANT SELECT ON TABLE $$DBSCHEMA.v_uebriger_gebaeudeteil_isolierte_flaeche TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_uebriger_gebaeudeteil_isolierte_linien AS
SELECT elem.ogc_fid, elem.t_ili_tid, elem.geometrie
FROM $$DBSCHEMA.einzelobjekte_linienelement AS elem
JOIN $$DBSCHEMA.einzelobjekte_einzelobjekt AS obj ON elem.linienelement_von = obj.ogc_fid
LEFT JOIN
(SELECT DISTINCT elem.ogc_fid FROM $$DBSCHEMA.einzelobjekte_linienelement AS elem
JOIN $$DBSCHEMA.bodenbedeckung_boflaeche AS boden ON ST_DWithin(ST_BUFFER(elem.geometrie, -0.05), boden.geometrie, 0)
WHERE boden.art_txt = ''Gebaeude'') touches
ON touches.ogc_fid = elem.ogc_fid WHERE touches.ogc_fid IS NULL AND obj.art_txt = ''uebriger_Gebaeudeteil'';
GRANT SELECT ON TABLE $$DBSCHEMA.v_uebriger_gebaeudeteil_isolierte_linien TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_uebriger_gebaeudeteil_isolierte_punkte AS
SELECT elem.ogc_fid, elem.t_ili_tid, elem.geometrie
FROM $$DBSCHEMA.einzelobjekte_punktelement AS elem
JOIN $$DBSCHEMA.einzelobjekte_einzelobjekt AS obj on elem.punktelement_von = obj.ogc_fid
LEFT JOIN
(SELECT DISTINCT elem.ogc_fid FROM $$DBSCHEMA.einzelobjekte_punktelement AS elem
JOIN $$DBSCHEMA.bodenbedeckung_boflaeche AS boden ON ST_DWithin(ST_BUFFER(elem.geometrie, -0.05), boden.geometrie, 0)
WHERE boden.art_txt = ''Gebaeude'') touches
ON touches.ogc_fid = elem.ogc_fid WHERE touches.ogc_fid IS NULL AND obj.art_txt = ''uebriger_Gebaeudeteil'';
GRANT SELECT ON TABLE $$DBSCHEMA.v_uebriger_gebaeudeteil_isolierte_punkte TO $$USER;',5,'Was in table postprocessing',NULL,1),
 (98,'CREATE TYPE $$DBSCHEMA.maengel_bereinigen AS ENUM
(
 ''i.O.'',
 ''nicht bereinigen''
);
CREATE TYPE $$DBSCHEMA.maengel_abrechnung AS ENUM
(
''PNF'',
''LNF'',
''Fehler''
);
CREATE TYPE $$DBSCHEMA.maengel_verifikation AS ENUM
(
''Ja'',
''Nein''
);
CREATE TYPE $$DBSCHEMA.avor_bezeichnung AS ENUM
(
''0-PNF1: In PNF1 beurteilt und entschieden nicht zu bearbeiten'',
''1-Waldgrenzen: Kontrolle und Beurteilung'',
''2-Übr. best. Fläche entlang Bäche, Bahn, Autobahn bereinigen'',
''3-Wytweiden: Definition durch Waldabteilung'',
''4-Schmale bestockte Fläche ab Bodenbedeckung in Eo übernehmen'',
''5-Schmale bestockte Fläche löschen'',
''6-Wanderwege: wenn fehlend, als Achse in Einzelobjekte erfassen'',
''7-Wege in Landswirtschaftszone gemäss Handbuch'',
''8-GNBE: Kontrolle, fehlende erfassen, Name attributieren, ...'',
''9-Flüsse und Seen: Bodenbedeckung nach Prinzip LWN anpassen'',
''10-Hochwasserdamm darstellen od. löschen'',
''11-Bauernhof: Gartenanlage od. übrig befestigt anpassen'',
''12-Bauernhof: durchgehenden Weg erfassen'',
''13-Erfassung und/oder Ergänzungen von Gebäudeerschliessungen'',
''14-Erfassung und/oder Ergänzung von grossen Parkplätzen'',
''15-Erfassung und/oder Ergänzung von übrig befestigen Flächen'',
''16-Bahnhof / Station: Bahnsteig erfassen'',
''17-Bereinigung an Gemeinde- oder Losgrenzen (Differenzen zu BB)'',
''18-Einzelobjekte: Bereinigung gemäss Handbuch'',
''19-Löschen von überflüssigen Bodenbedeckungsgrenzen'',
''20-neue BB ausscheiden, BB Art ändern, BB Abgrenzung anpassen'',
''21-fehlendes Silo / Wasserbecken / Gebäude etc.'',
''22-fehlende Brücke/ Mast/ schm. Weg/ eing. Gewässer/ Tunnel'',
''23-Gebäude vorhanden / unterierdisch?'',
''24-Bodenbedeckung löschen'',
''25-Einzelobjekt löschen'',
''26-Diverses''
);

-- The following table create assume these roles are available
--CREATE ROLE agi WITH LOGIN;
--CREATE ROLE geometer WITH LOGIN;
--CREATE ROLE forst WITH LOGIN;
--CREATE ROLE avor WITH LOGIN;


CREATE TABLE $$DBSCHEMA.t_maengel_punkt
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic,
 bezeichnun $$DBSCHEMA.avor_bezeichnung, --bezeichnung
 abrechnung $$DBSCHEMA.maengel_abrechnung,
 bem_avor varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bem_nfg text, --bemerkung_nfg
 forstorgan $$DBSCHEMA.maengel_bereinigen,
 bem_forst text, --bemerkung_forst
 verifikati $$DBSCHEMA.maengel_verifikation, --verifikation
 bem_verifi text, --bemerkung_verifikation
 erledigt bool,
 the_geom geometry(POINT,$$EPSG),
 CONSTRAINT t_maengel_punkt_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
--GRANT ALL ON TABLE $$DBSCHEMA.t_maengel_punkt TO $$USER;

REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_punkt FROM agi;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_punkt FROM geometer;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_punkt FROM forst;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_punkt FROM avor;

GRANT SELECT, UPDATE, INSERT, DELETE ON $$DBSCHEMA.t_maengel_punkt TO agi;
GRANT SELECT, UPDATE(bem_nfg) ON $$DBSCHEMA.t_maengel_punkt TO geometer;
GRANT SELECT, UPDATE(forstorgan, bem_forst) ON $$DBSCHEMA.t_maengel_punkt TO forst;
GRANT SELECT, UPDATE(topic, bezeichnun, bem_avor, abrechnung), INSERT, DELETE ON $$DBSCHEMA.t_maengel_punkt TO avor;

GRANT USAGE ON $$DBSCHEMA.t_maengel_punkt_ogc_fid_seq TO agi;
GRANT USAGE ON $$DBSCHEMA.t_maengel_punkt_ogc_fid_seq TO avor;

-- LINES
CREATE TABLE $$DBSCHEMA.t_maengel_linie
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic,
 bezeichnun $$DBSCHEMA.avor_bezeichnung, --bezeichnung
 abrechnung $$DBSCHEMA.maengel_abrechnung,
 bem_avor varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bem_nfg text, --bemerkung_nfg
 forstorgan $$DBSCHEMA.maengel_bereinigen,
 bem_forst text, --bemerkung_forst
 verifikati $$DBSCHEMA.maengel_verifikation, --verifikation
 bem_verifi text, --bemerkung_verifikation
 erledigt bool,
 the_geom geometry(LINESTRING,$$EPSG),
 CONSTRAINT t_maengel_linie_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
--GRANT ALL ON TABLE $$DBSCHEMA.t_maengel_linie TO $$USER;

REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_linie FROM agi;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_linie FROM geometer;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_linie FROM forst;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_linie FROM avor;

GRANT SELECT, UPDATE, INSERT, DELETE ON $$DBSCHEMA.t_maengel_linie TO agi;
GRANT SELECT, UPDATE(bem_nfg) ON $$DBSCHEMA.t_maengel_linie TO geometer;
GRANT SELECT, UPDATE(forstorgan, bem_forst) ON $$DBSCHEMA.t_maengel_linie TO forst;
GRANT SELECT, UPDATE(topic, bezeichnun, bem_avor, abrechnung), INSERT, DELETE ON $$DBSCHEMA.t_maengel_linie TO avor;

GRANT USAGE ON $$DBSCHEMA.t_maengel_linie_ogc_fid_seq TO agi;
GRANT USAGE ON $$DBSCHEMA.t_maengel_linie_ogc_fid_seq TO avor;

CREATE TABLE $$DBSCHEMA.t_maengel_polygon
(
 ogc_fid serial NOT NULL,
 topic $$DBSCHEMA.maengel_topic,
 bezeichnun $$DBSCHEMA.avor_bezeichnung, --bezeichnung
 abrechnung $$DBSCHEMA.maengel_abrechnung,
 bem_avor varchar,
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 bem_nfg text, --bemerkung_nfg
 forstorgan $$DBSCHEMA.maengel_bereinigen,
 bem_forst text, --bemerkung_forst
 verifikati $$DBSCHEMA.maengel_verifikation, --verifikation
 bem_verifi text, --bemerkung_verifikation
 erledigt bool,
 the_geom geometry(POLYGON,$$EPSG),
 CONSTRAINT t_maengel_polygon_pkey PRIMARY KEY (ogc_fid)
)
WITH (OIDS=FALSE);
--GRANT ALL ON TABLE $$DBSCHEMA.t_maengel_polygon TO $$USER;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_polygon FROM agi;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_polygon FROM geometer;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_polygon FROM forst;
REVOKE ALL PRIVILEGES ON $$DBSCHEMA.t_maengel_polygon FROM avor;

GRANT SELECT, UPDATE, INSERT, DELETE ON $$DBSCHEMA.t_maengel_polygon TO agi;
GRANT SELECT, UPDATE(bem_nfg) ON $$DBSCHEMA.t_maengel_polygon TO geometer;
GRANT SELECT, UPDATE(forstorgan, bem_forst) ON $$DBSCHEMA.t_maengel_polygon TO forst;
GRANT SELECT, UPDATE(topic, bezeichnun, bem_avor, abrechnung), INSERT, DELETE ON $$DBSCHEMA.t_maengel_polygon TO avor;

GRANT USAGE ON $$DBSCHEMA.t_maengel_polygon_ogc_fid_seq TO agi;
GRANT USAGE ON $$DBSCHEMA.t_maengel_polygon_ogc_fid_seq TO avor;

',5,'allow defects list
',NULL,1),
 (99,'CREATE TABLE $$DBSCHEMA.t_topics_tables AS

SELECT bar.basket_ogc_fid, bar.ogc_fid, bar.topic, bar.class_name, bar.sql_name, bar.ili_name, bar.f_geometry_column, pkey.attname as primary_key
FROM
(

SELECT basket_ogc_fid, ogc_fid, topic, class_name, sql_name, ili_name, f_geometry_column
FROM
(
 SELECT a.ogc_fid as basket_ogc_fid, substring(topic, position(''.'' in topic) + 1) as topic
 FROM $$DBSCHEMA.t_ili2db_import_basket as a, $$DBSCHEMA.t_ili2db_basket as b
 WHERE a.basket = b.ogc_fid

) as basket,
(
 SELECT ogc_fid, import_basket, class_name, sql_name, ili_name, g.f_geometry_column
 FROM
 (
  SELECT d.ogc_fid, d.import_basket, e.class_name, e.sql_name, e.ili_name
  FROM
  $$DBSCHEMA.t_ili2db_import_object as d,
  (
   SELECT substring(class_name, position(''.'' in class_name) + 1) as class_name, lower(sqlname) as sql_name, iliname as ili_name
   FROM
   (
    SELECT substring("class", position(''.'' in "class") + 1) as class_name, sqlname, iliname
    FROM $$DBSCHEMA.t_ili2db_import_object as a, $$DBSCHEMA.t_ili2db_classname as b
    WHERE a."class" = b.iliname
   ) as c
  ) as e
  WHERE e.ili_name = d."class"
 ) as classes
 LEFT OUTER JOIN
 (
  SELECT *
  FROM geometry_columns
  WHERE f_table_schema = ''$$DBSCHEMA''
 ) as g
 ON classes.sql_name = g.f_table_name
 ORDER BY classes.import_basket
) as foo
WHERE basket.basket_ogc_fid = foo.import_basket
ORDER BY basket_ogc_fid, class_name

) as bar,
(
 SELECT a.attname, i.indrelid
 FROM pg_index as i
 JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
 WHERE i.indisprimary
) as pkey
WHERE pkey.indrelid = (''$$DBSCHEMA.'' || bar.sql_name)::regclass ;

GRANT SELECT ON TABLE $$DBSCHEMA.t_topics_tables TO $$USER;',999,'Create a table of all topics table for the tables menu',NULL,1);
COMMIT;
