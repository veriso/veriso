drop table if exists tmp_postprocessing;
CREATE TABLE tmp_postprocessing (
	ogc_fid	INTEGER NOT NULL,
	sql_query	TEXT,
	`order`	INTEGER,
	comment	TEXT,
	lang	TEXT,
	apply INTEGER DEFAULT 1,
	PRIMARY KEY(ogc_fid)
);

insert into tmp_postprocessing (sql_query, `order`, comment, lang, apply)
select sql_query, 1, 'Was in table tables', lang, apply from tables;

insert into tmp_postprocessing (sql_query, `order`, comment, lang, apply)
select sql_query, 2, 'Was in table views', lang, apply from views;

insert into tmp_postprocessing (sql_query, `order`, comment, lang, apply)
select sql_query, 3, 'Was in table inserts', lang, apply from inserts;

insert into tmp_postprocessing (sql_query, `order`, comment, lang, apply)
select sql_query, 4, 'Was in table updates', lang, apply from updates;

insert into tmp_postprocessing (sql_query, `order`, comment, lang, apply)
select sql_query, 5, 'Was in table postprocessing', lang, apply from
	postprocessing;

drop table tables;
drop table views;
drop table inserts;
drop table updates;
drop table postprocessing;
ALTER TABLE tmp_postprocessing RENAME TO postprocessing
