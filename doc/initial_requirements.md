Architecture:
    - Finite number of parallel crawlers
    - In memory DB to store links to crawl next
    - Scheduler to manage crawlers
    - Persistent DB to hold an index of crawled links ==> [Key: URL, Document: <HTML DOC>, Freq: # of days]
    - API to consume links and return the HTML Document
    - Thread to consistently go through the DB to update any expired documents


TODO:
   - Schedule meeting time
   - Talk to link analysis & text transformation to see how our API should interact with them
