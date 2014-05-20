[NiceData](http://glacial-peak-3884.herokuapp.com/ "Link to Demo")
=========
![alt tag](https://dl.dropboxusercontent.com/u/45206361/NiceData_Prototype.png)
About
=========
A project for quickly creating financial graphics and analyses based on historical data. It pulls timeseries data from Yahoo! Finance, and builds charts using matplotlib with custom styling. 

Ticker data displayed using jqGrid and Quandl can be viewed on the side panel, with export feature to be implemented soon.

I decided to include an exact ticker data feature using jqGrid and the Quandl API. I'll provide the option to export to CSV shortly.

This project has a MVP that is hosted [here](http://glacial-peak-3884.herokuapp.com/).
TODO
=========
- Implement frontend interface for moving average, maybe bollinger bands.
- Pull XBRL data for companies and automate spreadsheet creation.
- Implement CSV Export
- Create repo for Quandl CSV to jqGrid formatter
- Minor aesthetic changes: Enlarge header, change bg image