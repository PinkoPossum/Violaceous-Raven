### A Brief Overview
 SlopBot9001 is a python script that will pull content from reddit following guidelines in the code that can be adjusted. It will then output a .csv file with what it pulled and information about the post. After this, it will narrate the post using Google's TTS. Finally, pulling video files from a specified folder it will overlay the audio on top of subway surfer or minecraft parkour footage and cut it up to 30 sec increments. I never got around to testing automated uploads. 

### Unrealized Features and Reflections
 Although originally I wanted to use Eleven labs for their more natural voices, I was limited by how much I was willing to spend on an exploratory project. 

 I did my best to make this OS-agnostic but further alteration maybe necessary as it was made on windows with deployment on a linux server.

**The requirements for your environtment will be listed below but will also be available in "requirements.txt":**
 
> annotated-types==0.7.0
anyio==4.9.0
audeer==2.2.1
audiofile==1.5.1
audmath==1.4.1
certifi==2025.4.26
cffi==1.17.1
charset-normalizer==3.4.2
colorama==0.4.6
decorator==4.4.2
elevenlabs==2.0.0
et_xmlfile==2.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
imageio==2.37.0
imageio-ffmpeg==0.6.0
moviepy==1.0.3
numpy==2.2.6
opencv-python==4.11.0.86
openpyxl==3.1.5
pandas==2.2.3
pillow==10.4.0
praw==7.8.1
prawcore==2.4.0
proglog==0.1.12
pycparser==2.22
pydantic==2.11.4
pydantic_core==2.33.2
pydub==0.25.1
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
pytz==2025.2
requests==2.32.3
scipy==1.15.3
six==1.17.0
sniffio==1.3.1
soundfile==0.13.1
tqdm==4.67.1
typing-inspection==0.4.0
typing_extensions==4.13.2
tzdata==2025.2
update-checker==0.18.0
urllib3==2.4.0
websocket-client==1.8.0
> websockets==15.0.1
