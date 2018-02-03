# Dynamical DNS updater for GoDaddy DNS

docker build -t ddns .
docker run --name ddns --restart always ddns
