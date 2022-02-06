# 1. country (https://support.microsoft.com/en-us/office/about-the-stocks-financial-data-sources-98a03e23-37f6-4776-beea-c5a6c8e787e6)
CREATE TABLE country (
	code VARCHAR(2) NOT NULL PRIMARY KEY COMMENT '국가코드',
	name VARCHAR(128) NOT NULL COMMENT '국호',
	market VARCHAR(128) NOT NULL COMMENT '시장'
) COMMENT '국가정보';


# 2. stock_info_kr
CREATE TABLE stock_info_kr (
	symbol VARCHAR(128) NOT NULL PRIMARY KEY COMMENT '종목코드',
	market VARCHAR(128) NOT NULL COMMENT '시장',
	name VARCHAR(128) NOT NULL COMMENT '이름',
	sector VARCHAR(128) COMMENT '업종',
	industry VARCHAR(128) COMMENT '산업그룹',
	listingdate VARCHAR(128) COMMENT '조회날짜',
	settlemonth VARCHAR(128) COMMENT '결산월',
	representative VARCHAR(128) COMMENT '대표자',
	homepage VARCHAR(128) COMMENT '홈페이지',
	region VARCHAR(128) COMMENT '지역',
	update_date VARCHAR(128) COMMENT '최신화 날짜'
) COMMENT '한국(KRX)에 상장된 종목들의 정보'
CHARACTER SET utf8mb4 COLLATE UTF8MB4_UNICODE_CI;


# 3. stock_daily_kr
CREATE TABLE stock_daily_kr (
	date DATE NOT NULL COMMENT '날짜',
	symbol VARCHAR(128)	not NULL COMMENT '종목코드',
	open float NOT NULL COMMENT '시가',
	high float NOT NULL COMMENT '고가',
	low float NOT NULL COMMENT '저가',
	close float NOT NULL COMMENT '종가',
	volume float NOT NULL COMMENT '거래량',
	`return` FLOAT COMMENT '종가 수익률',
	cap float comment '시가총액',
	trading_value float comment '거래대금',
    num_shares float comment '상장주식수',

	PRIMARY KEY (date, symbol),
	FOREIGN KEY (symbol) REFERENCES stock_info_kr(symbol) ON UPDATE CASCADE ON DELETE CASCADE
) COMMENT '한국(KRX)에 상장된 종목들의 일데이터'
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 4. index_daily_kr
CREATE TABLE index_daily_kr (
	date DATE NOT NULL COMMENT '날짜',
	symbol VARCHAR(128)	not NULL COMMENT '종목코드',
	open float NOT NULL COMMENT '시가',
	high float NOT NULL COMMENT '고가',
	low float NOT NULL COMMENT '저가',
	close float NOT NULL COMMENT '종가',
	volume float NOT NULL COMMENT '거래량',
	`return` FLOAT COMMENT '종가 수익률',

	PRIMARY KEY (date, symbol)
) COMMENT '한국 대표 지수들의 일데이터'
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
