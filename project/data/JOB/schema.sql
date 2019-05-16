(col1 int COMMENT CREA'TE TABLE aka_name (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'person_id integer NOT NULL,
(col1 int COMMENT     'name text NOT NULL,
(col1 int COMMENT     'imdb_index character varying(12),
(col1 int COMMENT     'name_pcode_cf character varying(5),
(col1 int COMMENT     'name_pcode_nf character varying(5),
(col1 int COMMENT     'surname_pcode character varying(5),
(col1 int COMMENT     'md5sum character varying(32)
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE aka_title (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'title text NOT NULL,
(col1 int COMMENT     'imdb_index character varying(12),
(col1 int COMMENT     'kind_id integer NOT NULL,
(col1 int COMMENT     'production_year integer,
(col1 int COMMENT     'phonetic_code character varying(5),
(col1 int COMMENT     'episode_of_id integer,
(col1 int COMMENT     'season_nr integer,
(col1 int COMMENT     'episode_nr integer,
(col1 int COMMENT     'note text,
(col1 int COMMENT     'md5sum character varying(32)
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE cast_info (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'person_id integer NOT NULL,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'person_role_id integer,
(col1 int COMMENT     'note text,
(col1 int COMMENT     'nr_order integer,
(col1 int COMMENT     'role_id integer NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE char_name (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'name text NOT NULL,
(col1 int COMMENT     'imdb_index character varying(12),
(col1 int COMMENT     'imdb_id integer,
(col1 int COMMENT     'name_pcode_nf character varying(5),
(col1 int COMMENT     'surname_pcode character varying(5),
(col1 int COMMENT     'md5sum character varying(32)
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE comp_cast_type (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'kind character varying(32) NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE company_name (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'name text NOT NULL,
(col1 int COMMENT     'country_code character varying(255),
(col1 int COMMENT     'imdb_id integer,
(col1 int COMMENT     'name_pcode_nf character varying(5),
(col1 int COMMENT     'name_pcode_sf character varying(5),
(col1 int COMMENT     'md5sum character varying(32)
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE company_type (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'kind character varying(32) NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE complete_cast (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer,
(col1 int COMMENT     'subject_id integer NOT NULL,
(col1 int COMMENT     'status_id integer NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE info_type (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'info character varying(32) NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE keyword (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'keyword text NOT NULL,
(col1 int COMMENT     'phonetic_code character varying(5)
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE kind_type (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'kind character varying(15) NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE link_type (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'link character varying(32) NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE movie_companies (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'company_id integer NOT NULL,
(col1 int COMMENT     'company_type_id integer NOT NULL,
(col1 int COMMENT     'note text
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE movie_info (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'info_type_id integer NOT NULL,
(col1 int COMMENT     'info text NOT NULL,
(col1 int COMMENT     'note text
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE movie_info_idx (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'info_type_id integer NOT NULL,
(col1 int COMMENT     'info text NOT NULL,
(col1 int COMMENT     'note text
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE movie_keyword (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'keyword_id integer NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE movie_link (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'movie_id integer NOT NULL,
(col1 int COMMENT     'linked_movie_id integer NOT NULL,
(col1 int COMMENT     'link_type_id integer NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE name (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'name text NOT NULL,
(col1 int COMMENT     'imdb_index character varying(12),
(col1 int COMMENT     'imdb_id integer,
(col1 int COMMENT     'gender character varying(1),
(col1 int COMMENT     'name_pcode_cf character varying(5),
(col1 int COMMENT     'name_pcode_nf character varying(5),
(col1 int COMMENT     'surname_pcode character varying(5),
(col1 int COMMENT     'md5sum character varying(32)
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE person_info (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'person_id integer NOT NULL,
(col1 int COMMENT     'info_type_id integer NOT NULL,
(col1 int COMMENT     'info text NOT NULL,
(col1 int COMMENT     'note text
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE role_type (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'role character varying(32) NOT NULL
(col1 int COMMENT );co'l1 int COMMENT (

(col1 int COMMENT CR'EA'TE TABLE title (
(col1 int COMMENT     'id integer NOT NULL PRIMARY KEY,
(col1 int COMMENT     'title text NOT NULL,
(col1 int COMMENT     'imdb_index character varying(12),
(col1 int COMMENT     'kind_id integer NOT NULL,
(col1 int COMMENT     'production_year integer,
(col1 int COMMENT     'imdb_id integer,
(col1 int COMMENT     'phonetic_code character varying(5),
(col1 int COMMENT     'episode_of_id integer,
(col1 int COMMENT     'season_nr integer,
(col1 int COMMENT     'episode_nr integer,
(col1 int COMMENT     'series_years character varying(49),
(col1 int COMMENT     'md5sum character varying(32)
(col1 int COMMEN'T );
