// Import data

clear
use "/Users/linghuiwu/uchicago/courseworks/macs30250/persp-research-econ_Spr20/FinalPaper/data/dataset.dta"


// Summary statistics

xtset agency year
codebook

twoway (lfit lstm_mean year) (scatter lstm_mean year) (lfit blob_mean year) (scatter blob_mean year)
twoway (lfit lstm_trade_mean year) (scatter lstm_trade_mean year) (lfit blob_trade_mean year) (scatter blob_trade_mean year)
twoway (lfit lstm_non_trade_mean year) (scatter lstm_non_trade_mean year) (lfit blob_non_trade_mean year) (scatter blob_non_trade_mean year)


// Baseline

reg lstm shock, r
est store base1
reg lstm shock fem asian bachelor income, r
est store base2
vif


// Subsample

reg trade_lstm shock, r
est store base3
reg trade_lstm shock fem asian bachelor income, r
est store base4

reg non_trade_lstm shock, r
est store base5
reg non_trade_lstm shock fem asian bachelor income, r
est store base6

esttab base1 base2 base3 base4 base5 base6 using base.tex, replace booktabs


// Robustness Check

reg blob shock, r
est store robust1
reg blob shock fem asian bachelor income, r
est store robust2


reg trade_blob shock, r
est store robust3
reg trade_blob shock fem asian bachelor income, r
est store robust4


reg non_trade_blob shock, r
est store robust5
reg non_trade_blob shock fem asian bachelor income, r
est store robust6

esttab robust1 robust2 robust3 robust4 robust5 robust6 using robust.tex, replace booktabs

