# To Save the image

1. `sudo docker tag mikenowak/exabgp mikenowak_exabgp`
2. `sudo docker save -o mikenowak_exabgp.tar mikwnowak_exabgp`
3. `sudo zip mikwnowak_exabgp.zip mikwnowak_exabgp.tar.gz`
4. Upload to google drive (and share link)

# To Load the image

1. `unzip mikwnowak_exabgp.zip` --> mikwnowak_exabgp.tar.gz
2. `gunzip mikwnowak_exabgp.tar.gz` --> mikwnowak_exabgp.tar
3. Load Image: `sudo docker load -i mikwnowak_exabgp.tar` 
4. Change Image name: `sudo docker tag mikwnowak_exabgp mikwnowak/exabgp`
