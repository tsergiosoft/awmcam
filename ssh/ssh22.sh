#!/bin/bash
#./ssh22.sh -cloud_ip=11.22.33.44 -cloud_user=ubuntu -port=5022

#One instance only check
me="$(basename "$0")";
running=$(ps h -C "$me" | grep -wv $$ | wc -l);
[[ $running > 1 ]] && exit;

KEY="tunaws.pem"
LOCPORT="22"

#CLOUDHOST="13.50.210.14"
#USER="ubuntu"
#REMOTE_PORT="5022"

while echo $1 | grep ^- > /dev/null; do declare $( echo $1 | sed 's/-//g' | sed 's/=.*//g' | tr -d '\012')=$( echo $1 | sed 's/.*=//g' | tr -d '\012'); shift; done

echo CLOUDHOST = $cloud_ip
echo USER = $cloud_user
echo REMOTE_PORT = $cloud_port

SSH_COMMAND="ssh -N -i ~/.ssh/$KEY -o ServerAliveCountMax=2 -o ServerAliveInterval=15 -R $cloud_port:localhost:$LOCPORT $cloud_user@$cloud_ip"


function ssh_remote_connect {
    while true; do
        # Check if the port is open on the remote server
        ncat --sh-exec "echo >/dev/null" -w 1 $cloud_ip $cloud_port
        local exit_status=$?
	echo "status [$exit_status]"
        #if [ $exit_status -eq 0 ] || [ $exit_status -eq 1 ]; then
        if [ $exit_status -eq 0 ]; then
            echo "Port $cloud_ip:$cloud_port is open. SSH tunnel is active."
        else
            echo "Port $cloud_ip:$cloud_port is closed. Reconnecting...\n$SSH_COMMAND"
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

sleep 5
ssh_remote_connect


