
#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

## program...
username <- args[1]
password <- args[2]
input_path <- args[3]
ouput_path <- args[4]

if (dir.exists(ouput_path)==FALSE) {
    dir.create(ouput_path) 
  }

print(input_path)
print(ouput_path)

# This implies that you are in the directory where the downloaded HTML scripts are saved
# Save the paths to the html files in a variable 
a <- list.files(input_path, full.names=TRUE)
print(a)

# Convert the file content to a dataframe
# To have a look at the content of the dataframe do this: tibble::glimpse(df)
df <- tjsp::tjsp_ler_cjsg(a)
print(df)

# Authenticate with username and password for the page https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1
# You need to authenticate in order to bypass the captchas
tjsp::tjsp_autenticar(username, password)

# Download the PDFs with the entore opinion
# The ID of the opinion is saved in the column cdacordao
# tjsp_baixar_acordaos_cjsg: first argument the id of the opinion to be downloaded, second argument the directory you want to save the pdfs, in this case the current directory
tjsp::tjsp_baixar_acordaos_cjsg(df$cdacordao, ouput_path)





