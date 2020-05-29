setwd("/Users/linghuiwu/uchicago/courseworks/macs30250/persp-research-econ_Spr20/FinalPaper/codes")

library(readxl)
library(ggplot2)
library(usmap)

da <- read_excel("../data/trade_shock.xlsx"); head(da)
da <- as.data.frame(da); head(da)

plot_usmap(data=da, values="change2017", color="red") + 
  scale_fill_continuous(
    low="white", high="red", name="Import Trade Shock",
    label=scales::comma
  ) + theme(legend.position="right")

