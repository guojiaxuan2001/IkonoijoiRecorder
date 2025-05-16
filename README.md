This is a simple catcher for Ikonoijoi events.

Would enhance the analyze efficacy with LLMs further.

+ I plan to optimize the logging system by improving SQL queries and develop a frontend for better data access.
+ I am planning to enhance the record management by optimizing SQL and building a frontend UI.

#Version1.1 Update Summary:#
+ Optimized the Twitter scraping logic to avoid repeated processing and infinite loops.
+ Now, only newly appeared tweets are processed during each scroll, ensuring no duplicates.
+ Each captured tweet’s content is printed in the logs for easier debugging and verification.
+ The scroll count is strictly limited, and scrolling stops early if no new content is loaded.
+ These changes make the script more efficient, stable, and user-friendly for data collection and Google Sheet export.
