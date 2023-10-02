#!/bin/bash
ACTION="remove"
DEVBASE="sda1"
DEVICE="/dev/${DEVBASE}"

MOUNT_POINT=$(/bin/mount | /bin/grep ${DEVICE} | /usr/bin/awk '{ print $3 }')  # See if this drive is already mounted
case "${ACTION}" in
    add)
        if [[ -n ${MOUNT_POINT} ]]; then exit 1; fi          # Already mounted, exit
        eval $(/sbin/blkid -o udev ${DEVICE})                # Get info for this drive: $ID_FS_LABEL, $ID_FS_UUID, and $ID_FS_TYPE
        OPTS="rw,relatime"                                   # Global mount options
        if [[ ${ID_FS_TYPE} == "vfat" ]]; then OPTS+=",users,gid=100,umask=000,shortname=mixed,utf8=1,flush"; fi     # File system type specific mount options
        if ! /bin/mount -o ${OPTS} ${DEVICE} /media/; then exit 1; fi          # Error during mount process: cleanup mountpoint
#        if ! /bin/mount -o ${OPTS} /dev/sda1 /media/; then exit 1; fi          # Error during mount process: cleanup mountpoint
        ;;
    remove)
        if [[ -n ${MOUNT_POINT} ]]; then /bin/umount -l ${DEVICE}; fi
#        if [[ -n ${MOUNT_POINT} ]]; then /bin/umount -l /dev/sda1; fi
        ;;
esac
