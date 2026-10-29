# Ticker verification

Requests sent through desk_core: 8.
A series shorter than five years, or covering under 80% of weekdays between its first and last print, is flagged and kept.
Weekdays are the denominator, so ordinary exchange holidays are not holes.

## Series

| ticker | field | name | currency | status | detail | n | first | last | years | weekday_coverage | flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CESIUSD Index | PX_LAST |  |  | empty |  | 0 |  |  |  |  | empty |
| IBOV Index | PX_LAST |  |  | empty |  | 0 |  |  |  |  | empty |
| LF98OAS Index | PX_LAST |  |  | empty |  | 0 |  |  |  |  | empty |
| CPI CHNG Index | BN_SURVEY_MEDIAN | US CPI Urban Consumers MoM SA |  | monthly |  | 259 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| CPI CHNG Index | PX_LAST | US CPI Urban Consumers MoM SA |  | monthly |  | 259 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| CPI YOY Index | BN_SURVEY_MEDIAN | US CPI Urban Consumers YoY NSA |  | monthly |  | 260 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| CPI YOY Index | PX_LAST | US CPI Urban Consumers YoY NSA |  | monthly |  | 260 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| NFP TCH Index | BN_SURVEY_MEDIAN | US Employees on Nonfarm Payrol |  | monthly |  | 261 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| NFP TCH Index | PX_LAST | US Employees on Nonfarm Payrol |  | monthly |  | 261 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| AS51 Index | PX_LAST | S&P/ASX 200 INDEX | AUD | ok |  | 5524 | 2005-01-04 | 2026-10-29 | 21.82 | 0.97 |  |
| AS51 Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P/ASX 200 INDEX | AUD | ok |  | 5524 | 2005-01-04 | 2026-10-29 | 21.82 | 0.97 |  |
| AS51T Index | PX_LAST | SP ASX 200 TR | AUD | ok |  | 5524 | 2005-01-04 | 2026-10-29 | 21.82 | 0.97 |  |
| ASA51 Index | PX_LAST | SP ASX 200 TR | AUD | ok |  | 5524 | 2005-01-04 | 2026-10-29 | 21.82 | 0.97 | probe |
| AUDUSD Curncy | PX_LAST | AUD-USD X-RATE | USD | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| CL1 Comdty | PX_LAST | Generic 1st 'CL' Future | USD | ok |  | 5498 | 2005-01-03 | 2026-10-29 | 21.82 | 0.966 |  |
| DAX Index | PX_LAST | DAX INDEX | EUR | ok |  | 5546 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| DAX Index | TOT_RETURN_INDEX_GROSS_DVDS | DAX INDEX | EUR | ok |  | 5546 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| DAXK Index | PX_LAST | DAX PRICE INDEX | EUR | ok |  | 5548 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| DJTTR Index | PX_LAST | DJ TransAvgTR | USD | ok |  | 5548 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| DJUSHB Index | PX_LAST | DJ US TOT MKT HME CONST | USD | ok |  | 5504 | 2005-01-03 | 2026-10-29 | 21.82 | 0.967 |  |
| DJUSHB Index | TOT_RETURN_INDEX_GROSS_DVDS | DJ US TOT MKT HME CONST | USD | ok |  | 5504 | 2005-01-03 | 2026-10-29 | 21.82 | 0.967 |  |
| DJUTR Index | PX_LAST | DJ UtilityAvgTR | USD | ok |  | 5548 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| DXY Curncy | PX_LAST | DOLLAR INDEX SPOT | USD | ok |  | 5674 | 2005-01-03 | 2026-10-29 | 21.82 | 0.996 |  |
| EURUSD Curncy | PX_LAST | EUR-USD X-RATE | USD | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| EWZ US Equity | PX_LAST | ISHARES MSCI BRAZIL ETF | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| EWZ US Equity | TOT_RETURN_INDEX_GROSS_DVDS | ISHARES MSCI BRAZIL ETF | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| FTSEMIB Index | PX_LAST | FTSE MIB INDEX | EUR | ok |  | 5544 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| FTSEMIB Index | TOT_RETURN_INDEX_GROSS_DVDS | FTSE MIB INDEX | EUR | ok |  | 5544 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| FTSEMIBN Index | PX_LAST | FTSE MIB Net TR | EUR | ok |  | 4506 | 2009-02-23 | 2026-10-29 | 17.68 | 0.977 |  |
| GBPUSD Curncy | PX_LAST | GBP-USD X-RATE | USD | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| GDBR10 Index | PX_LAST | GERMANY GOVT BND 10 YR DBR | EUR | ok |  | 5685 | 2005-01-03 | 2026-10-29 | 21.82 | 0.998 |  |
| GJGB10 Index | PX_LAST | Japan Govt 10Y Simple Yield | JPY | ok |  | 5684 | 2005-01-03 | 2026-10-29 | 21.82 | 0.998 |  |
| HG1 Comdty | PX_LAST | Generic 1st 'HG' Future | USD | ok |  | 5498 | 2005-01-03 | 2026-10-29 | 21.82 | 0.966 |  |
| HSCEI Index | PX_LAST | HANG SENG CHINA ENT INDX | HKD | ok |  | 5376 | 2005-01-03 | 2026-10-29 | 21.82 | 0.944 |  |
| HSCEI Index | TOT_RETURN_INDEX_GROSS_DVDS | HANG SENG CHINA ENT INDX | HKD | ok |  | 5376 | 2005-01-03 | 2026-10-29 | 21.82 | 0.944 |  |
| KRE US Equity | PX_LAST | SS SPDR S&P REGIONAL BANK | USD | ok |  | 5121 | 2006-06-22 | 2026-10-29 | 20.35 | 0.964 |  |
| KRE US Equity | TOT_RETURN_INDEX_GROSS_DVDS | SS SPDR S&P REGIONAL BANK | USD | ok |  | 5121 | 2006-06-22 | 2026-10-29 | 20.35 | 0.964 |  |
| KRX Index | PX_LAST | KBW REGIONAL BANKING INX | USD | ok |  | 5570 | 2005-01-03 | 2026-10-29 | 21.82 | 0.978 |  |
| KRX Index | TOT_RETURN_INDEX_GROSS_DVDS | KBW REGIONAL BANKING INX | USD | ok |  | 5570 | 2005-01-03 | 2026-10-29 | 21.82 | 0.978 |  |
| KRXTR Index | PX_LAST | KBWRegionalBnkTR | USD | ok |  | 5570 | 2005-01-03 | 2026-10-29 | 21.82 | 0.978 |  |
| MCX Index | PX_LAST | FTSE 250 INDEX | GBP | ok |  | 5515 | 2005-01-04 | 2026-10-29 | 21.82 | 0.969 |  |
| MCX Index | TOT_RETURN_INDEX_GROSS_DVDS | FTSE 250 INDEX | GBP | ok |  | 5515 | 2005-01-04 | 2026-10-29 | 21.82 | 0.969 |  |
| MCXNUK Index | PX_LAST | FTSE 250 Net Dvd TR Ix | GBP | ok |  | 4063 | 2010-12-31 | 2026-10-29 | 15.83 | 0.984 | probe |
| MDAX Index | PX_LAST | MDAX PERF INDEX | EUR | ok |  | 5547 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| MDAX Index | TOT_RETURN_INDEX_GROSS_DVDS | MDAX PERF INDEX | EUR | ok |  | 5547 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| MXEF Index | PX_LAST | MSCI EM | USD | ok |  | 5693 | 2005-01-03 | 2026-10-28 | 21.82 | 1.0 |  |
| MXEF Index | TOT_RETURN_INDEX_GROSS_DVDS | MSCI EM | USD | ok |  | 5693 | 2005-01-03 | 2026-10-28 | 21.82 | 1.0 |  |
| NDUEEGF Index | PX_LAST | MSCI Daily TR Net Emergi | USD | ok |  | 5693 | 2005-01-03 | 2026-10-28 | 21.82 | 1.0 |  |
| NDX Index | PX_LAST | NASDAQ 100 STOCK INDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| NDX Index | TOT_RETURN_INDEX_GROSS_DVDS | NASDAQ 100 STOCK INDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| NKY Index | PX_LAST | NIKKEI 225 | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| NKY Index | TOT_RETURN_INDEX_GROSS_DVDS | NIKKEI 225 | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| NKYTR Index | PX_LAST | Nikkei Total Return Idx | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| RSP US Equity | PX_LAST | INVESCO S&P 500 EQUAL WEIGHT | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| RSP US Equity | TOT_RETURN_INDEX_GROSS_DVDS | INVESCO S&P 500 EQUAL WEIGHT | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| RTY Index | PX_LAST | RUSSELL 2000 INDEX | USD | ok |  | 5493 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| RTY Index | TOT_RETURN_INDEX_GROSS_DVDS | RUSSELL 2000 INDEX | USD | ok |  | 5493 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| RUTTR Index | PX_LAST | Russ 2000 TR | USD | ok |  | 5493 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| S5COND Index | PX_LAST | S&P 500 CONS DISCRET IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5COND Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 CONS DISCRET IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5CONS Index | PX_LAST | S&P 500 CONS STAPLES IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5CONS Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 CONS STAPLES IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5ENRS Index | PX_LAST | S&P 500 ENERGY INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5ENRS Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 ENERGY INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5FINL Index | PX_LAST | S&P 500 FINANCIALS INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5FINL Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 FINANCIALS INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5INDU Index | PX_LAST | S&P 500 INDUSTRIALS IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5INDU Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 INDUSTRIALS IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5MATR Index | PX_LAST | S&P 500 MATERIALS INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5MATR Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 MATERIALS INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5UTIL Index | PX_LAST | S&P 500 UTILITIES INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5UTIL Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 UTILITIES INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SMI Index | PX_LAST | SWISS MARKET INDEX | CHF | ok |  | 5486 | 2005-01-03 | 2026-10-29 | 21.82 | 0.963 |  |
| SMI Index | TOT_RETURN_INDEX_GROSS_DVDS | SWISS MARKET INDEX | CHF | ok |  | 5486 | 2005-01-03 | 2026-10-29 | 21.82 | 0.963 |  |
| SMIC Index | PX_LAST | SMI GROSS TOTAL RETURN | CHF | ok |  | 5486 | 2005-01-03 | 2026-10-29 | 21.82 | 0.963 |  |
| SMIN Index | PX_LAST | SMI NR | CHF | ok |  | 4229 | 2010-01-04 | 2026-10-29 | 16.82 | 0.964 | probe |
| SOX Index | PX_LAST | PHILA SEMICONDUCTOR INDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SOX Index | TOT_RETURN_INDEX_GROSS_DVDS | PHILA SEMICONDUCTOR INDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPTR Index | PX_LAST | S&P 500 TR 4 JAN 1988 | USD | ok |  | 5490 | 2005-01-03 | 2026-10-28 | 21.82 | 0.964 |  |
| SPX Index | PX_LAST | S&P 500 INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPX Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P 500 INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPXEWI Index | PX_LAST | S&P EQUAL WEIGHT INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPXEWI Index | TOT_RETURN_INDEX_GROSS_DVDS | S&P EQUAL WEIGHT INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SX5E Index | PX_LAST | Euro Stoxx 50 Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX5E Index | TOT_RETURN_INDEX_GROSS_DVDS | Euro Stoxx 50 Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX5GT Index | PX_LAST | ESTX 50 (EUR) GRt | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX5T Index | PX_LAST | ESTX 50 (EUR) NRt | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 | probe |
| SX6P Index | PX_LAST | STXE 600 Utilities EUR | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX6P Index | TOT_RETURN_INDEX_GROSS_DVDS | STXE 600 Utilities EUR | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX6R Index | PX_LAST | STXE 600 Util (EUR) NRt | EUR | ok |  | 5599 | 2005-01-03 | 2026-10-29 | 21.82 | 0.983 |  |
| SX7E Index | PX_LAST | ESTX Banks (EUR) Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX7E Index | TOT_RETURN_INDEX_GROSS_DVDS | ESTX Banks (EUR) Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX7T Index | PX_LAST | ESTX Bnk (EUR) NRt | EUR | ok |  | 5598 | 2005-01-03 | 2026-10-29 | 21.82 | 0.983 |  |
| SXPP Index | PX_LAST | STXE 600 BasicResou EUR | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SXPP Index | TOT_RETURN_INDEX_GROSS_DVDS | STXE 600 BasicResou EUR | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SXPR Index | PX_LAST | STXE 600 BsRs (EUR) NRt | EUR | ok |  | 5599 | 2005-01-03 | 2026-10-29 | 21.82 | 0.983 |  |
| SXXP Index | PX_LAST | STXE 600 (EUR) Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SXXP Index | TOT_RETURN_INDEX_GROSS_DVDS | STXE 600 (EUR) Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SXXR Index | PX_LAST | STXE 600 (EUR) NRt | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| TMCXG Index | PX_LAST | FTSE 250 TR Index | GBP | ok |  | 5526 | 2005-01-04 | 2026-10-29 | 21.82 | 0.971 |  |
| TP17BNK Index | PX_LAST | TPX-17 Banks Index | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 | probe |
| TPNBNK Index | PX_LAST | TOPIX BANKS INDEX | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPNBNK Index | TOT_RETURN_INDEX_GROSS_DVDS | TOPIX BANKS INDEX | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPX Index | PX_LAST | TOPIX INDEX (TOKYO) | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPX Index | TOT_RETURN_INDEX_GROSS_DVDS | TOPIX INDEX (TOKYO) | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPXDDVD Index | PX_LAST | TOPIX TR Index | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPXNTR Index | PX_LAST | TOPIX Net Total Return | JPY | ok |  | 3213 | 2013-09-02 | 2026-10-29 | 13.16 | 0.936 | probe |
| TRAN Index | PX_LAST | DOW JONES TRANS. AVG | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| TRAN Index | TOT_RETURN_INDEX_GROSS_DVDS | DOW JONES TRANS. AVG | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| TUKXG Index | PX_LAST | FTSE 100 TR GBP | GBP | ok |  | 5579 | 2005-01-04 | 2026-10-29 | 21.82 | 0.98 |  |
| UKX Index | PX_LAST | FTSE 100 INDEX | GBP | ok |  | 5515 | 2005-01-04 | 2026-10-29 | 21.82 | 0.969 |  |
| UKX Index | TOT_RETURN_INDEX_GROSS_DVDS | FTSE 100 INDEX | GBP | ok |  | 5515 | 2005-01-04 | 2026-10-29 | 21.82 | 0.969 |  |
| UKXNUK Index | PX_LAST | FTSE 100 Net Tax Index | GBP | ok |  | 5538 | 2005-01-04 | 2026-10-29 | 21.82 | 0.973 | probe |
| USDBRL Curncy | PX_LAST | USD-BRL X-RATE | BRL | ok |  | 5504 | 2005-01-03 | 2026-10-29 | 21.82 | 0.967 |  |
| USDCHF Curncy | PX_LAST | USD-CHF X-RATE | CHF | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| USDHKD Curncy | PX_LAST | USD-HKD X-RATE | HKD | ok |  | 5692 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| USDJPY Curncy | PX_LAST | USD-JPY X-RATE | JPY | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| USGG10YR Index | PX_LAST | US Generic Govt 10 Yr | USD | ok |  | 5690 | 2005-01-03 | 2026-10-29 | 21.82 | 0.999 |  |
| USGG2YR Index | PX_LAST | US Generic Govt 2 Yr | USD | ok |  | 5690 | 2005-01-03 | 2026-10-29 | 21.82 | 0.999 |  |
| USGGBE10 Index | PX_LAST | US Breakeven 10 Year | USD | ok |  | 5686 | 2005-01-03 | 2026-10-29 | 21.82 | 0.999 |  |
| USGGT10Y Index | PX_LAST | US Generic Govt TII 10 Yr | USD | ok |  | 5688 | 2005-01-03 | 2026-10-29 | 21.82 | 0.999 |  |
| UTIL Index | PX_LAST | DOW JONES UTILITY AVG | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| UTIL Index | TOT_RETURN_INDEX_GROSS_DVDS | DOW JONES UTILITY AVG | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| VIX Index | PX_LAST | Cboe Volatility Index | USD | ok |  | 5524 | 2005-01-03 | 2026-10-29 | 21.82 | 0.97 |  |
| VNKY Index | PX_LAST | NIKKEI Volatility Index | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| XHB US Equity | PX_LAST | SS SPDR S&P HOMEBLDRS ETF | USD | ok |  | 5216 | 2006-02-06 | 2026-10-29 | 20.73 | 0.964 |  |
| XHB US Equity | TOT_RETURN_INDEX_GROSS_DVDS | SS SPDR S&P HOMEBLDRS ETF | USD | ok |  | 5216 | 2006-02-06 | 2026-10-29 | 20.73 | 0.964 |  |
| XNDX Index | PX_LAST | NASDAQ 100 TOTAL RETURN | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| XSOX Index | PX_LAST | PHLX SmCondtr Sec TR | USD | ok |  | 4239 | 2009-12-22 | 2026-10-29 | 16.85 | 0.964 |  |
| VOLQ Index | PX_LAST | NDX Volatility | USD | stale |  | 2453 | 2014-01-02 | 2023-09-29 | 9.74 | 0.965 | probe,stale |

## Spreads

| id | alignment | rows | built | empty_legs | bases | tr_vs_price | warning |
| --- | --- | --- | --- | --- | --- | --- | --- |
| us_cyc_def | native | 5490 | True |  | S5INDU Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5MATR Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5CONS Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5UTIL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | S5INDU Index:55.2%, S5MATR Index:58.0%, S5CONS Index:80.7%, S5UTIL Index:118.3% |  |
| rty_spx | native | 5498 | True |  | RTY Index=total_return_gross/RUTTR Index, SPX Index=total_return_gross/SPTR Index | RTY Index:34.0%, SPX Index:51.6% |  |
| spw_spx | native | 5491 | True |  | SPXEWI Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | SPXEWI Index:37.5%, SPX Index:51.6% |  |
| rsp_spx | native | 5490 | True |  | RSP US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | RSP US Equity:40.9%, SPX Index:51.6% | instrument_mismatch: etf, index |
| ndx_spx | native | 5490 | True |  | NDX Index=total_return_gross/XNDX Index, SPX Index=total_return_gross/SPTR Index | NDX Index:21.3%, SPX Index:51.6% |  |
| s5finl_s5util | native | 5490 | True |  | S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5UTIL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | S5FINL Index:55.8%, S5UTIL Index:118.3% |  |
| kre_s5finl | native | 5490 | True |  | KRE US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | KRE US Equity:63.5%, S5FINL Index:55.8% | instrument_mismatch: etf, index |
| krx_s5finl | native | 5569 | True |  | KRX Index=total_return_gross/KRXTR Index, S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | KRX Index:78.1%, S5FINL Index:55.8% |  |
| xhb_spx | native | 5490 | True |  | XHB US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | XHB US Equity:22.1%, SPX Index:51.6% | instrument_mismatch: etf, index |
| djushb_spx | native | 5503 | True |  | DJUSHB Index=price/price, SPX Index=total_return_gross/SPTR Index | DJUSHB Index:0.0%, SPX Index:51.6% | mixed_basis: price, total_return_gross |
| sox_spx | native | 5490 | True |  | SOX Index=total_return_gross/XSOX Index, SPX Index=total_return_gross/SPTR Index | SOX Index:53.6%, SPX Index:51.6% |  |
| s5enrs_s5cond | native | 5490 | True |  | S5ENRS Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5COND Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | S5ENRS Index:86.4%, S5COND Index:31.8% |  |
| tran_util | native | 5547 | True |  | TRAN Index=total_return_gross/DJTTR Index, UTIL Index=total_return_gross/DJUTR Index | TRAN Index:37.9%, UTIL Index:115.6% |  |
| sx7e_sx6p | native | 5598 | True |  | SX7E Index=total_return_net/SX7T Index, SX6P Index=total_return_net/SX6R Index | SX7E Index:106.7%, SX6P Index:137.2% |  |
| ftsemib_dax | native | 5571 | True |  | FTSEMIB Index=total_return_net/FTSEMIBN Index, DAX Index=total_return/price | FTSEMIB Index:234.9%, DAX Index:0.0% | mixed_basis: total_return, total_return_net |
| mdax_dax | native | 5546 | True |  | MDAX Index=total_return/price, DAX Index=total_return/price | MDAX Index:0.0%, DAX Index:0.0% |  |
| smi_sx5e | native | 5603 | True |  | SMI Index=total_return_gross/SMIC Index, SX5E Index=total_return_gross/SX5GT Index | SMI Index:93.8%, SX5E Index:119.4% |  |
| sxpp_sxxp | native | 5603 | True |  | SXPP Index=total_return_net/SXPR Index, SXXP Index=total_return_net/SXXR Index | SXPP Index:103.1%, SXXP Index:81.8% |  |
| tpx_nky | native | 5340 | True |  | TPX Index=total_return_gross/TPXDDVD Index, NKY Index=total_return_gross/NKYTR Index | TPX Index:57.6%, NKY Index:47.8% |  |
| tpxbnk_tpx | native | 5340 | True |  | TPNBNK Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, TPX Index=total_return_gross/TPXDDVD Index | TPNBNK Index:87.9%, TPX Index:57.6% |  |
| mcx_ukx | native | 5578 | True |  | MCX Index=total_return_gross/TMCXG Index, UKX Index=total_return_gross/TUKXG Index | MCX Index:84.1%, UKX Index:124.6% |  |
| mxef_spx | native | 5692 | True |  | MXEF Index=total_return_net/NDUEEGF Index, SPX Index=total_return_gross/SPTR Index | MXEF Index:68.3%, SPX Index:51.6% | mixed_basis: total_return_gross, total_return_net |
| hscei_spx | asia_to_us | 5489 | True |  | HSCEI Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | HSCEI Index:67.0%, SPX Index:51.6% |  |
| ibov_mxef | native | 5692 | False | IBOV Index | IBOV Index=price/price, MXEF Index=total_return_net/NDUEEGF Index | MXEF Index:68.3% | mixed_basis: price, total_return_net |
| ewz_mxef | native | 5693 | True |  | EWZ US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, MXEF Index=total_return_net/NDUEEGF Index | EWZ US Equity:134.7%, MXEF Index:68.3% | mixed_basis: total_return_gross, total_return_net; instrument_mismatch: etf, index |
| as51_spx | asia_to_us | 5489 | True |  | AS51 Index=total_return_gross/AS51T Index, SPX Index=total_return_gross/SPTR Index | AS51 Index:147.5%, SPX Index:51.6% |  |

## Probes that did not resolve

BOVA11 BZ Equity, CESIUSD Index, IBOV Index, PETR4 BZ Equity, RVX Index, IBOVESPA Index, LF98OAS Index, LF98TRUU Index, SPW Index, SPXEW Index, SPXEWTR Index, SPHOME Index, SPSIHOTR Index, SPSIRBK Index, SPSIRBKT Index, V2X Index, VSTOXX Index, VXN Index
