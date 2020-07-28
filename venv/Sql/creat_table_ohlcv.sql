create table ohlcv
(
    timestamp bigint not null
        constraint ohlcv_pkey
            primary key,
    open      numeric(8, 2),
    high      numeric(7, 1),
    low       numeric(8, 2),
    close     numeric(8, 2),
    volume    numeric(19, 6),
    future    numeric(8, 2),
    error     numeric(7, 4)
);

alter table ohlcv
    owner to root;
