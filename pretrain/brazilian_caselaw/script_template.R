# to install the packages, run the following commands:
# install.packages("remotes"), remotes::install_github("jjesusfilho/tjsp"), install.packages("rjson"), remotes::install_github("courtsbr/JurisMiner") 


library(tjsp)
library(rjson)


year <- {YEAR}
start_date <- paste("01/01/", year, sep="")
end_date <- paste("31/12/", year, sep="")
download <- {DOWNLOAD_BOOLEAN}

#slackr_setup()

print_and_report <- function(message) {
  print(message)
  #slackr_bot(message)
}

save_type <- function(json_dir, dir_name, type) {
  # The commands below will read the results from the scraping, convert them to a table and save them as json
  print_and_report(paste("Converting to a table the data from this directory: ", type))

  read_function <- getFunction(paste("ler_", type, sep = ""))
  table <- read_function(diretorio = dir_name)

  filename <- paste(json_dir, "/", dir_name, ".json", sep = "")
  #sink(filename)
  #cat(toJSON(table))
  #sink()

  # The download strategy below seems to be more reliable than the previous one above
  fh <- file(filename, "w")
  for (i in 1:nrow(table)) {
      write.table(toJSON(table[i,]), fh,
                  row.names = FALSE, col.names = FALSE, quote = FALSE)
  }
  close(fh)

}

# tjsp: Tribunal de Justicia de Sao Paolo

# cjpg: consulta de julgados de primeiro grau
# cjsg: consulta de julgados de segundo grau
# cpopg: consulta processual de primeiro grau
# cposg: consulta processual de segundo grau


json_dir <- "results_as_json"
if (dir.exists(json_dir)==FALSE) {
    dir.create(json_dir) # A general directory will be created where the results will be stored; for each keyword you can create a separate directory if you want
}


# You can insert (comma seperated) other keywords that you want to use to find documents
keyword <- "a" # just use a simple article "a" so that we find everything

# for testing purposes we will only download a few documents
# keyword <- "Agente de segurança penitenciária que almeja transferência – Impetrante que não cumpre o requisito"

types <- c("cjpg", "cjsg") # "cpopg", "cposg" require special treatment

dates <- JurisMiner::agrupar_datas(start_date, end_date, intervalos = 20)


for (type in types) {

  dir_name <- paste(type, gsub("/", "-", start_date), gsub("/", "-", end_date), sep = "__")

  print(dir_name)

  if (dir.exists(dir_name)==FALSE) {
    dir.create(dir_name) # A general directory will be created where the results will be stored; for each keyword you can create a separate directory if you want
  }

  print_and_report(paste("Scraping documents for type: ", type))

  if (download) {
    purrr::walk2(dates$data_inicial, dates$data_final, ~{
      if (setequal(type, 'cjpg')) {
        tjsp::tjsp_baixar_cjpg(inicio = .x, fim = .y, diretorio = dir_name)
      }
      else if (setequal(type, 'cjsg')) {
        tjsp::tjsp_baixar_cjsg(inicio = .x, fim = .y, diretorio = dir_name)
      }
    })
    # download_function <- getFunction(paste("baixar_", type, sep = ""))
    # download_function(livre = keyword, diretorio = type) # fetch the documents and save them in the specified directory
  }

  save_type(json_dir, dir_name, type)

  print_and_report(paste("Finished scraping documents for type: ", type))
}

