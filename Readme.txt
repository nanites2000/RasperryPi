Fisrt download NOOBS and extract onto the sd card using a sd card reader
Insert the microsd into the pi.
It should load up a boot menu when turned on
FIRST THING TO DO BEFORE SELECTING AN OPERATING SYSTEM
IS CLICK THE WIFI BUTTON.  ENTER user-euser password- Blendpiper1 
THEN CLICK THE LANGUAE BUTTON AT BOTTOM.  SELECT ENGLISH-US
now pick the operating system-
select the first option raspbian and then click install



Now in the terminal (the button is on the taskbar) you need to set the default python to python 3:
type in:
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
and
note:the 3.5 3 could cahnge to a newer version at any time
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 3
then if you type:
python --version
it should respond Python 3.5


use pip install xxxxx to install the packages in the terminal
you need matplotlib and cairocffi (which is needed to run on the pi I guess)
also 
sudo apt-get install libatlas-base-dev

Possibly other packages too by the same means.


you should then get a usb drive, plug it into a running pi and copy off the python folder
and both CycleTracker files on the desktop.  Then copy them onto the new pi in the same locations
on the desktop.




Then you can install GIT if you want to and link it to Bitbucket
you can install sqlite with the following:
   sudo apt-get install sqlite3


