# Ticker verification

Requests sent through desk_core: 160.
A series shorter than five years, or covering under 80% of weekdays between its first and last print, is flagged and kept.
Weekdays are the denominator, so ordinary exchange holidays are not holes.

## Series

| ticker | field | route | name | currency | status | detail | n | first | last | years | weekday_coverage | flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CPI CHNG Index | BN_SURVEY_MEDIAN | bpipe | US CPI Urban Consumers MoM SA |  | monthly |  | 259 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| CPI CHNG Index | PX_LAST | bpipe | US CPI Urban Consumers MoM SA |  | monthly |  | 259 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| CPI YOY Index | BN_SURVEY_MEDIAN | bpipe | US CPI Urban Consumers YoY NSA |  | monthly |  | 260 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| CPI YOY Index | PX_LAST | bpipe | US CPI Urban Consumers YoY NSA |  | monthly |  | 260 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| NFP TCH Index | BN_SURVEY_MEDIAN | bpipe | US Employees on Nonfarm Payrol |  | monthly |  | 261 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| NFP TCH Index | PX_LAST | bpipe | US Employees on Nonfarm Payrol |  | monthly |  | 261 | 2005-01-31 | 2026-09-30 | 21.66 | 0.046 | monthly |
| AS51 Index | PX_LAST | bpipe | S&P/ASX 200 INDEX | AUD | ok |  | 5525 | 2005-01-04 | 2026-10-30 | 21.82 | 0.97 |  |
| AS51 Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P/ASX 200 INDEX | AUD | ok |  | 5524 | 2005-01-04 | 2026-10-29 | 21.82 | 0.97 |  |
| AS51T Index | PX_LAST | bpipe | SP ASX 200 TR | AUD | ok |  | 5525 | 2005-01-04 | 2026-10-30 | 21.82 | 0.97 |  |
| ASA51 Index | PX_LAST | bpipe | SP ASX 200 TR | AUD | ok |  | 5525 | 2005-01-04 | 2026-10-30 | 21.82 | 0.97 | probe |
| AUDUSD Curncy | PX_LAST | bpipe | AUD-USD X-RATE | USD | ok |  | 5695 | 2005-01-03 | 2026-10-30 | 21.82 | 1.0 |  |
| BOVA11 BZ Equity | PX_LAST | terminal | ISHARES IBOVESPA | BRL | ok |  | 4440 | 2008-12-02 | 2026-10-30 | 17.91 | 0.95 | probe |
| CESIUSD Index | PX_LAST | terminal | CESIUSD | USD | ok |  | 5611 | 2005-01-03 | 2026-10-30 | 21.82 | 0.985 |  |
| CL1 Comdty | PX_LAST | bpipe | Generic 1st 'CL' Future | USD | ok |  | 5499 | 2005-01-03 | 2026-10-30 | 21.82 | 0.966 |  |
| DAX Index | PX_LAST | bpipe | DAX INDEX | EUR | ok |  | 5547 | 2005-01-03 | 2026-10-30 | 21.82 | 0.974 |  |
| DAX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | DAX INDEX | EUR | ok |  | 5546 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| DAXK Index | PX_LAST | bpipe | DAX PRICE INDEX | EUR | ok |  | 5549 | 2005-01-03 | 2026-10-30 | 21.82 | 0.974 |  |
| DJTTR Index | PX_LAST | bpipe | DJ TransAvgTR | USD | ok |  | 5549 | 2005-01-03 | 2026-10-30 | 21.82 | 0.974 |  |
| DJUSHB Index | PX_LAST | bpipe | DJ US TOT MKT HME CONST | USD | ok |  | 5505 | 2005-01-03 | 2026-10-30 | 21.82 | 0.967 |  |
| DJUSHB Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | DJ US TOT MKT HME CONST | USD | ok |  | 5504 | 2005-01-03 | 2026-10-29 | 21.82 | 0.967 |  |
| DJUTR Index | PX_LAST | bpipe | DJ UtilityAvgTR | USD | ok |  | 5549 | 2005-01-03 | 2026-10-30 | 21.82 | 0.974 |  |
| DXY Curncy | PX_LAST | bpipe | DOLLAR INDEX SPOT | USD | ok |  | 5675 | 2005-01-03 | 2026-10-30 | 21.82 | 0.996 |  |
| EURUSD Curncy | PX_LAST | bpipe | EUR-USD X-RATE | USD | ok |  | 5695 | 2005-01-03 | 2026-10-30 | 21.82 | 1.0 |  |
| EWZ US Equity | PX_LAST | bpipe | ISHARES MSCI BRAZIL ETF | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| EWZ US Equity | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | ISHARES MSCI BRAZIL ETF | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| FTSEMIB Index | PX_LAST | bpipe | FTSE MIB INDEX | EUR | ok |  | 5545 | 2005-01-03 | 2026-10-30 | 21.82 | 0.974 |  |
| FTSEMIB Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | FTSE MIB INDEX | EUR | ok |  | 5544 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| FTSEMIBN Index | PX_LAST | bpipe | FTSE MIB Net TR | EUR | ok |  | 4507 | 2009-02-23 | 2026-10-30 | 17.68 | 0.977 |  |
| GBPUSD Curncy | PX_LAST | bpipe | GBP-USD X-RATE | USD | ok |  | 5695 | 2005-01-03 | 2026-10-30 | 21.82 | 1.0 |  |
| GDBR10 Index | PX_LAST | bpipe | GERMANY GOVT BND 10 YR DBR | EUR | ok |  | 5686 | 2005-01-03 | 2026-10-30 | 21.82 | 0.998 |  |
| GJGB10 Index | PX_LAST | bpipe | Japan Govt 10Y Simple Yield | JPY | ok |  | 5685 | 2005-01-03 | 2026-10-30 | 21.82 | 0.998 |  |
| HG1 Comdty | PX_LAST | bpipe | Generic 1st 'HG' Future | USD | ok |  | 5499 | 2005-01-03 | 2026-10-30 | 21.82 | 0.966 |  |
| HSCEI Index | PX_LAST | bpipe | HANG SENG CHINA ENT INDX | HKD | ok |  | 5377 | 2005-01-03 | 2026-10-30 | 21.82 | 0.944 |  |
| HSCEI Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | HANG SENG CHINA ENT INDX | HKD | ok |  | 5376 | 2005-01-03 | 2026-10-29 | 21.82 | 0.944 |  |
| IBOV Index | PX_LAST | terminal | BRAZIL IBOVESPA INDEX | BRL | ok |  | 5411 | 2005-01-03 | 2026-10-30 | 21.82 | 0.95 |  |
| IBOV Index | TOT_RETURN_INDEX_GROSS_DVDS | terminal | BRAZIL IBOVESPA INDEX | BRL | ok |  | 5411 | 2005-01-03 | 2026-10-30 | 21.82 | 0.95 |  |
| KRE US Equity | PX_LAST | bpipe | SS SPDR S&P REGIONAL BANK | USD | ok |  | 5122 | 2006-06-22 | 2026-10-30 | 20.36 | 0.964 |  |
| KRE US Equity | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | SS SPDR S&P REGIONAL BANK | USD | ok |  | 5121 | 2006-06-22 | 2026-10-29 | 20.35 | 0.964 |  |
| KRX Index | PX_LAST | bpipe | KBW REGIONAL BANKING INX | USD | ok |  | 5571 | 2005-01-03 | 2026-10-30 | 21.82 | 0.978 |  |
| KRX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | KBW REGIONAL BANKING INX | USD | ok |  | 5570 | 2005-01-03 | 2026-10-29 | 21.82 | 0.978 |  |
| KRXTR Index | PX_LAST | bpipe | KBWRegionalBnkTR | USD | ok |  | 5571 | 2005-01-03 | 2026-10-30 | 21.82 | 0.978 |  |
| LF98OAS Index | PX_LAST | terminal | Bloomberg US Corporate High Yi | USD | ok |  | 5493 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| LF98TRUU Index | PX_LAST | terminal | U.S. Corporate High Yield | USD | ok |  | 5497 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 | probe |
| MCX Index | PX_LAST | bpipe | FTSE 250 INDEX | GBP | ok |  | 5516 | 2005-01-04 | 2026-10-30 | 21.82 | 0.969 |  |
| MCX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | FTSE 250 INDEX | GBP | ok |  | 5515 | 2005-01-04 | 2026-10-29 | 21.82 | 0.969 |  |
| MCXNUK Index | PX_LAST | bpipe | FTSE 250 Net Dvd TR Ix | GBP | ok |  | 4064 | 2010-12-31 | 2026-10-30 | 15.83 | 0.984 | probe |
| MDAX Index | PX_LAST | bpipe | MDAX PERF INDEX | EUR | ok |  | 5548 | 2005-01-03 | 2026-10-30 | 21.82 | 0.974 |  |
| MDAX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | MDAX PERF INDEX | EUR | ok |  | 5547 | 2005-01-03 | 2026-10-29 | 21.82 | 0.974 |  |
| MXEF Index | PX_LAST | bpipe | MSCI EM | USD | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| MXEF Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | MSCI EM | USD | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| NDUEEGF Index | PX_LAST | bpipe | MSCI Daily TR Net Emergi | USD | ok |  | 5694 | 2005-01-03 | 2026-10-29 | 21.82 | 1.0 |  |
| NDX Index | PX_LAST | bpipe | NASDAQ 100 STOCK INDX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| NDX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | NASDAQ 100 STOCK INDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| NKY Index | PX_LAST | bpipe | NIKKEI 225 | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 |  |
| NKY Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | NIKKEI 225 | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| NKYTR Index | PX_LAST | bpipe | Nikkei Total Return Idx | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 |  |
| PETR4 BZ Equity | PX_LAST | terminal | PETROBRAS - PETROLEO BRAS-PR | BRL | ok |  | 5410 | 2005-01-03 | 2026-10-30 | 21.82 | 0.95 | probe |
| RSP US Equity | PX_LAST | bpipe | INVESCO S&P 500 EQUAL WEIGHT | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| RSP US Equity | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | INVESCO S&P 500 EQUAL WEIGHT | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| RTY Index | PX_LAST | bpipe | RUSSELL 2000 INDEX | USD | ok |  | 5494 | 2005-01-03 | 2026-10-30 | 21.82 | 0.965 |  |
| RTY Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | RUSSELL 2000 INDEX | USD | ok |  | 5493 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| RUTTR Index | PX_LAST | bpipe | Russ 2000 TR | USD | ok |  | 5494 | 2005-01-03 | 2026-10-30 | 21.82 | 0.965 |  |
| RVX Index | PX_LAST | terminal | Cboe RSL2000 VOLATILTY I | USD | ok |  | 5490 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5COND Index | PX_LAST | bpipe | S&P 500 CONS DISCRET IDX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5COND Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 CONS DISCRET IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5CONS Index | PX_LAST | bpipe | S&P 500 CONS STAPLES IDX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5CONS Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 CONS STAPLES IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5ENRS Index | PX_LAST | bpipe | S&P 500 ENERGY INDEX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5ENRS Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 ENERGY INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5FINL Index | PX_LAST | bpipe | S&P 500 FINANCIALS INDEX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5FINL Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 FINANCIALS INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5INDU Index | PX_LAST | bpipe | S&P 500 INDUSTRIALS IDX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5INDU Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 INDUSTRIALS IDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5MATR Index | PX_LAST | bpipe | S&P 500 MATERIALS INDEX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5MATR Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 MATERIALS INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| S5UTIL Index | PX_LAST | bpipe | S&P 500 UTILITIES INDEX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| S5UTIL Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 UTILITIES INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SMI Index | PX_LAST | bpipe | SWISS MARKET INDEX | CHF | ok |  | 5487 | 2005-01-03 | 2026-10-30 | 21.82 | 0.963 |  |
| SMI Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | SWISS MARKET INDEX | CHF | ok |  | 5486 | 2005-01-03 | 2026-10-29 | 21.82 | 0.963 |  |
| SMIC Index | PX_LAST | bpipe | SMI GROSS TOTAL RETURN | CHF | ok |  | 5487 | 2005-01-03 | 2026-10-30 | 21.82 | 0.963 |  |
| SMIN Index | PX_LAST | bpipe | SMI NR | CHF | ok |  | 4230 | 2010-01-04 | 2026-10-30 | 16.82 | 0.964 | probe |
| SOX Index | PX_LAST | bpipe | PHILA SEMICONDUCTOR INDX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| SOX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | PHILA SEMICONDUCTOR INDX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPHOME Index | PX_LAST | terminal | S&P HOMEBUILDING SEL IND | USD | ok |  | 5497 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SPHOME Index | TOT_RETURN_INDEX_GROSS_DVDS | terminal | S&P HOMEBUILDING SEL IND | USD | ok |  | 5497 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SPSIHOTR Index | PX_LAST | terminal | S&P Homebuild Select TR | USD | ok |  | 5497 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SPSIRBK Index | PX_LAST | terminal | S&P Reg Bank Select Indu | USD | ok |  | 5494 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SPSIRBK Index | TOT_RETURN_INDEX_GROSS_DVDS | terminal | S&P Reg Bank Select Indu | USD | ok |  | 5494 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SPSIRBKT Index | PX_LAST | terminal | S&PRegBankSelectIndu TR | USD | ok |  | 5494 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SPTR Index | PX_LAST | bpipe | S&P 500 TR 4 JAN 1988 | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPW Index | PX_LAST | terminal | S&P500 EQUAL WEIGHTED IX | USD | ok |  | 5501 | 2005-01-03 | 2026-10-29 | 21.82 | 0.966 |  |
| SPW Index | TOT_RETURN_INDEX_GROSS_DVDS | terminal | S&P500 EQUAL WEIGHTED IX | USD | ok |  | 5501 | 2005-01-03 | 2026-10-29 | 21.82 | 0.966 |  |
| SPX Index | PX_LAST | bpipe | S&P 500 INDEX | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| SPX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | S&P 500 INDEX | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| SPXEW Index | PX_LAST | terminal | S&P500 EQUAL WEIGHTED IX | USD | ok |  | 5501 | 2005-01-03 | 2026-10-29 | 21.82 | 0.966 | probe |
| SPXEWTR Index | PX_LAST | terminal | S&P 500 EqWg USD TR | USD | ok |  | 5493 | 2005-01-03 | 2026-10-29 | 21.82 | 0.965 |  |
| SX5E Index | PX_LAST | bpipe | Euro Stoxx 50 Pr | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| SX5E Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | Euro Stoxx 50 Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX5GT Index | PX_LAST | bpipe | ESTX 50 (EUR) GRt | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| SX5T Index | PX_LAST | bpipe | ESTX 50 (EUR) NRt | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 | probe |
| SX6P Index | PX_LAST | bpipe | STXE 600 Utilities EUR | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| SX6P Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | STXE 600 Utilities EUR | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX6R Index | PX_LAST | bpipe | STXE 600 Util (EUR) NRt | EUR | ok |  | 5600 | 2005-01-03 | 2026-10-30 | 21.82 | 0.983 |  |
| SX7E Index | PX_LAST | bpipe | ESTX Banks (EUR) Pr | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| SX7E Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | ESTX Banks (EUR) Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SX7T Index | PX_LAST | bpipe | ESTX Bnk (EUR) NRt | EUR | ok |  | 5599 | 2005-01-03 | 2026-10-30 | 21.82 | 0.983 |  |
| SXPP Index | PX_LAST | bpipe | STXE 600 BasicResou EUR | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| SXPP Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | STXE 600 BasicResou EUR | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SXPR Index | PX_LAST | bpipe | STXE 600 BsRs (EUR) NRt | EUR | ok |  | 5600 | 2005-01-03 | 2026-10-30 | 21.82 | 0.983 |  |
| SXXP Index | PX_LAST | bpipe | STXE 600 (EUR) Pr | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| SXXP Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | STXE 600 (EUR) Pr | EUR | ok |  | 5604 | 2005-01-03 | 2026-10-29 | 21.82 | 0.984 |  |
| SXXR Index | PX_LAST | bpipe | STXE 600 (EUR) NRt | EUR | ok |  | 5605 | 2005-01-03 | 2026-10-30 | 21.82 | 0.984 |  |
| TMCXG Index | PX_LAST | bpipe | FTSE 250 TR Index | GBP | ok |  | 5527 | 2005-01-04 | 2026-10-30 | 21.82 | 0.971 |  |
| TP17BNK Index | PX_LAST | bpipe | TPX-17 Banks Index | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 | probe |
| TPNBNK Index | PX_LAST | bpipe | TOPIX BANKS INDEX | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 |  |
| TPNBNK Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | TOPIX BANKS INDEX | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPX Index | PX_LAST | bpipe | TOPIX INDEX (TOKYO) | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 |  |
| TPX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | TOPIX INDEX (TOKYO) | JPY | ok |  | 5341 | 2005-01-04 | 2026-10-29 | 21.82 | 0.938 |  |
| TPXDDVD Index | PX_LAST | bpipe | TOPIX TR Index | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 |  |
| TPXNTR Index | PX_LAST | bpipe | TOPIX Net Total Return | JPY | ok |  | 3214 | 2013-09-02 | 2026-10-30 | 13.16 | 0.936 | probe |
| TRAN Index | PX_LAST | bpipe | DOW JONES TRANS. AVG | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| TRAN Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | DOW JONES TRANS. AVG | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| TUKXG Index | PX_LAST | bpipe | FTSE 100 TR GBP | GBP | ok |  | 5580 | 2005-01-04 | 2026-10-30 | 21.82 | 0.98 |  |
| UKX Index | PX_LAST | bpipe | FTSE 100 INDEX | GBP | ok |  | 5516 | 2005-01-04 | 2026-10-30 | 21.82 | 0.969 |  |
| UKX Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | FTSE 100 INDEX | GBP | ok |  | 5515 | 2005-01-04 | 2026-10-29 | 21.82 | 0.969 |  |
| UKXNUK Index | PX_LAST | bpipe | FTSE 100 Net Tax Index | GBP | ok |  | 5539 | 2005-01-04 | 2026-10-30 | 21.82 | 0.973 | probe |
| USDBRL Curncy | PX_LAST | bpipe | USD-BRL X-RATE | BRL | ok |  | 5505 | 2005-01-03 | 2026-10-30 | 21.82 | 0.967 |  |
| USDCHF Curncy | PX_LAST | bpipe | USD-CHF X-RATE | CHF | ok |  | 5695 | 2005-01-03 | 2026-10-30 | 21.82 | 1.0 |  |
| USDHKD Curncy | PX_LAST | bpipe | USD-HKD X-RATE | HKD | ok |  | 5693 | 2005-01-03 | 2026-10-30 | 21.82 | 1.0 |  |
| USDJPY Curncy | PX_LAST | bpipe | USD-JPY X-RATE | JPY | ok |  | 5695 | 2005-01-03 | 2026-10-30 | 21.82 | 1.0 |  |
| USGG10YR Index | PX_LAST | bpipe | US Generic Govt 10 Yr | USD | ok |  | 5691 | 2005-01-03 | 2026-10-30 | 21.82 | 0.999 |  |
| USGG2YR Index | PX_LAST | bpipe | US Generic Govt 2 Yr | USD | ok |  | 5691 | 2005-01-03 | 2026-10-30 | 21.82 | 0.999 |  |
| USGGBE10 Index | PX_LAST | bpipe | US Breakeven 10 Year | USD | ok |  | 5687 | 2005-01-03 | 2026-10-30 | 21.82 | 0.999 |  |
| USGGT10Y Index | PX_LAST | bpipe | US Generic Govt TII 10 Yr | USD | ok |  | 5689 | 2005-01-03 | 2026-10-30 | 21.82 | 0.999 |  |
| UTIL Index | PX_LAST | bpipe | DOW JONES UTILITY AVG | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| UTIL Index | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | DOW JONES UTILITY AVG | USD | ok |  | 5491 | 2005-01-03 | 2026-10-29 | 21.82 | 0.964 |  |
| V2X Index | PX_LAST | terminal | VSTOXX Index | EUR | ok |  | 5560 | 2005-01-03 | 2026-10-30 | 21.82 | 0.976 |  |
| VIX Index | PX_LAST | bpipe | Cboe Volatility Index | USD | ok |  | 5525 | 2005-01-03 | 2026-10-30 | 21.82 | 0.97 |  |
| VNKY Index | PX_LAST | bpipe | NIKKEI Volatility Index | JPY | ok |  | 5342 | 2005-01-04 | 2026-10-30 | 21.82 | 0.938 |  |
| VXN Index | PX_LAST | terminal | Cboe NDX VOLATILITY INDX | USD | ok |  | 5495 | 2005-01-03 | 2026-10-30 | 21.82 | 0.965 |  |
| XHB US Equity | PX_LAST | bpipe | SS SPDR S&P HOMEBLDRS ETF | USD | ok |  | 5217 | 2006-02-06 | 2026-10-30 | 20.73 | 0.964 |  |
| XHB US Equity | TOT_RETURN_INDEX_GROSS_DVDS | bpipe | SS SPDR S&P HOMEBLDRS ETF | USD | ok |  | 5216 | 2006-02-06 | 2026-10-29 | 20.73 | 0.964 |  |
| XNDX Index | PX_LAST | bpipe | NASDAQ 100 TOTAL RETURN | USD | ok |  | 5492 | 2005-01-03 | 2026-10-30 | 21.82 | 0.964 |  |
| XSOX Index | PX_LAST | bpipe | PHLX SmCondtr Sec TR | USD | ok |  | 4240 | 2009-12-22 | 2026-10-30 | 16.85 | 0.964 |  |
| VOLQ Index | PX_LAST | bpipe | NDX Volatility | USD | stale |  | 2453 | 2014-01-02 | 2023-09-29 | 9.74 | 0.965 | probe,stale |

## Spreads

| id | alignment | rows | built | empty_legs | bases | tr_vs_price | warning |
| --- | --- | --- | --- | --- | --- | --- | --- |
| us_cyc_def | native | 5490 | True |  | S5INDU Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5MATR Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5CONS Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5UTIL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | S5INDU Index:57.4%, S5MATR Index:58.9%, S5CONS Index:77.5%, S5UTIL Index:116.3% |  |
| rty_spx | native | 5499 | True |  | RTY Index=total_return_gross/RUTTR Index, SPX Index=total_return_gross/SPTR Index | RTY Index:34.0%, SPX Index:54.0% |  |
| spw_spx | native | 5492 | True |  | SPW Index=total_return_gross/SPXEWTR Index, SPX Index=total_return_gross/SPTR Index | SPW Index:50.8%, SPX Index:54.0% |  |
| rsp_spx | native | 5490 | True |  | RSP US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | RSP US Equity:42.2%, SPX Index:54.0% | instrument_mismatch: etf, index |
| ndx_spx | native | 5491 | True |  | NDX Index=total_return_gross/XNDX Index, SPX Index=total_return_gross/SPTR Index | NDX Index:21.3%, SPX Index:54.0% |  |
| s5finl_s5util | native | 5490 | True |  | S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5UTIL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | S5FINL Index:57.0%, S5UTIL Index:116.3% |  |
| kre_s5finl | native | 5490 | True |  | KRE US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | KRE US Equity:65.7%, S5FINL Index:57.0% | instrument_mismatch: etf, index |
| krx_s5finl | native | 5570 | True |  | KRX Index=total_return_gross/KRXTR Index, S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | KRX Index:78.0%, S5FINL Index:57.0% |  |
| spsirbk_s5finl | native | 5493 | True |  | SPSIRBK Index=total_return_gross/SPSIRBKT Index, S5FINL Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | SPSIRBK Index:74.1%, S5FINL Index:57.0% |  |
| xhb_spx | native | 5490 | True |  | XHB US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | XHB US Equity:22.7%, SPX Index:54.0% | instrument_mismatch: etf, index |
| djushb_spx | native | 5504 | True |  | DJUSHB Index=price/price, SPX Index=total_return_gross/SPTR Index | DJUSHB Index:0.0%, SPX Index:54.0% | mixed_basis: price, total_return_gross |
| sphome_spx | native | 5496 | True |  | SPHOME Index=total_return_gross/SPSIHOTR Index, SPX Index=total_return_gross/SPTR Index | SPHOME Index:27.4%, SPX Index:54.0% |  |
| sox_spx | native | 5491 | True |  | SOX Index=total_return_gross/XSOX Index, SPX Index=total_return_gross/SPTR Index | SOX Index:53.7%, SPX Index:54.0% |  |
| s5enrs_s5cond | native | 5490 | True |  | S5ENRS Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, S5COND Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS | S5ENRS Index:83.9%, S5COND Index:33.3% |  |
| tran_util | native | 5548 | True |  | TRAN Index=total_return_gross/DJTTR Index, UTIL Index=total_return_gross/DJUTR Index | TRAN Index:37.9%, UTIL Index:115.6% |  |
| sx7e_sx6p | native | 5599 | True |  | SX7E Index=total_return_net/SX7T Index, SX6P Index=total_return_net/SX6R Index | SX7E Index:106.7%, SX6P Index:137.2% |  |
| ftsemib_dax | native | 5572 | True |  | FTSEMIB Index=total_return_net/FTSEMIBN Index, DAX Index=total_return/price | FTSEMIB Index:234.9%, DAX Index:0.0% | mixed_basis: total_return, total_return_net |
| mdax_dax | native | 5547 | True |  | MDAX Index=total_return/price, DAX Index=total_return/price | MDAX Index:0.0%, DAX Index:0.0% |  |
| smi_sx5e | native | 5604 | True |  | SMI Index=total_return_gross/SMIC Index, SX5E Index=total_return_gross/SX5GT Index | SMI Index:93.8%, SX5E Index:119.4% |  |
| sxpp_sxxp | native | 5604 | True |  | SXPP Index=total_return_net/SXPR Index, SXXP Index=total_return_net/SXXR Index | SXPP Index:103.1%, SXXP Index:81.8% |  |
| tpx_nky | native | 5341 | True |  | TPX Index=total_return_gross/TPXDDVD Index, NKY Index=total_return_gross/NKYTR Index | TPX Index:57.6%, NKY Index:47.8% |  |
| tpxbnk_tpx | native | 5341 | True |  | TPNBNK Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, TPX Index=total_return_gross/TPXDDVD Index | TPNBNK Index:89.6%, TPX Index:57.6% |  |
| mcx_ukx | native | 5579 | True |  | MCX Index=total_return_gross/TMCXG Index, UKX Index=total_return_gross/TUKXG Index | MCX Index:84.1%, UKX Index:124.6% |  |
| mxef_spx | native | 5693 | True |  | MXEF Index=total_return_net/NDUEEGF Index, SPX Index=total_return_gross/SPTR Index | MXEF Index:68.3%, SPX Index:54.0% | mixed_basis: total_return_gross, total_return_net |
| hscei_spx | asia_to_us | 5490 | True |  | HSCEI Index=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, SPX Index=total_return_gross/SPTR Index | HSCEI Index:64.8%, SPX Index:54.0% |  |
| ibov_mxef | native | 5694 | True |  | IBOV Index=price/price, MXEF Index=total_return_net/NDUEEGF Index | IBOV Index:0.0%, MXEF Index:68.3% | mixed_basis: price, total_return_net |
| ewz_mxef | native | 5693 | True |  | EWZ US Equity=total_return_gross/TOT_RETURN_INDEX_GROSS_DVDS, MXEF Index=total_return_net/NDUEEGF Index | EWZ US Equity:139.8%, MXEF Index:68.3% | mixed_basis: total_return_gross, total_return_net; instrument_mismatch: etf, index |
| as51_spx | asia_to_us | 5490 | True |  | AS51 Index=total_return_gross/AS51T Index, SPX Index=total_return_gross/SPTR Index | AS51 Index:147.5%, SPX Index:54.0% |  |

## Probes that did not resolve

IBOVESPA Index, VSTOXX Index
