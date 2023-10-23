-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    doc integer NOT NULL,
    cat_id integer NOT NULL,
    text text COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    date date NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Documents_pkey" PRIMARY KEY (doc),
    CONSTRAINT "Documents_Cat_ID_fkey" FOREIGN KEY (cat_id)
        REFERENCES public.category (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;