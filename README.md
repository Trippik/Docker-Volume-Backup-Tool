# Docker-Volume-Backup-Tool
A containerized python backup script to do regular daily backup of all docker volumes from a host machine and copy them as a compressed TAR file to a remote  SMB or SFTP server and or S3 Bucket, designed to provide volume data backup for small deployments

### Volumes and Bindings
Bind the system directory holding your containers volumes to /vols_path, this is intended to be bound read-only to ensure protection of data in running containers volumes.
The program also generates and stores a database of all backup events and jobs, this is intended to be stored in a volume mounted to the /databases directory in the container

### Enviroment Variables
- TARGET-MODES: A tuple list of various backup modes (e.g ['S3','FTP'])
- SUB-DIRECTORIES: If only wanting to backup specific sub directories/volumes within the /vols_path specify them here (e.g ['beep-vol','boop-vol']), if wanting to backip all sub directories/volumes leave this tuple blank (e.g [])
- STORAGE-SERVER: IP Address or hostname of target storage server (SMB or SFTP)
- USERNAME: Username for access to remote storage server
- PASSWORD: Password for access to remote storage server
- PORT: Port for access to remote storage server (only required for SFTP)
- NUMBER-OF-BACKUPS: The maximum number of backups you wish to hold on the remote storage server, the system will automatically delete the oldest backup when this amount is reached
- REPORTING_HOUR: The hour of the day in 24hr format when you would like the backup to run (e.g to backup at 3 O'Clock in the afternoon set this value to 15)
- ACCESS-KEY-ID: The AWS Access Key used for authentication if using S3 target mode
- SECRET-KEY: The AWS Secret Key used for authentication is using S3 target mode
- BUCKET: The target S3 bucket is using S3 target mode
- DB-FILEPATH: The filepath to the internal database used by the program (can be left as default value)
- SMB-SHARE: The name of the target SMB Share (if saving to SMB server)

https://hub.docker.com/r/trippik/docker-volume-backup-tool
