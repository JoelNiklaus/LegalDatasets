# to install the packages, run the following commands:
# install.packages("remotes"), remotes::install_github("jjesusfilho/tjsp"), install.packages("rjson"), remotes::install_github("courtsbr/JurisMiner") 

remotes::install_github("courtsbr/JurisMiner") 


library(tjsp)
library(rjson)

#slackr_setup()

print_and_report <- function(message) {
  print(message)
  #slackr_bot(message)
}

save_type <- function(json_dir, type) {
  # The commands below will read the results from the scraping, convert them to a table and save them as json
  print_and_report(paste("Converting to a table the data from this directory: ", type))

  read_function <- getFunction(paste("ler_", type, sep = ""))
  table <- read_function(diretorio = type)

  filename <- paste(json_dir, "/", type, ".json", sep = "")
  sink(filename)
  cat(toJSON(table))
  sink()

}

# tjsp: Tribunal de Justicia de Sao Paolo

# cjpg: consulta de julgados de primeiro grau
# cjsg: consulta de julgados de segundo grau
# cpopg: consulta processual de primeiro grau
# cposg: consulta processual de segundo grau


json_dir <- "results_as_json"
dir.create(json_dir)


# You can insert (comma seperated) other keywords that you want to use to find documents
keyword <- "a" # just use a simple article "a" so that we find everything

# for testing purposes we will only download a few documents
# keyword <- "Agente de segurança penitenciária que almeja transferência – Impetrante que não cumpre o requisito"

types <- c("cjpg", "cjsg") # "cpopg", "cposg" require special treatment


for (type in types) {

  dir.create(type) # A general directory will be created where the results will be stored; for each keyword you can create a separate directory if you want
  
  dates <- JurisMiner::agrupar_datas("01/10/2022", "31/10/2022",intervalos = 20)

  print_and_report(paste("Scraping documents for type: ", type))
  #download_function <- getFunction(paste("baixar_", type, sep = ""))

  purrr::walk2(dates$data_inicial, dates$data_final,~{
        
        if(setequal(type,'cjpg')){
          tjsp::tjsp_baixar_cjpg(inicio = .x, fim = .y, diretorio = type)
        }
        else if(setequal(type,'cjsg')){
          tjsp::tjsp_baixar_cjsg(inicio = .x, fim = .y, diretorio = type)
          }
 
  })
  #download_function(livre = keyword, diretorio = type) # fetch the documents and save them in the specified directory

  save_type(json_dir, type)

  print_and_report(paste("Finished scraping documents for type: ", type))
}

