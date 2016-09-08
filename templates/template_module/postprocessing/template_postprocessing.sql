CREATE TABLE postprocessing
(
	ogc_fid INTEGER PRIMARY KEY NOT NULL,
	sql_query TEXT,
	comment TEXT
);

-- Describe POSTPROCESSING
CREATE TABLE postprocessing (
    "ogc_fid" INTEGER PRIMARY KEY NOT NULL,
    "sql_query" TEXT,
    "order" INTEGER,
    "comment" TEXT,
    "lang" TEXT
, "apply" INTEGER   DEFAULT (1))
