ReStreamBot is a bot for Telegram made in 2022 that allows you to re-route your stream in multiple platforms at the same time with the power of a Linux server.
# Installation
#### Clone the repository
```terminal
git clone https://github.com/Bizzy-0110/ReStreamBot.git
```
```terminal
cd ReStreamBot
```
```terminal
pip install requirements.txt
```
#### Install Nginx with the RTMP module
To install Nginx with the RTMP module you can follow [this guide](https://obsproject.com/forum/resources/how-to-set-up-your-own-private-rtmp-server-using-nginx.50/).

A summary of the guide can be found under here.

Download dependencies:
```terminal
sudo apt update
```
```terminal
sudo apt install -y build-essential libpcre3 libpcre3-dev libssl-dev 
```

From your home directory, download the nginx source code and get the RTMP module source code from git:
```terminal
wget http://nginx.org/download/nginx-1.15.1.tar.gz
wget https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/dev.zip
```
Unpack/unzip them both, enter the nginx directory and build nginx with the RTMP module:
```terminal
tar -zxvf nginx-1.15.1.tar.gz
```
```terminal
unzip dev.zip
```
```terminal
cd nginx-1.15.1
```
```terminal
./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-dev
```
```terminal
make
```
```terminal
sudo make install 
```

And nginx is installed! By default it installs to /usr/local/nginx, so to start the server run the following command:
```terminal
sudo /usr/local/nginx/sbin/nginx 
```
To restart it, use:
```terminal
sudo /usr/local/nginx/sbin/nginx -s stop
```
```terminal
sudo /usr/local/nginx/sbin/nginx 
```

# Setup
## Bot
Edit the costants at the beginning of the `main.py` according to your needs
And add the bot token and the whitelist members in `secret.json`.
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
			# Twitch
			# push rtmp://ingest.global-contribute.live-video.net/app/{stream_key};
		}
	}

}
```
## Find the Rtmp Server Urls of the platform you want

Urls for [Twitch](https://help.twitch.tv/s/twitch-ingest-recommendation?language=en_US)

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
