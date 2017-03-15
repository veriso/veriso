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
 (4,'CREATE TABLE $$DBSCHEMA.t_maengel_punkt 
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
GRANT SELECT ON TABLE $$DBSCHEMA.t_maengel_linie TO $$USER;',10,'Create the maengel tables (lines and points).
Must be called *after* the creation of the maengel_topic enum type.',NULL,1),
 (5,'CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_lokalisationsnamepos AS 
SELECT b.ogc_fid, b.t_ili_tid, b.lokalisationsnamepos_von, b.anfindex, b.endindex, b.pos, b.ori, b.hali, b.vali, b.groesse, b.hilfslinie, ST_X(b.pos) AS y, ST_Y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.benannte, a.atext
FROM $$DBSCHEMA.gebaeudeadressen_lokalisationsname a, $$DBSCHEMA.gebaeudeadressen_lokalisationsnamepos b
WHERE a.ogc_fid = b.lokalisationsnamepos_von;

ALTER TABLE $$DBSCHEMA.t_gebaeudeadressen_lokalisationsnamepos ADD PRIMARY KEY (ogc_fid);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_lokalisationsnamepos TO $$USER;

CREATE TABLE $$DBSCHEMA.t_distanz_gebaeudeeingang_lokalisationsnamepos AS
SELECT a.ogc_fid AS a_ogc_fid, b.ogc_fid AS b_ogc_fid, min(ST_Length(ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(b.pos)::text) || '' ''::text) || ST_Y(b.pos)::text) || '')''::text, $$EPSG))) AS min
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, $$DBSCHEMA.t_gebaeudeadressen_lokalisationsnamepos b
WHERE a.gebaeudeeingang_von::text = b.benannte::text 
GROUP BY a.ogc_fid, b.ogc_fid
ORDER BY a.ogc_fid, min(ST_Length(ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(b.pos)::text) || '' ''::text) || ST_Y(b.pos)::text) || '')''::text, $$EPSG)));

GRANT SELECT ON TABLE $$DBSCHEMA.t_distanz_gebaeudeeingang_lokalisationsnamepos TO $$USER;

CREATE TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz AS
SELECT a.ogc_fid, a.t_ili_tid, ST_GeometryFromText((((((((''LINESTRING(''::text || ST_X(a.lage)::text) || '' ''::text) || ST_Y(a.lage)::text) || '',''::text) || ST_X(c.pos)::text) || '' ''::text) || ST_Y(c.pos)::text) || '')''::text, $$EPSG)::geometry(LineString,$$EPSG) AS line, a.hausnummer
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, 
( 
 SELECT  a.a_ogc_fid, a.b_ogc_fid, a.min 
 FROM $$DBSCHEMA.t_distanz_gebaeudeeingang_lokalisationsnamepos a, 
  ( 
    SELECT t_distanz_gebaeudeeingang_lokalisationsnamepos.a_ogc_fid, min(t_distanz_gebaeudeeingang_lokalisationsnamepos.min) AS min
    FROM $$DBSCHEMA.t_distanz_gebaeudeeingang_lokalisationsnamepos 
    GROUP BY t_distanz_gebaeudeeingang_lokalisationsnamepos.a_ogc_fid
  ) b 
 WHERE a.min = b.min 
 AND a.a_ogc_fid = b.a_ogc_fid
) b, 
$$DBSCHEMA.t_gebaeudeadressen_lokalisationsnamepos c 
WHERE b.a_ogc_fid = a.ogc_fid 
AND b.b_ogc_fid = c.ogc_fid;

ALTER TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz ADD PRIMARY KEY (ogc_fid);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeudeadressen_spinnennetz TO $$USER;',15,'Spinnennetz: LokalisationsnamePos - Gebäudeeingang',NULL,1),
 (6,'CREATE TABLE $$DBSCHEMA.t_topics_tables AS

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

GRANT SELECT ON TABLE $$DBSCHEMA.t_topics_tables TO $$USER;',11,'This is for the topics-table-loader. No language support.',NULL,1),
 (7,'CREATE TABLE $$DBSCHEMA.t_lfp3_ausserhalb_gemeinde AS
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
GRANT SELECT ON TABLE $$DBSCHEMA.t_lfp3_ausserhalb_gemeinde TO $$USER;',20,'LFP3 outside municipality.',NULL,1),
 (8,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_flaechenelement AS
SELECT b.*, a.art, a.ogc_fid as eo_ogc_fid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_flaechenelement as b
WHERE b.flaechenelement_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_flaechenelement TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_linienelement AS
SELECT b.*, a.art, a.ogc_fid as eo_ogc_fid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_linienelement as b
WHERE b.linienelement_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_linienelement TO $$USER;

CREATE OR REPLACE VIEW $$DBSCHEMA.v_einzelobjekte_punktelement AS
SELECT b.*, a.art, a.ogc_fid as eo_ogc_fid
FROM $$DBSCHEMA.einzelobjekte_einzelobjekt as a, $$DBSCHEMA.einzelobjekte_punktelement as b
WHERE b.punktelement_von = a.ogc_fid;

GRANT SELECT ON TABLE $$DBSCHEMA.v_einzelobjekte_punktelement TO $$USER;',30,'View for Einzelobjekte.',NULL,1),
 (9,'CREATE OR REPLACE VIEW $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos AS 
SELECT b.ogc_fid, b.t_ili_tid, b.hausnummerpos_von, b.pos, b.ori, b.hali, b.vali, b.groesse, ST_X(b.pos) AS y, ST_Y(b.pos) AS x, (100::double precision - b.ori) * 0.9::double precision AS rot, a.hausnummer, a.gebaeudeeingang_von as lok_tid
FROM $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang a, $$DBSCHEMA.gebaeudeadressen_hausnummerpos b
WHERE a.ogc_fid = b.hausnummerpos_von;

GRANT SELECT ON TABLE $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos TO $$USER;',16,'View: Join of HausnummerPos and Gebaeudeeingang.',NULL,1),
 (10,'CREATE TABLE $$DBSCHEMA.t_shortestline_hausnummerpos AS 
SELECT a.ogc_fid, d."atext" as strnam, b.hausnummer, a.ogc_fid as a_tid, b.ogc_fid as b_tid, 
       b.gebaeudeeingang_von as lok_tid, ST_ShortestLine(a.pos, c.geometrie)::geometry(LineString,$$EPSG) as the_geom
FROM $$DBSCHEMA.v_gebaeudeadressen_hausnummerpos as a, 
     $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang as b,
     (
       SELECT ST_Union(geometrie) as geometrie, strassenstueck_von
       FROM $$DBSCHEMA.gebaeudeadressen_strassenstueck
       GROUP BY strassenstueck_von
     ) as c,
     $$DBSCHEMA.gebaeudeadressen_lokalisationsname as d
WHERE a.hausnummerpos_von = b.ogc_fid
AND b.gebaeudeeingang_von = c.strassenstueck_von
AND d.benannte = b.gebaeudeeingang_von;

ALTER TABLE $$DBSCHEMA.t_shortestline_hausnummerpos ADD PRIMARY KEY (ogc_fid);
GRANT SELECT ON TABLE $$DBSCHEMA.t_shortestline_hausnummerpos TO $$USER;',16,'Table: Shortestline from HausnummerPos to axis.',NULL,1),
 (11,'CREATE TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang AS 
SELECT c.ogc_fid, c.entstehung, c.geometrie::geometry(Polygon,$$EPSG), ST_Area(c.geometrie) as flaeche, c.qualitaet, c.art
FROM 
(
 SELECT bodenbedeckung_boflaeche.ogc_fid, bodenbedeckung_boflaeche.entstehung, 
        bodenbedeckung_boflaeche.geometrie, bodenbedeckung_boflaeche.qualitaet, bodenbedeckung_boflaeche.art
 FROM $$DBSCHEMA.bodenbedeckung_boflaeche
 WHERE bodenbedeckung_boflaeche.art = ''Gebaeude'' 
 AND ST_Area(bodenbedeckung_boflaeche.geometrie) > 12::double precision

EXCEPT 

 SELECT DISTINCT ON (a.ogc_fid) a.ogc_fid, a.entstehung, a.geometrie, a.qualitaet, 
        a.art
 FROM $$DBSCHEMA.bodenbedeckung_boflaeche a, $$DBSCHEMA.gebaeudeadressen_gebaeudeeingang b
 WHERE a.art = ''Gebaeude'' AND ST_Area(a.geometrie) > 12::double precision 
 AND a.geometrie && b.lage 
 AND ST_Distance(a.geometrie, b.lage) = 0::double precision
) as c;

ALTER TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang ADD PRIMARY KEY (ogc_fid);
GRANT SELECT ON TABLE $$DBSCHEMA.t_gebaeude_groesser_12m2_ohne_eingang TO $$USER;',16,'Table: Houses bigger than 12m2 without an entry.',NULL,1),
 (12,'CREATE TABLE $$DBSCHEMA.t_topics_tables AS

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
