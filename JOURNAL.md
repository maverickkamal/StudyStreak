---
title: "StudyStreak"
author: "Maverick"
description: "A desk device for healthier study habits using ESP32, presence sensing, and an OLED display."
created_at: "2025-05-31" 
---

## May 31

It is my first hardware project. I have been thinking of trying out onboard since I joined hackclub, but I never got a chance.
I think this highways is my best shot. I am currently planning and synthesizing stuff. I wanted something original that's why I didn't start with the starter project.
I am currently vetting my plans. I have a solid Idea already thanks to my buddy that knows a lot about hardware :)
I will be frank I have an AI partner that helps me in brainstorming. My journal is original, and this is just the beginning. 

[No Image today ;0]

spend 2hrs

## June 01

I am done with my plans, but I gotta still research parts that are needed. 
I was confused at first thinking we need to make the full project before submitting. I have to check the highway guidelines once more
and I think I just have to design and make BOM. I set up the MicroPico extension on vs code and switch stubs to ES32. 
I will be using python instead of C++ until. I will switch when I am more comfortable with my shitty skills in C++. I suck at it.
I faced some errors initially and I find out it's fine since the hardware ai't connected. 

![alt text](images/image.png)

![alt text](images/image-1.png)

I started coding some firmware offline for now. I made pomodoro logic and idk if i's gonna work that well but I made it just in case.

![alt text](images/image-2.png)

A sneak peak hehe
I will check if my plan needs change but for now see ya tmr

spend 3hrs

## June 02

I started today with a block diagram of how I will connect my stuffs. I started sketching on my journal
I then remember excalidraw and I immediately discard my journal to use it. I did some research initially, 
and thanks to AI for clarifying things. I spent an hour and half making the block diagram. I ensure it's readable
I spent extra 10 mins taking out useless aesthetics I add like colors. 

![alt text](images/studystreak_sketch.png)

I love this block diagram. it is pretty ngl. it wasn't easy stopping at this hehe
After I tested my shitty code and as expected a bit buggy. I ran some test and confirm some issues with my logic and I made some fixes.
I spent 2 hrs debugging as I added like 20 print statement just to get the exact error location. I did spent extra time cleaning the 
print statement. I ran the last test and yay it's working from python's end :|
Now I make the main orchestrator which is the main_controller.py
it was easier to implement as mostly it is place holders and part of pomodoro logic. 
I am cworking in parallel cuz I just made my BOM template on google doc. I cover some part as it was just rough hehe

![alt text](images/bom1.png)

spent 5hr 20mins

## June 03

I did a lot of coding today as I spent time making some of the firmware. I made a handler for TCRT5000 Sensor Module tho no hardware integration yet. I spent sometime research how to work with the sensor to detect presence. I made a generic presence class.
I improved pomodoro logic just added short break to the class. I made handler for the WS2812B RGB LED, SSD1306 OLED Display Module, and TTP223 Capacitive Touch Sensor Module just like tcrt5000 no hardware connection just a class ready to work with them. I had to do a lil bit of research just to make sure things work. it didn't work straight away lol. I faced some bugs that are stupidly easy but hard to find. I ran several test and some still failed so I am stopping here for today. I put them together in the main controller, and I added lots of print statement just for debugging. 

![alt text](images/image-3.png)

I am also gathering datasheet for my componenets to understand some stuffs about them. I think this is where everything will get hot. i gotta read them still. Not all but part of it. I will journal anything I find interesting here.

spent 4hr 12mins

## June 04

I went through the datasheets, and I was hit by technical details I know nothing about. I spent time on youtube and other tools that could help me understand those sheets. It was frustrating because I don't even know where to start at first, so I started anyways exploring the diagrams first. wihout yapping too much lemme jot some key stuffs I found useful to my project.

#### ESP32-DevKitC V4 (with ESP32-WROOM-32)

It will be the power sources of most of the components. Some utilizes 3.3V output (for OLED, TCRT5000, TTP223) and some 5V output (from USB, for WS2812B). The logic level is 3.3V. I figure out the tentative pin assignments for StudyStreak, here are they;
- OLED SDA - GPI021
- OLED SCL - GPI022
- WS2812B Data - GPI04 (Idk just the one I like)
- TCRT5000 Analog Out - GPI034 (ADC1-CH6, input-only)
- TTP223 Outpu - GPI013 (not concluded)
I find out i gotta avoid some pins as they are used for flash memory like GPIOs 6, 7, 8, 9, 10, 11 etc
Some buttons I saw in the sheet are EN(Reset), Boot (Download mode)

![alt text](images/esp32_diagram.png)

The diagram is colorful and cool

#### 0.96" I2C OLED Display

The module have a SSD1306 Controller with 128x64 pixels (my mobile is 3200x1440 😭😭) anyways i'm not making a phone. It uses I2C Interface which is suitable and as provided above I will be sticking to 3.3V for operating voltage (it supports up to 5V). for the pinout I'll do
- VCC (connect to ESP32 3.3V)
- GND (connect to ESP32 GND)
- SCL (connect to ESP32 I2C SCL pin like GIO22)
- SDA (connect to ESP32 I2C SDA pin like GPIO21)
I want to use 0x3C for the I2C Address since it's 7-bit address tho some libraries, according to a certain source, might refer to 0x78 if they mean the 8 bit address idk I still didn't get it.

![alt text](images/oled_diagram.png)

The diagram here is kinda b&W

#### TTP223 Capacitive Touch Sensor Module

My fav module. It was the easiest to grasp since it's a touch sensor it makes sense. The operating voltage ranges from 2.0V to 5.5V, but i'll use 3.3V to stay on a safe point. for the pinout we'll do 3 lol
- VCC (connect to ESP32 3.3V)
- GND (connect to ESP32 GND)
- OUT (signal - connect to a digital GPIO on ESP32 like GPIO13)
I am still trying to understand the output behaivior but seems I will go with the common one. Active HIGH means OUT pin goes HIGH when touched, LOW otherwise. Momentary means OUT pin is HIGH only while touched. Here is the schematic diagram 

![alt text](images/ttp223_diagram.png)

ughh my neck hurts damn

#### WS2812B Addressable RGB LED

uhmm this doesn't support 3.3V operating voltage at all so we are using 5V instead tho it ranges 3.5V to 5.3V. It works with data input logic level which requires VIH of at least 0.7*VDD. if VDD=5V, VH_min = 3.5V. we'll use the following pinout
- VDD (power - connect to ESP32 5V)
- VSS (ground - connect to ESP32 GND)
- DIN (data input - connect to ESP32 GPIO like GPIO4)
- DOUT (data output - not used for a single LED)
I will use a single data line for control which is specific timing protocol (handled by neopixel library). The data format is 24 bits per LED, GRB color order.

![alt text](images/ws2812b_diagram.png)

#### TCRT5000 Reflective Optical Sensor

This is also my fav module. It senses reflected IR or Infrared light as a means to detect something. the likely pinout I will consider
- VCC (connect to ESP32 3.3V)
- GND (connect to ESP32 GND)
- AO (Analog Output - connect to an ESP32 ADC pin like GPIO34)
- DO (Digital Output - will be optional, it may not use if AO is available and preferred)
The operating voltage I'll use is 3.3v even tho it ranges from 3.3V to 5V. The output behavior esp AO which I assume common pull up config on module. So, the voltage decreases with increased reflection or presence of an object. If no object = AO voltage is HIGH, near VCC. if Object present = AO voltage is LOW. Tho the sensitivity and specific voltage range will kinda need calibration with the actual hardware

phew a marathon today.

spent 7hrs (estimated)

## June 05

Uhmmm I gotta sleep guys 

![alt text](images/call.png)

