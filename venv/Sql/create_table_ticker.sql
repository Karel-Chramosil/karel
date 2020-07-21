create table ticker
(
    ask           numeric(8, 2),
    askvolume     numeric(12, 6),
    average       numeric(12, 6),
    basevolume    numeric(13, 6),
    bid           numeric(12, 6),
    bidvolume     numeric(13, 6),
    change        numeric(8, 2),
    close         numeric(8, 2),
    datetime      timestamp not null,
    high          numeric(7, 1),
    last          numeric(8, 2),
    low           numeric(8, 2),
    open          numeric(8, 2),
    percentage    numeric(7, 3),
    previousclose numeric(8, 2),
    quotevolume   numeric(19, 8),
    symbol        varchar(100),
    timestamp     bigint    not null
        constraint ticker_pkey
            primary key,
    vwap          numeric(14, 8)
);

alter table ticker
    owner to root;

   
