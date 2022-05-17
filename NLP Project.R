library(pdftools)
library(tidytext)
library(textrank)
library(dplyr)
library(tibble)
library(tidyverse)
library(rvest)
library(stringr)
library(httr)
library(jsonlite)


template=matrix(nrow = 1, ncol = 4)
template=as.data.frame(template)
colnames(template)=c("language","country","type","text")
template$country="lu"
template$language="fr"
template$type="case law"

for (page_results in seq(from=10400,to=20000,by=20)) {
  link=paste0("https://justice.public.lu/fr/jurisprudence/juridictions-judiciaires.html?b=",page_results)
  
  page <- read_html(link)
  raw_list <- page %>% # takes the page above for which we've read the html
    html_nodes("a") %>%  # find all links in the page
    html_attr("href") %>% # get the url for these links
    str_subset("\\.pdf") %>% # find those that end in pdf only
    str_c("", .)
    test11=as.character(as.integer (page_results / 500))
    
  
    for (i in 1:length(raw_list)) {

    if(!http_error(raw_list[i]))
    {
      
      tryCatch({
        url=raw_list[i]
        article <- pdf_text(url)
        test=paste(article, collapse = '')
        test=paste(test,'"',sep = "")
        template$text=test
        to_Write=toJSON(template)
        to_Write<-str_sub(to_Write,2,-2)
        filename=paste0(test11,"_juridictions_judiciaires.json")
        write(to_Write,  file=filename,append = TRUE)
        remove(article)
        remove(to_Write)
        stop("Urgh, the iphone is in the blender !")
      }, error=function(e){})
      
    }
}
}


