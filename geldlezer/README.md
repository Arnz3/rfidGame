# rfidGame

## SETUP

### enable spi

enable spi in config
```
sudo raspi-config
```

test spi
```
lsmod | grep spi
```

### python libs

python3-dev
```
sudo apt install python3-dev python3-pip
```

spidev
```
sudo pip3 install spidev
```

mfrc522
```
sudo pip3 install mfrc522
```


## pin layout

| Element       | pin    | 
| ------------- |:------:| 
| kp 8          | 40     | 
| kp 7          | 38     | 
| kp 6          | 36     | 
| kp 5          | 32     | 
| kp 4          | 37     | 
| kp 3          | 35     | 
| kp 2          | 33     | 
| kp 1          | 31     | 
| SDA           | 24     | 
| SCK           | 23     | 
| MOSI          | 19     | 
| MISO          | 21     | 
| GND           | 6      | 
| RST           | 22     | 
| 3.3v          | 1      | 
| GRN LED       | 15     | 
| RED LED       | 11     | 
| YEL LED       | 13     | 
