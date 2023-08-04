-- DBInvoice.dbo.PrizeCity definition

-- Drop table

-- DROP TABLE DBInvoice.dbo.PrizeCity;

CREATE TABLE DBInvoice.dbo.PrizeCity (
	prizeNm nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	townCd varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	townNm nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	invoiceAwardTotalAmt int NULL,
	awardAmt int NULL,
	invoiceAwardTotalCnt int NULL,
	awardDate varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	yearNm varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	hsnCd varchar(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	prize varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	hsnNm nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	awardDateNm varchar(6) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);
 CREATE NONCLUSTERED INDEX idx_PrizeCity ON dbo.PrizeCity (  yearNm ASC  , hsnCd ASC  , prize ASC  , hsnNm ASC  , prizeNm ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
