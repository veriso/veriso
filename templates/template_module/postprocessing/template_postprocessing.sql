BEGIN TRANSACTION;
CREATE TABLE postprocessing (
    "ogc_fid" INTEGER PRIMARY KEY NOT NULL,
    "sql_query" TEXT,
    "order" INTEGER,
    "comment" TEXT,
    "lang" TEXT
, "apply" INTEGER   DEFAULT (1));
INSERT INTO `postprocessing` (ogc_fid,sql_query,order,comment,lang,apply) VALUES (1,'CREATE TABLE $$DBSCHEMA.t_topics_tables AS

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
