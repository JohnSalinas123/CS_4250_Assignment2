-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    doc_id integer NOT NULL,
    term text COLLATE pg_catalog."default" NOT NULL,
    count integer NOT NULL,
    CONSTRAINT "Index_pkey" PRIMARY KEY (doc_id, term),
    CONSTRAINT "Doc_FK" FOREIGN KEY (doc_id)
        REFERENCES public.documents (doc) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Term_FK" FOREIGN KEY (term)
        REFERENCES public.term (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;