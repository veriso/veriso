BEGIN TRANSACTION;
CREATE TABLE postprocessing (
    "ogc_fid" INTEGER PRIMARY KEY NOT NULL,
    "sql_query" TEXT,
    "order" INTEGER,
    "comment" TEXT,
    "lang" TEXT
, "apply" INTEGER   DEFAULT (1));
INSERT INTO `postprocessing` (ogc_fid,sql_query,order,comment,lang,apply) VALUES (1,'GRANT USAGE ON SCHEMA $$DBSCHEMA TO $$USER;
GRANT SELECT ON ALL TABLES IN SCHEMA $$DBSCHEMA TO $$USER;',1,'Grant usage for the imported data to the read-only user.',NULL,1),
 (2,'CREATE TYPE $$DBSCHEMA.maengel_topic AS ENUM 
(
 ''FixpunkteKatgrie1'', 
 ''FixpunkteKatgrie2'', 
 ''FixpunkteKatgrie3'', 
 ''Bodenbedeckung'', 
 ''Einzelobjekte'', 
 ''Hoehen'', 
 ''Nomenklatur'', 
 ''Liegenschaften'', 
 ''Rohrleitungen'', 
 ''Nummerierungsbereiche'', 
 ''Gemeindegrenzen'', 
 ''Bezirksgrenzen'', 
 ''Kantonsgrenzen'', 
 ''Landesgrenzen'', 
 ''Planeinteilungen'', 
 ''TSEinteilung'', 
 ''Rutschgebiete'', 
 ''PLZOrtschaft'', 
 ''Gebaeudeadressen'', 
 ''Planrahmen''
);',5,'German enum type for t_maengel_topic.','de',1),
 (3,'CREATE TYPE $$DBSCHEMA.maengel_topic AS ENUM 
(
 ''Points_fixesCategorie1'', 
 ''Points_fixesCategorie2'', 
 ''Points_fixesCategorie3'', 
 ''Couverture_du_sol'', 
 ''Objets_divers'', 
 ''Altimetrie'', 
 ''Nomenclature'', 
 ''Biens_fonds'', 
 ''Conduites'', 
 ''Domaines_numerotation'', 
 ''Limites_commune'', 
 ''Limites_district'', 
 ''Limites_canton'', 
 ''Limites_nationales'', 
 ''Repartitions_plans'', 
 ''RepartitionNT'', 
 ''Zones_glissement'', 
 ''NPA_Localite'', 
 ''Adresses_des_batiments'', 
 ''Bords_de_plan''
);',5,'French enum type for t_maengel_topic','fr',1),
 (4,'CREATE TABLE $$DBSCHEMA.t_topics_tables AS

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

GRANT SELECT ON TABLE $$DBSCHEMA.t_topics_tables TO $$USER;',6,'This is for the topics-table-loader. No language support.',NULL,1),
 (5,'CREATE TABLE $$DBSCHEMA.t_lfp3_ausserhalb_gemeinde AS
SELECT a.ogc_fid, a.t_ili_tid, a.entstehung, a.nbident, a.nummer, a.hoehegeom, 
       a.lagegen, a.lagezuv, a.hoehegen, a.hoehezuv, 
       a.punktzeichen, a.protokoll, 
       a.geometrie::geometry(Point,$$EPSG)
FROM $$DBSCHEMA.fixpunktekatgrie3_lfp3 a, 
(
 SELECT (ST_Union(geometrie)) as geometrie
 FROM $$DBSCHEMA.gemeindegrenzen_gemeindegrenze
) b
WHERE ST_Distance(a.geometrie, b.geometrie) > 0;

ALTER TABLE $$DBSCHEMA.t_lfp3_ausserhalb_gemeinde ADD PRIMARY KEY (ogc_fid);
GRANT SELECT ON TABLE $$DBSCHEMA.t_lfp3_ausserhalb_gemeinde TO $$USER;',20,'LFP3 outside community. 

You really have to set the  geometry type to make this work properly.',NULL,1),
 (6,'CREATE TABLE $$DBSCHEMA.t_maengel_punkt 
(
 ogc_fid serial NOT NULL, 
 topic $$DBSCHEMA.maengel_topic NOT NULL, 
 bemerkung varchar, 
 datum timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 
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
 the_geom geometry(POLYGON,$$EPSG), 
 CONSTRAINT t_maengel_polygon_pkey PRIMARY KEY (ogc_fid)
) 
WITH (OIDS=FALSE); 
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_polygon TO $$USER;',6,'Defects tables (points and lines).',NULL,1),
 (7,'CREATE TABLE $$DBSCHEMA.t_lfp3_pro_ts AS

WITH ts AS (
 SELECT ST_Union(geometrie) as the_geom, ST_Area(ST_Union(geometrie))/10000 as area_ha, art
 FROM $$DBSCHEMA.tseinteilung_toleranzstufe
 GROUP BY art
)

SELECT ts.art as toleranzstufe, ts.area_ha as flaeche_ha, count(ts.art)::integer as ist_anzahl, 
CASE 
 WHEN art = ''TS1'' THEN ts.area_ha * 150 / 100
 WHEN art = ''TS2'' THEN ts.area_ha * 70 / 100
 WHEN art = ''TS3'' THEN ts.area_ha * 20 / 100
 WHEN art = ''TS4'' THEN ts.area_ha * 10 / 100
 WHEN art = ''TS5'' THEN ts.area_ha * 2 / 100
END::integer as soll_anzahl

FROM ts, $$DBSCHEMA.fixpunktekatgrie3_lfp3 as lfp3
WHERE ST_Distance(ts.the_geom, lfp3.geometrie) = 0
GROUP BY ts.art, ts.area_ha
ORDER BY ts.art;

ALTER TABLE $$DBSCHEMA.t_lfp3_pro_ts ADD PRIMARY KEY (toleranzstufe);
GRANT SELECT ON TABLE $$DBSCHEMA.t_lfp3_pro_ts TO $$USER;',20,'LFP3 per TS',NULL,1),
 (8,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_flaechenelement AS
SELECT b.*, a.art
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_flaechenelement as b
WHERE b.flaechenelement_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_flaechenelement TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_linienelement AS
SELECT b.*, a.art
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_linienelement as b
WHERE b.linienelement_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_linienelement TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_punktelement AS
SELECT b.*, a.art
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_punktelement as b
WHERE b.punktelement_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_punktelement TO $$USER;',30,'Views for single objects.',NULL,1),
 (9,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_liegenschaften_liegenschaft AS
SELECT l.ogc_fid, g.nbident, g.nummer, g.egris_egrid, g.gueltigkeit, g.vollstaendigkeit, g.art, l.flaechenmass, l.geometrie
FROM $$DBSCHEMA.liegenschaften_grundstueck g, $$DBSCHEMA.liegenschaften_liegenschaft l
WHERE g.ogc_fid = l.liegenschaft_von;

GRANT SELECT ON TABLE $$DBSCHEMA.v_liegenschaften_liegenschaft TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_liegenschaften_projliegenschaft AS
SELECT l.ogc_fid, g.nbident, g.nummer, g.egris_egrid, g.gueltigkeit, g.vollstaendigkeit, g.art, l.flaechenmass, l.geometrie
FROM $$DBSCHEMA.liegenschaften_projgrundstueck g, $$DBSCHEMA.liegenschaften_projliegenschaft l
WHERE g.ogc_fid = l.projliegenschaft_von;

GRANT SELECT ON TABLE $$DBSCHEMA.v_liegenschaften_projliegenschaft TO $$USER;


CREATE OR REPLACE VIEW $$DBSCHEMA.v_liegenschaften_selbstrecht AS
SELECT l.ogc_fid, g.nbident, g.nummer, g.egris_egrid, g.gueltigkeit, g.vollstaendigkeit, g.art, l.flaechenmass, l.geometrie
FROM $$DBSCHEMA.liegenschaften_grundstueck g, $$DBSCHEMA.liegenschaften_selbstrecht l
WHERE g.ogc_fid = l.selbstrecht_von;

GRANT SELECT ON TABLE $$DBSCHEMA.v_liegenschaften_selbstrecht TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_liegenschaften_projselbstrecht AS
SELECT l.ogc_fid, g.nbident, g.nummer, g.egris_egrid, g.gueltigkeit, g.vollstaendigkeit, g.art, l.flaechenmass, l.geometrie
FROM $$DBSCHEMA.liegenschaften_projgrundstueck g, $$DBSCHEMA.liegenschaften_projselbstrecht l
WHERE g.ogc_fid = l.projselbstrecht_von;

GRANT SELECT ON TABLE $$DBSCHEMA.v_liegenschaften_selbstrecht TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_liegenschaften_grundstueckpos AS
SELECT l.*, g.nummer, g.nbident, g.egris_egrid, g.gueltigkeit, g.art
FROM $$DBSCHEMA.liegenschaften_grundstueck g, $$DBSCHEMA.liegenschaften_grundstueckpos l
WHERE g.ogc_fid = l.grundstueckpos_von;

GRANT SELECT ON TABLE $$DBSCHEMA.v_liegenschaften_grundstueckpos TO $$USER;',40,'Views for real estates.',NULL,1),
 (10,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_bodenbedeckung_boflaechesymbol AS
SELECT b.*, a.art
FROM $$DBSCHEMA.bodenbedeckung_boflaeche as a, $$DBSCHEMA.bodenbedeckung_boflaechesymbol as b
WHERE b.boflaechesymbol_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_bodenbedeckung_boflaechesymbol TO $$USER;',30,'View for land surface symbols.',NULL,1),
 (11,'CREATE TABLE $$DBSCHEMA.t_topics_tables AS

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

GRANT SELECT ON TABLE $$DBSCHEMA.t_topics_tables TO $$USER;
',999,'Create a table of all topics table for the tables menu',NULL,1);
COMMIT;
