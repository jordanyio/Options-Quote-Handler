import pandas as pd
import datetime 
import time as t
import subprocess
from concurrent.futures import ThreadPoolExecutor

tickers = ['TSLA', 'AAPL', 'NVDA', 'AMZN', 'MSFT']

now = datetime.datetime.now()
start_time = t.time()

for ticker in tickers:
    filename = (f"{ticker}calls_processed.csv")

    try:
        df = pd.read_csv(f"{ticker}calls_processed.csv")
    except pd.errors.EmptyDataError:
        print("c.Err.18.empty")
    except pd.errors.ParserError:
        print("c.Err.20.fixData")
        df = pd.read_csv(filename, on_bad_lines='skip')       
        df = df[df.count(axis=1) == 8]
        df.to_csv(filename, index=False)              
    except IndexError:
        print('c.Err.25.index')            
        pass     
                
    df = df[(df['Strike'] != 0) & (df['mid'] != 0)]
    df['Strike'] = df['Strike'].astype(str).str.replace(",", "").astype(float)
    df['Strike'] = df['Strike'].astype(float)
    df['mid'] = df['mid'].astype(float)

    try:
        p = float(df.iloc[0, df.columns.get_loc("p")])
    except Exception as e:
        print("c.err.", e) 
        t.sleep(1)
        pass 

    df["P/L"] = 0 # P/L must be calculated here. 
    filtered_df = df[(df["P/L"] >= -200) & (df["Strike"] >= 101) & (df["mid"] != 0)]
    filtered_df = filtered_df.sort_values("P/L", ascending=False)
    filtered_df = filtered_df[filtered_df['P/L'] >= -500]

    # Write the header row to the file
    filtered_df.head(0).to_csv(f"{ticker}calls_filtered.csv", index=False, header=True, mode="w")
    # Write the header row to the file, starting from the third column
    # filtered_df.iloc[:0, 2:].to_csv(f"{ticker}calls_filtered.csv", index=False, header=True, mode="w")
    # Write the remaining rows starting from the second row
    filtered_df.iloc[2:].to_csv(f"{ticker}calls_filtered.csv", index=False, header=False, mode="a")
    # Write the remaining rows starting from the third column
    # filtered_df.iloc[2:, 2:].to_csv(f"{ticker}calls_filtered.csv", index=False, header=False, mode="a")

    subprocess.Popen(["python", "polyApi/clearTrades.py"]).wait()
    print(f"clearTrades for {ticker} is done")

with ThreadPoolExecutor(max_workers=len(tickers)) as executor:
    futures = []
    for ticker in tickers:
        futures.append(executor.submit(subprocess.Popen, ["python", f"polyApi/conData{ticker}.py"]))
    for future in futures:
        future.result()

subprocess.Popen(["python", "polyApi/sortTrades.py"]).wait()
print("sortTrades is done")

end_time = t.time()
elapsed_time = end_time - start_time
print("Total elapsed time:", elapsed_time, "seconds")
