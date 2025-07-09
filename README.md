# MHWVoiceChanger
Allow the reassigning of voices to other voices. This means that any voice or voice mod is compatible with (almost) any other voice!

Powered by the MHW Audio Modding Tool (wwiseutil)

You can download it's latest version in the Releases: https://github.com/ItsBurpee/MHWVoiceChanger/releases

## How to Use:

### File Conversion (Original functionality):
1. Load the .nbnk file with the "Load File" button (It should auto-detect its information in the "Overview")
2. Select the voice to convert to with the "Output Voice" options
3. Click the "CONVERT" button to convert
4. Determine where to save the new .nbnk file
	- This step is skipped if 'Save to "Output"' is enabled

- If the conversion is successful, your new voice file should be in the folder you saved it to
	- If 'Save to "Output"' is enabled, it will be in a folder called "Output" in the same folder as the .exe
- If the conversion failed, you can check the console to see what happened

### Real-time Voice Conversion (NEW):
1. Switch to the "Real-time Conversion" tab
2. Select your microphone from the "Microphone" dropdown
3. Select your speakers/headphones from the "Speakers" dropdown
4. Choose the target voice gender and number you want to convert to
5. Click "Setup Models" to create placeholder model files (first time only)
6. Replace placeholder files in the `models/` directory with actual RVC model files
7. Click "Start Real-time" to begin real-time voice conversion
8. Speak into your microphone - your voice will be converted in real-time
9. Click "Stop Real-time" to end the conversion

**Note**: Real-time conversion requires RVC (Retrieval-based Voice Conversion) dependencies. Install them using:
```
pip install -r requirements-rvc.txt
```

## RED TEXT:
Red text indicates issues or unsupported voices

- Wwiseutil: ERROR
  - The program couldn't find "wwiseutil.exe"
  - Make sure it's in the same folder as the program and it's renamed correctly
- DB Version: ERROR
  - The program can't read the "version" table from the database file: MHWCharacterVoices.db
  - Make sure the MHWCharacterVoices.db is in the same folder as the .exe
- In the "Overview"
  - The selected voice doesn't have information on it
  - I do apologize if you're on one of those voices. I'll get to it at some point (Or you can help by filling it out)
  - You can check if your voice is supported in the spreadsheet under **"DO NOT DELETE"**
  
## Other Notes:
- This program opens a console alongside itself
	- This is used to track errors or progress
	- If your conversion fails, look for errors in the console
- There is a "Manual Mode" option in the "Input Voice" section
	- DO NOT turn on unless you know what you're doing
		- It's for cases where you rename files but understand what they do
	- DO NOT use it to do Ciri, Geralt, Leon, or Claire conversions
		- It won't work. And if it does, it won't sound right
  - There is a 'Save to "Output"' option in the "Output Voice" section
	  - It reverts the saving behaviour to that of the pervious version
    
## Do Not Delete:
- EmptyNbnks
	- This folder holds the placeholder nbnks for conversion
	- They hold the metadata for each voice
- MHWCharacterVoices.db
	- A database that holds information about character voices
	- A link to the spreadsheet it's based on is here: https://docs.google.com/spreadsheets/d/17__upp0CDmhdhVOS6Wk8Us27Yai-Xf3N1sudkrY9yvE/
- models/ (NEW)
	- This folder holds RVC model files for real-time voice conversion
	- Replace placeholder files with actual trained RVC models
	- Model files should be named according to voice ID (e.g., FEMALE_1.pth, MALE_3.pth)
  
### Thanks To/Dependencies:
- Richard Jarvis for the appJar library which powers this program
- hpxro7 for the MHW Audio Modding Tool
	- The link to that tool's GitHub is here: https://github.com/hpxro7/wwiseutil 
- D. Richard Hipp for SQLite3
- RVC-Project for Retrieval-based Voice Conversion technology
	- The link to RVC project: https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
- Real-time voice conversion powered by RVC (Retrieval-based Voice Conversion)
