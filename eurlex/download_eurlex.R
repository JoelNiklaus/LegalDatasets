# install.packages("pdftools")
# install.packages("eurlex")
# install.packages("jsonlite")


library(eurlex)
library(dplyr) # my preference, not needed for the package
library(jsonlite)


download_with_progress_bar <- function(results, n) {

  safe_fetch <- function(work, type) {
    tryCatch({
      return(elx_fetch_data(work, type = type))
    }, error = function(e) {
      print(paste("Could not load instance of type ", type, ". Saving NA instead.", sep = ""))
      print(e)
      return(NA)
    })
  }

  titles <- c()
  texts <- c()
  pb <- txtProgressBar(min = 0, max = length(results$work[1:n]), initial = 0)
  for (i in seq_along(results$work[1:n])) {
    titles <- append(titles, safe_fetch(results$work[i], "title"))
    texts <- append(texts, safe_fetch(results$work[i], "text"))
    setTxtProgressBar(pb, i)
  }
  close(pb)
  df <- slice(results, 1:n)
  df['title'] <- titles
  df['text'] <- texts
  df <- df %>% select(celex, date, title, text)

  return(df)
}


download_vectorized <- function(results, n) {

  # the function is not vectorized by default
  # elx_fetch_data(url = results$work[1], type = "title")

  # we can use purrr::map() to play that role
  library(purrr)

  download <- function(work, type) {
    result <- tryCatch({
      return(elx_fetch_data(work, type = type))
    }, error = function(cond) {
      message(cond)
      return(NA)
    })
    return(result)
  }

  df <- results[1:n,] %>% # take the first 5 ones only to save time
    #df <- results %>% # download everything
    mutate(title = map_chr(work, download, "title")) %>%
    mutate(text = map_chr(work, download, "text")) %>%
    as_tibble() %>%
    select(celex, date, title) # text

  return(df)
}


download_and_save_resource_type <- function(resource_type, debug = TRUE) {
  print(paste("Downloading", resource_type))

  # compose the sparql query
  query_dir <- elx_make_query(resource_type = resource_type, include_date = TRUE)
  query_dir %>%
    cat() # for nicer printing

  # run the sparql query
  results <- elx_run_query(query = query_dir) %>%
    rename(date = `callret-3`) %>%
    as_tibble()

  if (debug == TRUE) {
    n <- 2
  }else {
    n <- length(results$work)
  }

  # TODO chunk this to be safer if it doesn't work

  # download actual data (titles and texts)
  df <- download_with_progress_bar(results, n)
  print(df)

  # convert the df to jsonl
  jsonl <- toJSON(df)
  cat(jsonl)

  # write jsonl to file
  file_name <- paste("eurlex/", resource_type, ".jsonl", sep = '')
  write(jsonl, file = file_name)

  return(df)
}


# regulation: ~140K
# caselaw: ~100K
# decision: ~53K
# proposal: ~29K
# recommendation: ~3K

resource_types <- c("directive", "regulation", "decision", "recommendation",
                    "intagr", "caselaw", "manual", "proposal", "national_impl")

for (resource_type in resource_types) {
  df <- download_and_save_resource_type(resource_type, debug = FALSE)
  print(df)
}

# Run the script with "R CMD BATCH download_eurlex.R"