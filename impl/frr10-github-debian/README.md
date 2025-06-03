# Some Points to use frr10 properly
1. use github/frr10 latest
2. use command: "/usr/lib/frr/docker-start” in docker-compose.yml
3. no bgp ebgp-requires-policy
4. no bgp network import-check
5. If using exabgp: then announce route with “next hop self”. If random as-path used then route won’t get installed.

# Running instructions

1. Choose the correct FRR version by chnaging the `ENV FRRVER` variable in the Dockerfile.
2. Create the docker image from Dockerfile: `sudo docker build --tag ksator/frr8 .`
3. The `docker-compose.yml` file specifies the network topology. Here we have a simple network topology, i.e. one frr router `frr_1` and one exabgp route injector `exabgp_1`. They are connected by `test_net1`. The ip address of the `frr_1` is `3.0.0.2` and the ip address of `exabgp_1` is `3.0.0.3`. To run the docker containers for frr and exabgp:
```
sudo docker-compose up -d
```
4. Write configurations for `frr_1` and `exabgp_1` as mentioned.
5. Enter into bash terminal of `frr_1` and `exabgp_1` in two separate terminals. (change directory to `impl/frr` in both):
```
sudo docker exec -it frr_1 bash
sudo docker exec -it exabgp_1 bash
```
6. To Send route through exabgp, run the following command from the `exabgp_1` bash:
```
exabgp exabgp/conf.ini
```
7. To Check the BGP RIB in `frr_1`, run the following command from bash of `frr_1`:
```
vtysh -c "show ip bgp"
```
8. Run `sudo docker-compose down` from the same directory (`impl/frr`) to remove all containers and networks.

# To Save the image

1. `sudo docker tag github/frr10 github_frr10`
2. `sudo docker save -o github_frr10.tar github_frr10`
3. `sudo zip github_frr10.zip github_frr10.tar.gz`
4. Upload to google drive

# To Load the image

1. `unzip github_frr10.zip` --> github_frr10.tar.gz
2. `gunzip github_frr10.tar.gz` --> github_frr10.tar
3. Load Image: `sudo docker load -i github_frr10.tar` 
4. Change Image name: `sudo docker tag github_frr10 github/frr10`

