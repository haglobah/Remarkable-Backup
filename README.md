# Remarkable Backup Tool

This is a simple script that lets you automatically recreate the directory structure of your remarkable and export `PDFs` of all of your notebooks, along with storing complementary metadata and `.rm` files.

To use, install the basic requirements by creating and entering a virtual environment and running `pip install -r requirements.txt`. Then go to `config.py`and set the `password` and `username` of your remarkable tablet to the SSH login of the tablet, which can be found in the about section of the tablet.

Finally, run `backup.py`. It will create an `output` directory with two folders: `trove` and `dump`. Dump is a direct copy of ALL of the contents of your remarkable, in case you break the tablet and need to clone your data to a new tablet. Trove is a recreation of the directory structure of your tablet with PDFs and complementary ZIP `.rm` packages meant for your viewing.

The tool uses the USB web interface to render `PDF`s from `RM` files, and direct SSH to export the additional metadata files.

![image](https://github.com/404Wolf/remarkableBackup/assets/108041238/1d08023e-5149-4a62-809b-3cc46b272414)
![image](https://github.com/404Wolf/remarkableBackup/assets/108041238/5a510145-68d0-4c2f-b24f-f87da0c48371)
![image](https://github.com/404Wolf/remarkableBackup/assets/108041238/e6851697-8f4e-4b50-8fb6-be37ce36f545)
