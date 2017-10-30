# ClusterRateWatch

This code is from a project that I did for the University of Aizu's Creative Factory Seminar in 2017. It uses a simple clustering algorithm to monitor the most recent acceleration activity provided by a CAN bus simulation board.

## What It Does/How It Works

The code analyzes a 29-bit extended CAN frame generated by a simulation board and software and strips the header information out for speed data. Each message from the board has an Rx/Tx identifier, header, and data payload. It looks something like this:

```
Tx: 18DAF110 04 41 10 0C E0
```

The Rx/Tx portion, header, and other redundant information is stripped away, leaving the speed data. From there, we calculate the derivates between speed values, which shifts our focus from observed speed to observed acceleration.

These data are handled using a simple clustering algorithm, preserving each new entry in a data set, and preserving only the three latest data sets. The collected speed values and derivate values utilize their own data sets.

### Back-end

The back-end is done in Python. There are two files in Python; one is for the actual data analyzer, and the other is for the server running on localhost that connects the back and front-ends together.

### Front-end

The front-end is a simple HTML page that posts the latest three average derivative rates collected by the algorithm. The code then interprets the data based on four likely outcomes:

* constant reading, indicating no change in acceleration
* standard acceleration or deceleration
* a possibility that something malignant has happened involving the car's network
* very brief junk traffic that more likely could have been generated as a result of technical error

## Getting Started

### Prerequisites

All versions specified have been confirmed to work with the project. (Because this is not overtly complex code, using later versions should have no effect on the program's operability.)

* Python 2.7.13
* Pip 9.0.1
* Flask 0.12.2
* OBDwiz 2.16.3.959

Because OBDwiz is proprietary and restricted to Windows machines only, it is recommended to run this code on a Linux VM (I used Lubuntu 17.04 via VirtualBox) while running OBDwiz on your Windows host.

The project utilized a ScanTool ECUsim 2000 OBD Simulator with the ISO 15765 (CAN) protocol and an OBDLink SX Cable. If you can find a board that produces the same kind of output as specified in "What It Does/How It Works", you can try using that, too.

### Install

After installing the prerequisites, just clone the project on the VM:

```
git clone https://github.com/wputnam/ClusterRateWatch.git
```

and run it. No compilation necessary.

### Run

Be sure to specify in the source code which COM port the board itself will be using. You will also need to enable that COM port in the VM settings.

First, with both the terminal and OBD cables connected to the computer, launch OBDwiz, and  connect to the board. Use the EngineControl monitor settings. This will start generating the data that the board will produce over the terminal.

Then, on your VM, navigate to the project directory in your terminal and type:

```
sudo python server.py
```

to get the server started. Keep the tab open or relegate it to the background; it's your choice.

Finally, in your browser, navigate to `localhost:5000`. This will launch the collection script and will start reading in the data. Give it at most two seconds for meaningful data to start generating.

## Future Development and Contributions

There probably won't be for this specific project. (It's also my first solo Git project, so please excuse the sloppiness.) I intend, however, to use the algorithm as part of my master's thesis research.

If I had more time to devote to this project, I would try to allow the code to collect information for other analytics such as engine RPMs, engine temperature, and MAF sensor. I would also convert it over to JavaScript, which I tried to do before, but had to abandon due to the board's weird behavior with the serial libraries on both Windows and Linux.

That being said, if you have nothing else to do with your time and wish to improve on what I have here, feel free to add a merge request. (I would especially appreciate it if someone can figure out how to use the project using nothing but open-source hardware and software.)

## Authors

* **William Putnam** - *Program design and coding* - [wputnam](https://github.com/wputnam)

## License

This project is licensed under Apache 2.0. A copy of the license is included in [LICENSE.md](LICENSE.md).

## Acknowledgments

* Prof. Akihito Nakamura, the supervisor for the project
* Yilang Wu, for inspiration with the program design