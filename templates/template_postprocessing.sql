CREATE TABLE postprocessing
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT,
	comment TEXT
);


CREATE TABLE tables
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);

CREATE TABLE views
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);

CREATE TABLE inserts
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);

-- unnoetig?
CREATE TABLE updates
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT
);
