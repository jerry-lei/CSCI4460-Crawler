## Architecture:
   - Finite number of parallel crawlers
   - In memory DB to store links to crawl next
   - Scheduler to manage crawlers
   - Persistent DB to hold an index of crawled links
      - Key: URL
      - Freq: # of days
      - Timestamp: Last time it was updated
      - Result: Success/Failure
   - Thread to consistently go through the DB to update any expired documents


## API Requirements
   - API to consume links and return the HTML Document
      - Link Analysis calls our HTTP endpoint
      - Push to text transformation on success
      - Return success/failure to link analysis


## TODO:
   - Schedule meeting time
   - Talk to link analysis & text transformation to see how our API should interact with them