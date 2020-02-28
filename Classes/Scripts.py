from Classes.Config import ftp_password, ftp_user, mikrotik_arch, mikrotik_fw, mikrotik_name, ftp_addr

get_info = ":put [/system identity get name];"\
           ":put [/system resource get architecture-name];"\
           ":put [/system resource get version ];"

backup_script = ':local time [/system clock get time];' \
                ':local thisdate [/system clock get date]; ' \
                ':local datetimestring ([:pick $thisdate 0 3] ."-" . [:pick $thisdate 4 6] ."-" . [:pick $thisdate 7 11]);' \
                ':local backupfilename ([/system identity get name]."_' + mikrotik_fw + "_" + mikrotik_arch + '_".$datetimestring."_".$time); ' \
                '/system backup save name="$backupfilename";' \
                ':delay 1s;' \
                \
                '/export compact file="$backupfilename";' \
                '/tool fetch address="' + ftp_addr + '" src-path="$backupfilename.backup" user=' \
                + ftp_user + ' password=' + ftp_password + ' port=21 upload=yes mode=ftp dst-path="' \
                + mikrotik_name + '/$backupfilename.backup";' \
                \
                ':delay 1;' \
                \
                '/tool fetch address="' + ftp_addr + '" src-path="$backupfilename.rsc" user=' \
                + ftp_user + ' password=' + ftp_password + ' port=21 upload=yes mode=ftp dst-path="' \
                + mikrotik_name + '/$backupfilename.rsc";' \
                \
                ':delay 1;' \
                '/file remove "$backupfilename.backup";' \
                '/file remove "$backupfilename.rsc";' \
                ':log'' info "Finished Backup Script.";'