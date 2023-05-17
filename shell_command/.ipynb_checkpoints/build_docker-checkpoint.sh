clear
docker stop bat_infra
docker rm bat_infra
docker image rm bat_infra:v1.0
docker build -t bat_infra:v1.0 ../.
docker run -itd --name bat_infra --restart unless-stopped --memory="4G" -p 0.0.0.0:5003:5003 bat_infra:v1.0