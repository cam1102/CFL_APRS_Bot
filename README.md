# CFL_APRS_Bot

Preparing for Use

_Hardware Preparations:_
As the program depends on serially connected devices to operate, these devices must be connected and turned on before use.


1) Connect APRS Radio:
While this radio may change, in development, the Kenwood TH-D74 was used. The serial output was enabled (See Kenwood User Guide for instructions on doing this) and the radio was plugged into the computer over Micro-USB. The Radio should be fully charged or on a power dock before flight. While normal APRS on the 144.390 is standard, we cannot transmit fast enough on this frequency to adequately track the balloon due to regulations on this national frequncy. For this reason, we have a separate transmitter beaconing once every 5 seconds on the 144.350 frequency that will be more acceptable for tracking purposes.

2) Port Check: The Python script relies upon all these peripherals running on the correct ports. Upon plugging in these peripherals the first time, use the “ls /dev/tty.*” command to list out the connected Serial Ports

The Kenwood Serial Port is usually /dev/tty.usbmodemXXXXXX. Before running the Python script, check that the correct port is being used on line 69.

Software Preparations:
Before running the Python script, multiple libraries and dependencies must be installed on the use computer, and the computer requires an Internet connection.

1) Install Dependencies:

a) APRSLib (https://pypi.org/project/aprslib/)

b) what3words (https://developer.what3words.com/tutorial/python), My API key will be sent later.

c) slack_sdk (https://slack.dev/python-slack-sdk/), You already have access to this token.


2) Pass in environmental tokens to start the script...

SLACK_BOT_TOKEN="xoxb-restoftoken" 3WORDS_TOKEN="tokenhere" python3 APRSTrack.py

If script is working, all 5 bot run channels should start up and start reporting.
