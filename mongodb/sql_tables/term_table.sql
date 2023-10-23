-- Table: public.term

-- DROP TABLE IF EXISTS public.term;

CREATE TABLE IF NOT EXISTS public.term
(
    term text COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    CONSTRAINT "Term_pkey" PRIMARY KEY (term)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.term
    OWNER to postgres;