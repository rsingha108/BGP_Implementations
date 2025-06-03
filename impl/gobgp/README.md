1. Create the docker image from Dockerfile: `sudo docker build --tag ksator/gobgp:1.0 .`
2. The `docker-compose.yml` file specifies the network topology. Here we have a simple network topology, i.e. one gobgp router `gobgp_1` and one exabgp route injector `exabgp_1`. They are connected by `test_net1`. The ip address of the `gobgp_1` is `3.0.0.2` and the ip address of `exabgp_1` is `3.0.0.3`. To run the docker containers for gobgp and exabgp:
```
sudo docker-compose up -d
```
3. Write configurations for `gobgp_1` and `exabgp_1` as mentioned.
4. Enter into bash terminal of `gobgp_1` and `exabgp_1` in two separate terminals. (change directory to `impl/gobgp` in both):
```
sudo docker exec -it gobgp_1 bash
sudo docker exec -it exabgp_1 bash
```
5. To Send route through exabgp, run the following command from the `exabgp_1` bash:
```
exabgp exabgp/conf.ini
```
6. To Check the BGP RIB in `gobgp_1`, run the following command from bash of `gobgp_1`:
```
gobgp global rib
```
7. Run `sudo docker-compose down` from the same directory (`impl/gobgp`) to remove all containers and networks.

# To Save the image

1. `sudo docker tag ksator/gobgp:1.0 ksator_gobgp`
2. `sudo docker save -o ksator_gobgp.tar ksator_gobgp`
3. `sudo zip ksator_gobgp.zip ksator_gobgp.tar.gz`
4. Upload to google drive

# To Load the image

1. `unzip ksator_gobgp.zip` --> ksator_gobgp.tar.gz
2. `gunzip ksator_gobgp.tar.gz` --> ksator_gobgp.tar
3. Load Image: `sudo docker load -i ksator_gobgp.tar` 
4. Change Image name: `sudo docker tag ksator_gobgp ksator/gobgp`
