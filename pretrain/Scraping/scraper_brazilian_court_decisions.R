library(tjsp)
library(rjson) # Install it before, in case it has not been installed yet with the following command: install.packages("rjson")


#You can insert (comma seperated) other keywords that you want to use to find documents
list_of_keywords = list("a")

for (keyword in list_of_keywords)

	{
	    print(paste("Scraping documents for the keyword: ",keyword))	
		
		#dirname <- paste("results_with_keyword",keyword,sep="__") # In case you want to create a separate directory for each keyword, you can use this

		dirname <- "scraping_results"

		dir.create(dirname) #A general directory will be created where the results will be stored; for each keyword you can create a separate directory if you want

		baixar_cjsg(livre=keyword,diretorio=dirname) #This command will fetch the documents and save them in the specified directory

	}	



# The commands below will read the results from the scraping, convert them to a table and save them as json


dirname <- "scraping_results"
list_of_directories = list( dirname
							)

for (directory in list_of_directories)

	{
	    print(paste("Converting to a table the data from this directory: ",directory))	
		table <- ler_cjsg(diretorio=directory)
		filename = paste("results_as_json/",directory,".json",sep="")
		sink(filename)
		cat(toJSON(table))
		sink()

	}
