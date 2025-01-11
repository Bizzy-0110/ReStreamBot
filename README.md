ReStreamBot is a bot for telegram made in 2022 that allows you with the use of a linux server to re-route your stream in multiple platforms at the same time
# Installation
Clone the repository
```terminal
git clone https://github.com/Bizzy-0110/ReStreamBot.git
```
```terminal
cd ReStreamBot
```
```terminal
pip install requirements.txt
```
```terminal
apt install nginx
```

# Setup
## Bot
Edit the costants at the beginning of the main.py according to your needs
And add the bot token and the whitelist members in secret.json
## Nginx
Open the Nginx configuration and add the following
```text
rtmp {
	server {
		listen 1935;
		chunk_size 4096;

		 application starting_key {

			live on;
			record off;

			meta copy;

			
			# <put here the rtmp servers that you want>
			# Example
			# Youtube
			# push rtmp://a.rtmp.youtube.com/live2/{stream_key};
			# Twich
			# push rtmp://ingest.global-contribute.live-video.net/app/{stream_key};
		}
	}

}
```
## Find the Rtmp Server Urls of the platform you want

Urls for [Twich](https://help.twitch.tv/s/twitch-ingest-recommendation?language=en_US)

Url for youtube: 
```text
push rtmp://a.rtmp.youtube.com/live2/<YourStreamKey>
```


# Starting the bot
```terminal
python3 main.py
```

# Bot Commands
**/stop =** stop the stream and change the token<br>
**/start =** generate a new token and start the nginx service<br>
**/reload =** reload the nginx service<br>
**/get_token =** get the current token<br>
**/help =** get help for the commands<br>

# Usage
Setup the bot and start it
After starting the bot with the appropriate command go to the OBS settings, then go to Stream section, select custom in the Service selector, now, in the Server textbox insert:
```
rtmp://<YourLinuxServerIp>/<TheTokenGivenByTheBot>
```
Then if you configured correctly when you start your livestream the video streaming should be re-sent to the selected platforms
