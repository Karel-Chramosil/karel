create table info
(
    askprice           numeric(14, 8),
    askqty             numeric(14, 8),
    bidprice           numeric(14, 8),
    bidqty             numeric(14, 8),
    closetime          bigint not null
        constraint info_pkey
            primary key,
    count              bigint,
    firstid            bigint,
    highprice          numeric(14, 8),
    lastid             bigint,
    lastprice          numeric(14, 8),
    lastqty            numeric(14, 8),
    lowprice           numeric(14, 8),
    openprice          numeric(14, 8),
    opentime           bigint,
    prevcloseprice     numeric(14, 8),
    pricechange        numeric(14, 8),
    pricechangepercent numeric(7, 3),
    quotevolume        numeric(20, 8),
    symbol             varchar(100),
    volume             numeric(14, 8),
    weightedavgprice   numeric(14, 8)
);

alter table info
    owner to root;

   



