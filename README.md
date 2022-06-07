# Docker-Volume-Backup-Tool
A containerized python backup script to do regular daily backup of all docker volumes from a host machine and copy them as a compressed TAR file to a remote FTP or SFTP server, designed to provide volume data backup for small deployments

### Volumes and Bindings
Bind the system directory holding your containers volumes to /vols_path, this is intended to be bound read-only to ensure protection of data in running containers volumes

### Enviroment Variables
- TARGET-MODE: FTP or SFTP
- STORAGE-SERVER: IP Address or hostname of target storage server
- USERNAME: Username for access to remote storage server
- PASSWORD: Password for access to remote storage server
- PORT: Port for access to remote storage server (only required for SFTP, can be set to dummy integer when using FTP)
- NUMBER-OF-BACKUPS: The maximum number of backups you wish to hold on the remote storage server, the system will automatically delete the oldest backup when this amount is reached
- REPORTING_HOUR: The hour of the day in 24hr format when you would like the backup to run (e.g to backup at 3 O'Clock in the afternoon set this value to 15)

https://hub.docker.com/r/trippik/docker-volume-backup-tool
