library(tjsp)
library(rjson)

table <- ler_cjsg(diretorio="./cjpg")


json_dir <- "results_as_json"
dir.create(json_dir)

filename <- paste(json_dir, "/", 'cjpg', ".json", sep = "")
sink(filename)
cat(toJSON(table))
sink()