# Dynamical DNS updater for GoDaddy DNS

Copy sample-config.yaml to config.yaml and update the config with the correct values.

```docker build -t ddns .```

```docker run --name ddns --restart always ddns```
