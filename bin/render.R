#!/usr/bin/env Rscript
rmarkdown::render("report.Rmd",
  output_file = "datashare/report.html",
  params = list(input_dir = "data")
)
