# Track 158: Taxis #

### RUNNING THE PROGRAM ###

Required Software: Python2, Max Cycling '74.

Note: Later versions of Python are not compatible with `OSC.py`; use Python2 with the `python` command.

1. Open `taxisounds.maxpat`. Make sure the `ezdac~` sound is turned on (the speaker color is light blue) and the `gain~` volume is adjusted accordingly.

2. In a Terminal window, enter the main project directory containing all the files for the program (if the project was downloaded in the home directory, `cd ~\track158-taxis`).

3. Run `python run.py arg1 *arg2 *arg3 *arg4`, with up to four arguments (four taxis) that correspond to the CSV file(s) you wish to run the program with. (Note: `arg1` is required, `*arg2 *arg3 *arg4` are optional.)

    * Example: `python run.py output3.csv output2.csv output4.csv output1.csv` OR `python run.py output2.csv output1.csv`

4. To end the program early, use keyboard command `CONTROL + C` in the Terminal. To clear any remaining sounds after halting the program, run `python reset.py` in the Terminal to reset the UDP sockets until the next call to the program.

### ABOUT ###

UC Berkeley | 
Course: MUSIC 158A - Sound and Music Computing with CNMAT Technologies | 
Semester: Fall 2015

Assignment: "Create something cool in Max."

This program was inspired by Chris Whong's [NYC Taxis: A Day in the Life](http://nyctaxi.herokuapp.com), a data visualization of a single NYC taxi over 24 hours, and his open source GitHub repository: [taxitracker](https://github.com/chriswhong/taxitracker).

Using the Google API polyline-encoded files from [2013 NYC Taxi Trip Data](http://www.andresmh.com/nyctaxitrips/), a Python script unpacks these data files and translates the taxi's movements into sound by tracking its unique path across New York City. The polylines in the CSV files are unpacked; timed OSC bundles of polyline-decoded taxi movements are created; and the relevant information, such as the longitude and latitude coordinates, are sent to Max. In Max, four voices are set up to track up to four taxis' movements at a time, with each of their sound paths layered together. The latitude, longitude coordinate pairs are scaled in two ways to set up the waveforms and frequency. Whether or not the taxi is currently full or currently empty, and how many passengers the cab is carrying, determines the amplitude.

WAVEFORMS: The taxi's X and Y coordinates are scaled from 0 to 1, according to the RBFI patch dimensions. Depending on the taxi's location in the RBFI UI and the locations of the four waveform points, different waveforms (cycle, sawtooth, triangle, and rectangle) are weighted in the RBFI (radial basis function interpolater) patch by its proximity to each of the individual waveform's inner radius.

FREQUENCY: A list of steps for a two-octave chromatic scale and a list containing starting pitch 'C' for four octaves is set up. The taxi's current Y coordinate is scaled from the single trip's start and end Y coordinates (or the minimum and maximum Y coordinates of taxi's total trips) to a number between 0 to 16, mod 4, taken as the index for the base note in the list of octave starting pitches. The taxi's current X coordinate is scaled from the trip's minimum and maximum X coordinates of the taxi's total trips (or the single trip's start and end X coordinates) to a number between 0 and 14, taken as the index for the step/note away from the base note in the octave.

AMPLITUDE: Depending on if the taxi is currently full or empty, the amplitude will be set to a higher or lower amplitude, respectively. The more passengers in the cab during the trip, the more dominant the amplitude will be.
