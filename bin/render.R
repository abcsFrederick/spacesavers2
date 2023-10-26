#!/usr/bin/env Rscript
rmarkdown::render("report.Rmd",
  output_file = "docs/report.html",
  params = list(input_dir = "data")
)
