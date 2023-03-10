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
template$country="be"
template$language="fr"
template$type="case law"


for (y in 2007:2022) {
  
  for (c in 0:200) {
    
    text1=paste0("https://juportal.be/content/ECLI:BE:GHCC:",as.character(y))
    text2=paste0(":ARR.",as.character(sprintf("%03d", c)))
    text1=paste0(text1,text2)
    text1=paste0(text1,"/FR?HiLi=eNpLtDK2qs60MrAutjI0sFLKKk3JTM5MzCxKVbLOtDKEinqFung6ezp6BrmCRI1gokhqawEFMBVu")
    page=read_html(text1)
    
    raw_list <- page %>% # takes the page above for which we've read the html
      html_nodes("a") %>%  # find all links in the page
      html_attr("href") %>% # get the url for these links
      str_subset("\\.pdf") %>% # find those that end in pdf only
      str_c("", .)
    
    tryCatch({
      url=raw_list[1]
      url=paste0("https://juportal.be",url,sep="")
      article <- pdf_text(url)
      test=paste(article, collapse = '')
      template$text=test
      to_Write=toJSON(template)
      to_Write<-str_sub(to_Write,2,-2)
      write(to_Write,  file="belgium.json",append = TRUE)
      remove(article)
      remove(to_Write)
      stop("Error !")
    }, error=function(e){})
    
    
  }
  
}





  

