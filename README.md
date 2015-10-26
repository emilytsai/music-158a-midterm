# music-158a-midterm

Track 158: Taxis

To run the program:
1. Open maxFile.maxpat.
2. In Terminal, cd into the main project directory and run 'python run.py arg1 *arg2 *arg3 *arg4', with up to four arguments (four taxis) that correspond to the CSV file(s) you wish to run the program with. (Note: arg1 is required, arg2/arg3/arg4 are optional)
Example: 'python run.py output4.csv output3.csv output1.csv output2.csv'

* NOTE: Later versions of Python are not compatible with OSC.py, please use the 'python' and not 'python2' or 'python3' commands.


This program is inspired by Chris Whong's [NYC Taxis: A Day in the Life](http://nyctaxi.herokuapp.com), a data visualization of a single NYC taxi over 24 hours, and his open source GitHub repository: [taxitracker](https://github.com/chriswhong/taxitracker).

Using the Google API polyline-encoded [2013 NYC Taxi Trip Data](http://www.andresmh.com/nyctaxitrips/), the polylines in the CSV files are unpacked, timed OSC bundles of polyline-decoded taxi movements are created, and the longitude and latitude coordinates are sent to Max. In Max, four voices are set up to track up to four taxis' movements.
