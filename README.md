# Amp Trigger Control for CamillaDSP and RaspberryPi using a GPIO pin (forked from igfarm/amp_power for Kasa SmartPlugs)

This project contains a small script to trigger the standyby power of an audio power amplifier using a GPIO pin when connected to CamillaDSP on a RaspberryPi. The "RPi4 + CamillaDSP Tutorial" setup is descirbed in [this thread](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/) of the Audio Science Review website.

The script can use any appropriate GPIO pin. In my case I used GPIO(26).

![raspberry-pi-pinout](https://user-images.githubusercontent.com/5959044/198881674-b7f59858-7659-4ca4-82b4-c1a1d28edce7.png)

The script looks for the status of the playback device on the linux process information pseudo-file system:
```
$ head /proc/asound/card2/stream0
MOTU M4 at usb-0000:01:00.0-1.3, high speed : USB Audio

Playback:
  Status: Stop
  Interface 1
  ...
```

and checks the stream for a `Stop` or `Running` status and uses that to toggle the GPIO pin.

First, clone the library, modify as required and:

```
cd camilladsp
git clone git@github.com:chuckt62/amp_trigger.git
cd amp_trigger
```

Test the script
```
python3 amp_trigger.py
```

After you are satisfied it works, install it as a service. To do this update `amp_trigger.service` to point to the correct path and then:

```
sudo cp amp_trigger.service /lib/systemd/system/
sudo systemctl enable amp_trigger.service
sudo systemctl daemon-reload
sudo systemctl start amp_trigger.service
```

```

