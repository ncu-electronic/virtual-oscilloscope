# Virtual-Oscilloscope-NCU
A virtual oscilloscope that supports multiple data source protocols.
Written in python3 and PyQt5.

## How to use:
### 1. Install dependencies:
[*pyqtgraph*](http://www.pyqtgraph.org/)

[*PyQt5*](https://pypi.python.org/pypi/PyQt5)

**Install with pip:**

`pip3 install PyQt5, pyqtgraph`

**In addition**, on linux users should install ***qt5-serialport*** package to obtain the qtserial.so shared library, this name is specific for the "pacman" package manager on arch linux, it may be different on other linux distributions.

### 2. Run it:
`python3 main.py`

## Current data procotol:
Currently, data is transfering through serial port.

And at present we'll use one 8 bit to represent a certain data number, so it'll be restrained in 0~255, there is temporarly no other thing.

**Demonstration:**

Send square waveform data by arduino, source code:
```
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0x01);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
}
```

## Documention:
https://ncu-electronic.github.io/virtual-oscilloscope/

## Screenshots
![alt_text](https://github.com/ncu-electronic/general_instrument_gui/raw/master/screenshots/2018-10-02-065207_1920x1080_scrot.png)
