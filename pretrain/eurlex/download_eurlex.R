# install.packages("pdftools")
# install.packages("eurlex")
# install.packages("jsonlite")
# install.packages("xml2")
# install.packages("slackr")


library(eurlex)
library(dplyr) # my preference, not needed for the package
library(jsonlite)
library(stringr)
library(slackr)

slackr_setup()


debug_size <- 12
debug <- FALSE
verbose <- FALSE


download_with_progress <- function(results, language, resource_type, n, chunk_size = 1000) {
  error_counter <- 0

  log <- function(string) {
    print(paste(format(Sys.time(), "%Y-%m-%d %X:"), string))
  }

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

  download_chunk <- function(chunked_results, df) {
    titles <- c()
    texts <- c()
    languages <- c()
    for (i in seq_along(chunked_results)) {
      titles <- append(titles, safe_fetch(chunked_results[i], "title"))
      texts <- append(texts, safe_fetch(chunked_results[i], "text"))
      languages <- append(languages, language)
    }
    df['title'] <- titles
    df['text'] <- texts
    df['language'] <- languages
    df <- df %>% select(celex, language, date, title, text)
    return(df)
  }


  dir.create(language, showWarnings = FALSE) # don't show a warning if it exists already
  file_name <- paste(language, "/", resource_type, ".jsonl", sep = '')
  print(paste("Download progress (saving downloaded data to ", file_name, "):", sep = ''))


  for (start in seq(1, n, chunk_size)) {
    end <- min(start + chunk_size - 1, n)
    chunked_results <- results$work[start:end]
    df <- slice(results, start:end)
    df <- download_chunk(chunked_results, df)
    log(paste(end, "/", n))

    # append to the jsonl file
    for (row in seq_len(nrow(df))) {
      json <- toJSON(df[row,]) # make row to json
      json <- str_sub(json, 2, -2) # remove first and last characters ([ and ])
      cat(json, file = file_name, append = TRUE, sep = "\n")
    }
  }
  print(paste("Encountered errors (saved NA) for", error_counter, "entries."))
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

  # download actual data (titles and texts)
  download_with_progress(results, language, resource_type, n)
}

# example usage
# download_and_save_resource_type("recommendation", language = "de", debug = debug)


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
if (TRUE) {
  languages <- c("bg", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "hu", "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "es", "sv",)

  # sorted in ascending order of size
  resource_types <- c("recommendation", "directive", "intagr", "proposal", "decision", "caselaw", "regulation")
  # "manual" and "national_impl" are not working

  for (language in languages) {
    for (resource_type in resource_types) {
      message <- paste('Started downloading language', language, 'and resource type', resource_type)
      slackr_bot(message)
      download_and_save_resource_type(resource_type, language, debug = debug)
      message <- paste('Finished downloading language', language, 'and resource type', resource_type)
      slackr_bot(message)
    }
  }
}

message <- paste('Script finished completely for the languages', paste(languages, collapse = ", "),
                 'and the resource types', paste(resource_types, collapse = ", "))
slackr_bot(message)


# Run the script with "R CMD BATCH download_eurlex.R"
