#!/bin/bash
#One instance only check
me="$(basename "$0")";
running=$(ps h -C "$me" | grep -wv $$ | wc -l);
[[ $running > 1 ]] && exit;

KEY="tunaws.pem"
CLOUDHOST="13.50.210.14"
USER="ubuntu"
#KEY=tunaws.pem
#CLOUDHOST="34.118.38.72"
#USER="tunkey"
REMOTE_PORT="8081"
LOCPORT="8080"
SSH_COMMAND="ssh -N -i ~/.ssh/$KEY -o ServerAliveCountMax=2 -o ServerAliveInterval=15 -R $REMOTE_PORT:localhost:$LOCPORT $USER@$CLOUDHOST"

#ssh -N -i ~/.ssh/tunkey -o ServerAliveCountMax=2 -o ServerAliveInterval=15 -R 5000:localhost:8080 tunkey@34.118.38.72
#ssh -N -i ~/.ssh/tunaws.pem -o ServerAliveCountMax=2 -o ServerAliveInterval=5 -R 5000:localhost:8080 ubuntu@13.50.210.14
#SSH_COMMAND="ssh -N -R $REMOTE_PORT:localhost:$LOCPORT ubuntu@$CLOUDHOST"
#ssh -N -R 5000:localhost:8080 ubuntu@13.50.210.14
#ncat --sh-exec "echo >/dev/null" -w 1 13.50.210.14 5000
#nc -z -w 1 13.50.210.14 5000
function ssh_remote_connect {
    while true; do
	current_time=$(date +"%T")
	echo "$current_time"
        # Check if the port is open on the remote server
        #nc -z -w 1 $CLOUDHOST $REMOTE_PORT
        ncat --sh-exec "echo >/dev/null" -w 1 $CLOUDHOST $REMOTE_PORT
        local exit_status=$?
	echo "status [$exit_status]"
        #if [ $exit_status -eq 0 ] || [ $exit_status -eq 1 ]; then
        if [ $exit_status -eq 0 ]; then
            echo "Port $CLOUDHOST:$REMOTE_PORT is open. SSH tunnel is active."
        else
            echo "Port $CLOUDHOST:$REMOTE_PORT is closed. Reconnecting...$SSH_COMMAND"
            $SSH_COMMAND &
        fi

        # Sleep for a few seconds before the next check
        sleep 10
    done
}

# Function to handle SSH errors
function handle_ssh_error {
    echo "SSH connection failed. Reconnecting..."
    # Attempt to re-establish the SSH connection in the background
	$SSH_COMMAND &
}

# Set up a trap to handle SSH errors
trap handle_ssh_error ERR

ssh_remote_connect

