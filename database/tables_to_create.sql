--  Create Table books_issued

CREATE TABLE IF NOT EXISTS public.books_issued
(
    id integer NOT NULL,
    member_no character varying(50) COLLATE pg_catalog."default",
    book_title character varying(100) COLLATE pg_catalog."default",
    author character varying(50) COLLATE pg_catalog."default",
    issue_date timestamp without time zone,
    return_date timestamp without time zone,
    CONSTRAINT books_issued_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.books_issued
    OWNER to postgres;
	
-- Create Sequence for primary key id

CREATE SEQUENCE IF NOT EXISTS public.books_issued_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1
    OWNED BY books_issued.id;

ALTER SEQUENCE public.books_issued_id_seq
    OWNER TO postgres;
	
-- Add sequence to primary key column 

ALTER TABLE IF EXISTS public.books_issued
    ALTER COLUMN id SET DEFAULT  nextval('books_issued_id_seq'::regclass);