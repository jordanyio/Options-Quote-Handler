# Options-Quote-Handler - OQH
 The script reads and processes option tickers from CSV files, filters and writes the processed data to new CSV files,
 executes subprocesses for data clearing and additional data processing, and measures the total elapsed time for the script to run.
The script has asynchronous and multi thread functionality. 

Makes use of the polygon.io API. 

It iterates over each ticker and performs the following actions:
  Reads a CSV file ({ticker}calls_processed.csv) into a pandas DataFrame.
  Handles potential exceptions related to empty data, parsing errors, or index errors.
  Filters and processes the DataFrame by removing rows with specific conditions.
  Filters the DataFrame further based on additional criteria.
  Writes the filtered DataFrame to a CSV file ({ticker}calls_filtered.csv).
  Executes multiple subprocesses asynchronously 
  Prints a message indicating that the clearTrades.py subprocess is completed.

The csv file that OQH reads is populated by the GetOptionTickers.py file, which uses the yahoo finance api to 
get tickers that meet the desired conditions.

The OQH gets real time screenshots for each ticker and outputs them to a csv file
Once it completes writing to this file, another method reads that file and acts if its conditions are met.

$$ Future Plans $$

Build a database to replace the csv files

Remove subprocesses, use oop methods to call functions instead of running subprocesses with other scripts.





  
