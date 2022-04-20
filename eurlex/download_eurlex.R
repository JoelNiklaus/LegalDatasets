# install.packages("pdftools")
# install.packages("eurlex")
# install.packages("jsonlite")


library(eurlex)
library(dplyr) # my preference, not needed for the package
library(jsonlite)

debug_size <- 2
debug <- TRUE
verbose <- FALSE


download_with_progress_bar <- function(results, language, n, log_frequency = 1000) {
  error_counter <- 0

  safe_fetch <- function(work, type) {
    tryCatch({
      return(elx_fetch_data(work, type = type,
                            language_1 = language, language_2 = "", language_3 = ""))
    }, error = function(e) {
      if (verbose) {
        print(paste("Could not load instance of type ", type, ". Saving NA instead.", sep = ""))
        print(e)
      }
      error_counter <<- error_counter + 1
      return(NA)
    })
  }

  print("Download progress:")

  titles <- c()
  texts <- c()
  languages <- c()
  selected_results <- results$work[1:n]
  max <- length(selected_results)
  # pb <- txtProgressBar(min = 0, max = max, initial = 0)
  for (i in seq_along(selected_results)) {
    titles <- append(titles, safe_fetch(results$work[i], "title"))
    texts <- append(texts, safe_fetch(results$work[i], "text"))
    languages <- append(languages, language)
    if (i %% log_frequency == 0) {
      print(paste(i, "/", max))
    }
    # setTxtProgressBar(pb, i)
  }
  # close(pb)
  df <- slice(results, 1:n)
  df['title'] <- titles
  df['text'] <- texts
  df['language'] <- languages
  df <- df %>% select(celex, language, date, title, text)

  print(paste("Encountered errors (saved NA) for", error_counter, "entries."))

  return(df)
}


download_and_save_resource_type <- function(resource_type, language, debug = TRUE) {
  print(paste("Downloading", resource_type, language))

  # compose the sparql query
  query_dir <- elx_make_query(resource_type = resource_type, include_date = TRUE)
  if (verbose) {
    query_dir %>%
      cat() # for nicer printing
  }

  # run the sparql query
  results <- elx_run_query(query = query_dir) %>%
    rename(date = `callret-3`) %>%
    as_tibble()

  n_results <- length(results$work)

  print(paste("Found", n_results, "for resource_type", resource_type, "and language", language))

  if (debug == TRUE) {
    n <- debug_size
  }else {
    n <- n_results
  }


  # TODO chunk this to be safer if it doesn't work

  # download actual data (titles and texts)
  df <- download_with_progress_bar(results, language, n)
  #print(df)

  # convert the df to jsonl
  jsonl <- toJSON(df)
  #cat(jsonl)

  # write jsonl to file
  dir.create(language, showWarnings = FALSE) # don't show a warning if it exists already
  file_name <- paste(language, "/", resource_type, ".jsonl", sep = '')
  write(jsonl, file = file_name)
  print(paste("Saved downloaded data to", file_name))


  return(df)
}

# example usage
df <- download_and_save_resource_type("caselaw", language = "de", debug = debug)


# Approximate number of entries for English:
# regulation:     ~140K
# caselaw:        ~100K
# decision:       ~53K
# proposal:       ~29K
# recommendation: ~3K

# EU Languages with iso codes
# Bulgarian	    bg
# Croatian	    hr
# Czech	        cs
# Danish	    da
# Dutch	        nl
# English	    en
# Estonian	    et
# Finnish	    fi
# French	    fr
# German	    de
# Greek	        el
# Hungarian	    hu
# Irish	        ga
# Italian	    it
# Latvian	    lv
# Lithuanian	lt
# Maltese	    mt
# Polish	    pl
# Portuguese	pt
# Romanian	    ro
# Slovak	    sk
# Slovenian	    sl
# Spanish	    es
# Swedish	    sv

# Final run through
languages <- c("de", "fr", "it", "es")

resource_types <- c("directive", "regulation", "decision", "recommendation",
                    "intagr", "caselaw", "manual", "proposal", "national_impl")

if (FALSE) {
  for (resource_type in resource_types) {
    for (language in languages) {
      df <- download_and_save_resource_type(resource_type, language, debug = debug)
    }
  }
}

# Run the script with "R CMD BATCH download_eurlex.R"