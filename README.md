# nypdCrashData
A web application that maps NYPD crash data utilizing OpenStreetMap and its clustering feature.

Root URL will provide crash data from the last 14 days.  Use /days/XX to set a custom range (NOTE: page loads will take longer for larger day ranges... See TODO below for future work on this).

TODO: Currently, the data query is made upon the URL request.  The goal will eventually be to move this to a task handler that periodically queries data throughout the day and stores in server-side.

TODO: Improve data infoboxes

## Overview Map
![alt text](https://raw.githubusercontent.com/cheebz/nypdCrashData/master/nypdCrashData/screenshots/NYC%20Crash%20Data%201.JPG)

## Data Points
![alt text](https://raw.githubusercontent.com/cheebz/nypdCrashData/master/nypdCrashData/screenshots/NYC%20Crash%20Data%202.JPG)
