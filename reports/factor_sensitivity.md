# Factor sensitivity

Betas are from a rolling regression with an intercept. The fit on a date includes that date.
Yield betas are spread return per 1 percentage point, not per basis point.
The driver signs in the config are still placeholders. A disagree below is a disagree with that placeholder.
A native Asian spread is joined on the same calendar date, so a US factor can print after that equity close.
`net_vs_gross` is copied from the sized series and is not a reason to drop the spread.

## Placeholder signs, beta-neutral, longest window

### disagrees (20)

- `us_cyc_def` vs `us_10y` (local): beta -0.043, t -3.29 (notable), placeholder +. same basis.
- `us_cyc_def` vs `us_2s10s` (local): beta -0.031, t -1.29 (not notable), placeholder +. same basis.
- `spw_spx` vs `us_10y` (local): beta -0.037, t -5.79 (notable), placeholder +. same basis.
- `rsp_spx` vs `us_10y` (local): beta -0.036, t -5.62 (notable), placeholder +. instrument_mismatch: etf, index.
- `ndx_spx` vs `us_10y` (local): beta 0.018, t 2.36 (notable), placeholder -. same basis.
- `ndx_spx` vs `us_10y_real` (local): beta 0.018, t 1.96 (not notable), placeholder -. same basis.
- `s5finl_s5util` vs `us_10y` (local): beta -0.029, t -2.10 (notable), placeholder +. same basis.
- `kre_s5finl` vs `hy_oas` (local): beta 0.003, t 0.24 (not notable), placeholder -. instrument_mismatch: etf, index.
- `krx_s5finl` vs `hy_oas` (local): beta 0.005, t 0.48 (not notable), placeholder -. same basis.
- `spsirbk_s5finl` vs `hy_oas` (local): beta 0.004, t 0.41 (not notable), placeholder -. same basis.
- `sox_spx` vs `us_10y_real` (local): beta 0.060, t 1.76 (not notable), placeholder -. same basis.
- `tran_util` vs `us_10y` (local): beta -0.074, t -3.64 (notable), placeholder +. same basis.
- `tran_util` vs `wti` (local): beta -0.102, t -3.90 (notable), placeholder +. same basis.
- `sx7e_sx6p` vs `us_2s10s` (local): beta -0.007, t -0.18 (not notable), placeholder +. same basis.
- `sx7e_sx6p` vs `bund_10y` (local): beta -0.097, t -4.01 (notable), placeholder +. same basis.
- `mdax_dax` vs `bund_10y` (local): beta -0.008, t -0.78 (not notable), placeholder +. same basis.
- `tpx_nky` vs `usdjpy` (local): beta 0.109, t 1.33 (not notable), placeholder -. same basis. Native Asian close, same calendar date as the US factor.
- `hscei_spx` vs `copper` (usd): beta -0.015, t -0.35 (not notable), placeholder +. same basis.
- `ibov_mxef` vs `wti` (usd): beta -0.091, t -2.28 (notable), placeholder +. mixed_basis: price, total_return_net.
- `ewz_mxef` vs `wti` (local): beta -0.092, t -2.37 (notable), placeholder +. mixed_basis: total_return_gross, total_return_net; instrument_mismatch: etf, index; net_vs_gross.

### matches (30)

- `rty_spx` vs `us_2y` (local): beta -0.019, t -2.09 (notable), placeholder -. same basis.
- `rty_spx` vs `hy_oas` (local): beta -0.003, t -0.46 (not notable), placeholder -. same basis.
- `s5finl_s5util` vs `us_2s10s` (local): beta 0.003, t 0.13 (not notable), placeholder +. same basis.
- `kre_s5finl` vs `us_2s10s` (local): beta 0.018, t 0.75 (not notable), placeholder +. instrument_mismatch: etf, index.
- `krx_s5finl` vs `us_2s10s` (local): beta 0.019, t 0.79 (not notable), placeholder +. same basis.
- `spsirbk_s5finl` vs `us_2s10s` (local): beta 0.018, t 0.76 (not notable), placeholder +. same basis.
- `xhb_spx` vs `us_10y` (local): beta -0.173, t -9.36 (notable), placeholder -. instrument_mismatch: etf, index.
- `xhb_spx` vs `us_10y_real` (local): beta -0.161, t -6.87 (notable), placeholder -. instrument_mismatch: etf, index.
- `djushb_spx` vs `us_10y` (local): beta -0.216, t -9.39 (notable), placeholder -. mixed_basis: price, total_return_gross.
- `djushb_spx` vs `us_10y_real` (local): beta -0.212, t -7.33 (notable), placeholder -. mixed_basis: price, total_return_gross.
- `sphome_spx` vs `us_10y` (local): beta -0.173, t -9.36 (notable), placeholder -. same basis.
- `sphome_spx` vs `us_10y_real` (local): beta -0.161, t -6.84 (notable), placeholder -. same basis.
- `sox_spx` vs `copper` (local): beta 0.279, t 3.86 (notable), placeholder +. same basis.
- `s5enrs_s5cond` vs `us_10y_be` (local): beta 0.236, t 5.11 (notable), placeholder +. same basis.
- `s5enrs_s5cond` vs `wti` (local): beta 0.252, t 11.88 (notable), placeholder +. same basis.
- `ftsemib_dax` vs `bund_10y` (local): beta 0.018, t 1.92 (not notable), placeholder +. mixed_basis: total_return, total_return_net; net_vs_gross.
- `smi_sx5e` vs `dxy` (usd): beta -0.253, t -1.90 (not notable), placeholder -. same basis.
- `sxpp_sxxp` vs `dxy` (local): beta -0.973, t -3.90 (notable), placeholder -. same basis.
- `sxpp_sxxp` vs `copper` (local): beta 0.465, t 12.07 (notable), placeholder +. same basis.
- `tpx_nky` vs `jgb_10y` (local): beta 0.006, t 0.59 (not notable), placeholder +. same basis. Native Asian close, same calendar date as the US factor.
- `tpxbnk_tpx` vs `usdjpy` (local): beta -0.128, t -0.83 (not notable), placeholder -. same basis. Native Asian close, same calendar date as the US factor.
- `tpxbnk_tpx` vs `jgb_10y` (local): beta 0.071, t 3.46 (notable), placeholder +. same basis. Native Asian close, same calendar date as the US factor.
- `mcx_ukx` vs `dxy` (local): beta -0.220, t -1.99 (notable), placeholder -. same basis.
- `mxef_spx` vs `dxy` (local): beta -0.304, t -1.07 (not notable), placeholder -. mixed_basis: total_return_gross, total_return_net; net_vs_gross.
- `mxef_spx` vs `copper` (local): beta 0.187, t 3.64 (notable), placeholder +. mixed_basis: total_return_gross, total_return_net; net_vs_gross.
- `hscei_spx` vs `dxy` (usd): beta -0.534, t -2.34 (notable), placeholder -. same basis.
- `ibov_mxef` vs `dxy` (usd): beta -2.049, t -4.90 (notable), placeholder -. mixed_basis: price, total_return_net.
- `ewz_mxef` vs `dxy` (local): beta -2.037, t -5.01 (notable), placeholder -. mixed_basis: total_return_gross, total_return_net; instrument_mismatch: etf, index; net_vs_gross.
- `as51_spx` vs `dxy` (usd): beta -0.193, t -1.13 (not notable), placeholder -. same basis.
- `as51_spx` vs `copper` (usd): beta 0.015, t 0.47 (not notable), placeholder +. same basis.

### no_estimate (0)

None.

## Short window and long window disagree, and both t-stats are past 1.96

- `sx7e_sx6p` vs `bund_10y` (local): long beta -0.097, t -4.01. same basis

