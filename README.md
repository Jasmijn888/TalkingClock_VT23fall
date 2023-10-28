# Talking Clock (VT23)

## Introduction

This 'talking clock' provides an interface to a clock with several features. It was developed as the final assignment for the courses Introduction to Programming and Introduction to Voice Technology, part of RUG's MSc Voice Technology.

## Dependencies

The following libraries / modules are required to successfully run the clock:
- tkinter: https://docs.python.org/3/library/tkinter.html
- pillow: https://pillow.readthedocs.io/en/stable/
- pyttsx3: https://pyttsx3.readthedocs.io/en/latest/
- pytz: https://pythonhosted.org/pytz/
- playsound: https://pypi.org/project/playsound/
 
## Installation and Setup
 Before installation, make sure that:
 1. Python (3.10 or above) is installed on your device: https://www.python.org/downloads/
 2. All required dependencies are installed on your device.
 
## Usage

Once all necessary libraries are installed, the clock can be run by executing the python script in your terminal or IDE. The clock interface will appear, displaying the current time, and there are several buttons you can interact with to make use of the clock's features.

### Features

#### Clock style:
The graphical clock display has two face styles. These can be navigated via the button 'Switch style'.

#### Read time aloud: 
Using the 'Read time' button, the current time can be spoken out loud. For this, multiple languages are supported: Chinese, German, English.

#### Time zone selection:
The clock can be set up to display the current hour in a different time zone than the local one (e.g. Shanghai, Berlin). 

#### Alarm setting:
The 'Set Alarm' button allows the user to set an alarm at the desired time, as well as to choose the ringtone out of three options.

## Authors and distribution of roles

###### Jasmine:
- overseeing project timeline and ensuring adherence to schedule.
- addressing cross-functional issues.

###### Jocomin and Janice:
- implementing the core functionality of the clock.
- audiofile recordings and integration of audio into the clock functionality.

###### Weihao, Qing:
- implementation of user interface and customization.
- implementation and functionality of features.

###### Maria:
- writing up documentation.
- code commenting.
