create table crypt_exch
(
    id        varchar(100) not null
        constraint crypt_exch_pkey
            primary key,
    logo_img  bytea,
    uri       varchar(300),
    name      varchar(100)
        constraint crypt_exch_name_key
            unique,
    ver       numeric(3, 2),
    doc       varchar(10),
    uri_doc   varchar(300)
        constraint crypt_exch_uri_doc_key
            unique,
    certified boolean default false,
    pro       boolean default false
);

alter table crypt_exch
    owner to root;


