# ACD – A Mark Fisher ACD Trading System Implementation

## Project Title & Description
**ACD** is an algorithmic trading analysis system based on Mark B. Fisher’s ACD trading methodology from *The Logical Trader*. It provides a software implementation of Fisher’s ACD system, which identifies key price levels (the “A”, “B”, “C”, and “D” points) derived from the market’s opening range to signal trade entries and exits ([Gauging the Strength of a Market Move With the ACD System](https://www.investopedia.com/articles/technical/04/040704.asp#:~:text=,commodities%20such%20as%20crude%20oil)). Fisher’s ACD system is a breakout strategy that uses the opening range of the trading day to set thresholds: **A and C points** mark potential entry levels (breakouts above or below the opening range), while **B and D points** serve as exit or stop levels ([Gauging the Strength of a Market Move With the ACD System](https://www.investopedia.com/articles/technical/04/040704.asp#:~:text=,commodities%20such%20as%20crude%20oil)). By leveraging this logic, the ACD project helps traders spot when a market is trending and generates objective buy/sell signals based on price movements relative to the opening range.

 ([KillZones + ACD Fisher Indicator in TradingView - Free](https://tradingfinder.com/products/indicators/tradingview/killzones-acd-fisher/)) *Example of the ACD system in action: an “A up” breakout (green arrow) signals an uptrend and an entry point once price exceeds the opening range by a set threshold. A confirmed breakout above the higher “C” level (purple arrow) indicates trend strength, while risk is managed by placing a stop-loss just below the corresponding “A down” level (red dashed line at bottom). This illustrates how the ACD method provides clear entry and exit levels to apply Mark Fisher’s strategy in practice.* 

In essence, this project aims to turn the ACD methodology into a usable tool for traders. It fetches market data, calculates the opening range and ACD levels for each trading day, and tracks **“number line” scores** (cumulative plus/minus values over days) to gauge trend strength as described by Fisher. By automating these calculations, **ACD** allows users to analyze stocks or commodities through the lens of Fisher’s strategy – identifying breakout signals (A-ups/A-downs), tracking rolling pivots and number lines, and highlighting when an instrument is in a strong up-trending (+5) or down-trending (−4) condition. This provides a rule-based approach to trading decisions, reducing guesswork and enforcing risk management principles from the ACD system.

## Key Features
- **ACD Signal Generation** – Automatically computes opening range breakout signals. The system determines daily **A-up and A-down levels** (price points above/below the opening range that trigger entry signals) and **C-up/C-down levels** (secondary confirmation breakout points) following Mark Fisher’s rules ([Gauging the Strength of a Market Move With the ACD System](https://www.investopedia.com/articles/technical/04/040704.asp#:~:text=,commodities%20such%20as%20crude%20oil)). When price crosses these levels, the software generates alerts for potential long or short entries. It also identifies when an **A signal** fails and a **D point** exit is hit, indicating a reversal or exit condition.
- **Risk Management** – Incorporates Fisher’s risk control methodology by using predefined exit points and stop levels. For any given trade signal, the corresponding **B or D point** serves as a logical stop-loss level (e.g. if an A-up entry is triggered, a move down through the opening range or a set threshold – the D-down – signals an exit). The system clearly displays these exit levels so traders can manage downside risk. Additionally, the application calculates **pivot range** levels (such as 3-day rolling pivots) to highlight support/resistance zones that aid in setting stop-loss and profit targets.
- **Market Data Analysis** – Integrates with market data feeds to retrieve price and volume information and performs analytical computations. It can download **daily and intraday data** (e.g. open, high, low, close prices) for chosen symbols and then analyze this data to compute ACD metrics. The software also includes tools for specialized analysis, such as **bid/ask spread monitoring** and **volume analysis** (via modules like `bidask.py` and `volume.py`), and relative strength comparison against benchmarks (e.g. comparing a stock’s behavior to S&P 500 via `spyrelative.py`). These analyses help confirm ACD signals by providing additional market context.
- **Trading Alerts and Number Line Tracking** – The system monitors ongoing conditions and highlights when certain thresholds are reached. For example, it keeps a **30-day “number line”** for each symbol – a running score of how many days have bullish vs bearish ACD signals. When a symbol’s number line reaches a significant value (such as **+5** or **−4**), the software can flag this (using scripts like `getalertsLong5plus.py` or `getalertsdwn5plus.py`) as an indication of a strong persistent trend. This helps traders focus on instruments with building trend strength. The alert functionality can filter for various criteria (e.g. “5 consecutive A-up days” or “4 minus days in a month”) and output those signals.
- **User Interface for Analysis** – The project includes a graphical user interface (GUI) built with Qt. The GUI allows users to input a ticker symbol and select date ranges for analysis. It then displays the computed **opening range, A levels, C levels, pivot range**, and current number line value for that symbol. Buttons and controls in the interface (for example, an “Run ACD” button) let users trigger calculations or update data. The GUI presents the results in an organized way – showing today’s ACD levels, recent signals, and even enabling plotting of price charts with these levels overlaid. This interactive interface makes it easier to visualize the trading signals and historical performance of the strategy for a given stock or commodity.
- **Extensibility** – The codebase is modular, allowing new indicators or data sources to be integrated. For instance, the project documentation provides guidelines on **adding new technical indicators** into the analysis pipeline (“How to add a new indicator” guide). Developers can extend the system by writing new Python modules that calculate additional metrics or by modifying the GUI (.ui files) to include new displays and controls. This design enables contributors to adapt the tool for different markets or to incorporate custom tweaks to the ACD methodology.

## Installation & Setup
To get started with the ACD system on your local machine, follow these steps:

1. **Clone the Repository** – Begin by cloning the ACD project from GitHub:
   ```bash
   git clone https://github.com/pantoner/ACD.git
   ```
   Then navigate into the project directory:
   ```bash
   cd ACD
   ```
2. **Install Dependencies** – Ensure you have **Python 3.x** installed, then install the required Python libraries. The main dependencies include:
   - **PyQt5** – for the graphical user interface.
   - **pandas** – for data manipulation and time-series analysis.
   - **matplotlib** – for plotting charts (if you plan to use the plotting features).
   - **tiingo** – the official Tiingo API client for Python, used to fetch market data.
   - (Additionally, other standard libraries like `requests` or `sqlite3` are used; these typically come with Python or will be installed as dependencies of the above packages.)
   
   You can install these using pip:
   ```bash
   pip install pyqt5 pandas matplotlib tiingo
   ```
   *(Alternatively, use a virtual environment or conda environment to avoid conflicts with other projects.)*
3. **Obtain API Access (Tiingo)** – The ACD system uses the Tiingo market data API to pull historical prices. You will need a Tiingo API key (you can get a free API key by creating an account at tiingo.com). Once you have an API key, you should configure the application to use it:
   - Open the configuration or main script (e.g. `runmain4.py`) and locate where the `TiingoClient` is initialized. Insert your API key there (replace any placeholder or sample key in the code with your own). For example:
     ```python
     from tiingo import TiingoClient
     config = {'api_key': 'YOUR_TIINGO_API_KEY_HERE'}
     client = TiingoClient(config)
     ```
     For better security, you can store the key in an environment variable and load it in the code using `os.getenv`.
4. **Database Setup** – No manual database setup is required. The project uses SQLite databases (e.g., `BidAsk.db`, `macroACD.db`) to cache market data and store computed results. These `.db` files will be created/updated by the application automatically. Just ensure the project folder is writable so the program can save data. If you have existing `.db` files provided in the repository (they may contain sample data), you can use them as-is; otherwise, the system will create new ones on first run.
5. **Run the Application** – After installing dependencies and setting up the API key, you can launch the ACD tool. The main interface can be started by running the appropriate Python script. For example:
   ```bash
   python runmain4.py
   ```
   This should open the GUI window for the ACD system. (On some platforms, you may need to specify `python3` instead of `python`.)
   
   If you prefer to run in a headless mode or test specific functionality, you can also execute individual scripts. For instance, running `python getalertsLong5plus.py` in a terminal might print out all symbols in the database that currently have a number line of +5 or higher (indicating strong bullish trends). However, the typical usage is through the integrated GUI for an interactive experience.

## Usage
Using the ACD trading system involves interacting with the GUI to retrieve signals or running the analysis scripts for automated outputs:

- **Launching the GUI**: When you run the main application (e.g. via `runmain4.py`), a window will appear. Start by entering a **stock ticker symbol** (or any instrument supported by your data source) into the provided input field. Select the date range you want to analyze – for example, set the “Start Date” and ensure “End Date” (which could default to today) is correct. You can also choose whether to include the current partial day in analysis (via a checkbox for “Today’s data”, if available).
- **Generating Signals**: Click the button (such as “Run ACD” or “Calculate”) in the GUI to start the analysis. The application will connect to the data provider (Tiingo) to fetch the necessary price data for the selected symbol and date range. It then computes:
  - The daily **Opening Range (OR)** high and low for each day.
  - The **A-up** and **A-down** levels (based on the OR and the predefined breakout threshold for that symbol/market).
  - The subsequent **C-up** and **C-down** levels (typically further out breakout points or used in multi-day calculations).
  - The rolling **Pivot Range** (which may be displayed as “Pivot Range Top/Bottom” – often calculated from the previous days’ highs, lows, and close).
  - The **Number Line** score for the symbol (aggregating recent days’ outcomes into a single bullish or bearish score).
- **Interpreting Output**: Once calculation is complete, the GUI will display the results. You will see numeric values for today’s OR, A levels, C levels, etc., and possibly color-coded indications of any triggered signals. For example, if today’s price exceeded the A-up level, the interface might highlight a long entry signal. If the price then fell back and hit the D-down level, it would indicate an exit. The pivot range and number line provide context – e.g. if the number line is +4 and today triggers another A-up, you might anticipate a “+5” strong bullish condition. All these outputs help you decide on trades: a trader might go long when an A-up is shown and exit if a C-down (stop) occurs, for instance.
- **Charting (Optional)**: The system includes plotting capabilities to visualize price action relative to ACD levels. By running the `plotonesymbol.py` script or using a plot feature in the GUI (if available), you can generate a chart for the selected symbol. The chart typically shows candlesticks for price, horizontal lines for the OR, A-up/A-down, C-up/C-down, and possibly marks where signals occurred. This visual aid is useful for confirming how the strategy played out over time.
- **Batch Scanning**: Beyond single-symbol analysis, ACD can scan multiple symbols for alerts. Using the provided alert scripts (like `getalerts.py` or the specialized `getalertsLong5plus.py` etc.), you can run a batch job that goes through a list of tickers in the database and outputs those meeting certain criteria. For example, you could set up a daily cron job to run `getalertsLong.py` which might output any new A-up signals across your watchlist, or `getalertsdwn5plus.py` to warn of any instrument that has hit −5 on its number line (potentially a strong downtrend worth noting). This is useful for monitoring a broad market with the ACD methodology automatically.
  
Overall, the typical usage pattern is: **fetch data → calculate ACD levels → review signals/alerts → make trading decisions**. The tool does not execute trades automatically; it’s an analysis and decision support system. Users should take the signals and apply their own judgment and risk management (in line with ACD’s guidance) when placing actual trades with their broker.

## Tech Stack
This project is built with a focus on Python and data analysis libraries, as well as GUI components for a user-friendly experience. The main technologies and frameworks include:

- **Python 3.x** – Core programming language used for all strategy logic, data processing, and UI control.
- **PyQt5 (Qt for Python)** – Framework for the graphical user interface. The interface (windows, buttons, input fields, etc.) is designed in Qt Designer (.ui files like `MainWindow6.ui` and `MainWindow8.ui`) and loaded in Python to provide an interactive desktop application.
- **Pandas** – Used extensively for data manipulation. Market data (prices, volumes, dates) are loaded into Pandas DataFrames for calculation of rolling averages, number lines, and other indicators. Pandas makes it easy to compute things like the opening range for each day, or to shift data when computing multi-day pivot ranges.
- **Matplotlib** – Employed for generating charts and visualizations of price data with ACD levels. Some scripts produce plots (for example, overlaying ACD entry/exit points on a candlestick chart) to help users visually verify signals.
- **Tiingo API** – The system relies on the Tiingo financial data API as its data source. The official `tiingo-python` library is used to connect to Tiingo’s REST API ([Mark Fisher Indicator | news.cqg.com](https://news.cqg.com/workspaces/2016/11/mark-fisher-indicator#:~:text=The%20ACD%C2%A0lines%20and%20the%20three,an%20opening%20range%20breakout%20system)), enabling retrieval of historical daily price data for stocks, ETFs, or other supported instruments. This provides the open, high, low, close (OHLC) and volume information needed for ACD calculations.
- **SQLite** – Lightweight database used for storing data locally. The project includes SQLite database files (e.g., `macroACD.db`, `BidAsk.db`) which likely cache historical data and maybe store computed results like number lines or recent signals. Using SQLite allows the app to quickly retrieve past data without re-fetching from the API each time, and to maintain state (such as accumulating the 30-day number line values).
- **Multi-threading** – The application uses Python threads (via Qt’s `QThread`) to keep the UI responsive. For instance, data fetching and heavy computations are done in background threads (`DailyDownLoadThread`, `indicatorThread`, etc. in the code) so that the GUI doesn’t freeze. This results in a smoother user experience when pulling data or running scans on multiple symbols.
- **Other Libraries** – Standard Python libraries like `requests` (for web requests, possibly used under the hood by the Tiingo client), `pickle` (used in code for saving/loading objects or caching), and possibly `numpy` (for numeric operations, often used by Pandas) are utilized. There’s also an `optionvue.py` which suggests compatibility to import/export data with OptionVue (a trading analysis software), indicating the tool might integrate with other platforms or data formats as needed.

Overall, the tech stack is a combination of data science and desktop GUI tools, making ACD a self-contained application for quantitative trading analysis based on Python.

## Configuration & Environment Variables
Configuration for the ACD system mainly involves API keys and adjustable parameters for the trading logic:

- **Tiingo API Key** – As mentioned, you need to provide your Tiingo API key for data access. It’s recommended to store this securely. You can set an environment variable, for example:
  ```bash
  export TIINGO_API_KEY="YOUR_API_KEY"
  ```
  and then modify the code to read this instead of hardcoding the key (e.g., use `os.getenv('TIINGO_API_KEY')` when constructing the `TiingoClient`). This prevents exposing your key in code and allows different environments to easily use their own keys.
- **Default Parameters** – Mark Fisher’s ACD method can have different parameters (like the length of the opening range, or the multiplier for ATR to set A/C levels) depending on the market traded. In this implementation, some of those may be hardcoded or set in config sections of the code:
  - For example, the **Opening Range duration** might be set (15 minutes for equities by default, etc.). If you need to change it (say to 30 minutes), you would update the relevant part of the code or configuration file (if provided).
  - The **threshold for A up/A down** – sometimes expressed as a fixed value or as a fraction of Average True Range. In the code, look for where A levels are calculated. You may find a constant or formula (like `0.25 * ATR` or a fixed point value) that you can tweak to suit different volatility or instruments.
  - **Symbol lists or Sectors** – Some scripts (like `bidasksector.py`) might group symbols by sector or some category. These could be configured via lists in the code or external files. If you want to change which symbols are analyzed, you may need to edit those lists or provide your own list of tickers to the scanning scripts.
- **Logging and Output** – By default, most outputs will either be shown in the GUI or printed to console by scripts. If you want to change verbosity or log to a file, you might configure Python’s logging settings in the scripts.
- **Environment Setup** – Ensure that your environment’s locale/timezone is correctly set if dealing with time-sensitive data (the opening range is time-based). The code may assume market times in a certain timezone (likely US/Eastern for NYSE if dealing with stocks). If you use it for other markets or timezones, adjust any timezone settings accordingly.
- **Proxy/Network** – If you are behind a proxy or have network constraints, you might need to configure the `requests` library or the Tiingo client to use proxy settings. This can usually be done via environment variables (`HTTP_PROXY`, `HTTPS_PROXY`) or modifying the request session in code.

*(Currently, the project does not have a separate config file or .env file – configuration is done by editing constants in the Python scripts. Future improvements might include adding a config file for easier parameter tuning.)*

## Contributing
Contributions to **ACD** are welcome! Since this project is in its early stages (as an open-source implementation with a small user base so far), there are many ways it can be improved or expanded. To contribute, you can:

- **Fork the Repository** – Start by forking the GitHub repo and cloning it to your development environment.
- **Set Up Your Environment** – Follow the installation steps to get the project running. It’s a good idea to create a virtual environment for development and ensure you can fetch data and launch the UI.
- **Identify Improvements or Features** – Issues and enhancements could range from code refactoring and bug fixes to adding new features (for example, integrating a new data source, adding a strategy parameter, or improving the UI/UX). Check if there’s an existing TODO list or issues in the repository; if not, you can also create an issue to discuss your proposed changes.
- **Follow Code Style** – Try to maintain consistency with the coding style present in the project. Use clear variable names and comments especially when dealing with complex financial calculations. Document any new functions or modules you add.
- **Testing** – If possible, test your changes with various scenarios (different symbols, date ranges, edge cases like holidays or missing data). Currently, the project might not have a formal test suite, so manual testing is important. Ensure that your contributions do not break existing functionality.
- **Submit a Pull Request** – Once you have made changes, push them to your fork and open a pull request on the original repository. Provide a clear description of what your PR does, referencing any issue it addresses. The maintainer (or community) can then review your changes. Be open to feedback and willing to make adjustments if requested.
- **Documentation** – If your contribution changes how users interact with the system or adds new capabilities, update the documentation accordingly. This might mean editing the README (for usage instructions, new features) or adding supplementary docs (like an “Adding Indicators” guide if you introduce a new indicator integration).
  
Before contributing major changes, it might be wise to get in touch with the project owner (you can open an issue or discussion) to ensure your efforts align with the project’s direction. Collaboration and clear communication will help your contributions get merged smoothly.

## License
This project is currently not explicitly licensed under any open-source license. It has been published on GitHub as a public repository, but no `LICENSE` file or header is provided in the source code. 

- **All Rights Reserved**: In the absence of a license, the default copyright terms apply – meaning you should not assume free use, modification, or distribution rights beyond fair use. If you intend to use a significant portion of this code in your own projects (especially commercial ones), you should contact the author for permission or clarification.
- **Planned Licensing**: It’s possible that the author may add a license as the project matures (for example, a permissive license like MIT, or a copyleft license like GPL). Keep an eye on the repository README or commits for any update on licensing.
- **Contributing and Forks**: If you contribute to the project, you’re contributing under the project’s terms. Since there is no license, contributors should be aware that their code will be under the same implicit copyright. It’s recommended to discuss with the maintainer if you have concerns about this. 
