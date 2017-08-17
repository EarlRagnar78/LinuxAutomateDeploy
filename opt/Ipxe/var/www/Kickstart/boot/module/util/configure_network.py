## @mainpage Network Configuration
# @brief This package contains functions for helping the network configuration of a defectless RedHat GNU/Linux installation.


## @package configure_network
# @brief This module contains functions for configuring network parameters and services.
# It is supported:
# - Creation of a backup of the network manager configuration
# - Disable the Network Manager service
# - Disable the IPv6 Protocol.

# IMPORT MODULE DEFINITIONS PART

import os
import shutil
import subprocess
import sys
import errno

# FUNCTION DEFINITION PART

##
# @brief This function is for checking permissions of a file.
# It checks if a file has read and write permissions.
# When there is no permission, the execution is stopped.
# @param file_or_directory_to_check It indicates the file or directory to check.
# @param permission It indicates the permission type to check: R for read permission, W for write permission,
# WR or RW for reading and writing permission.
# @warning If a file does not exist the function will stop the execution.
# @return The function returns True if everything is Ok or it stops the execution in case of error.


def check_permissions(file_or_directory_to_check, permission):
    error_flag = False
    if permission != 'R' and permission != 'r' and permission != 'w' and permission != 'W' and permission != 'wr' and  permission != 'Wr' and permission != 'wR' and permission != 'WR':
        print "Syntax Error"
        sys.exit(1)
    if permission == 'W' or permission == 'w':
        if not os.access(file_or_directory_to_check, os.W_OK):
            error_flag = True
            print "Error: There is no write permissions for", file_or_directory_to_check
    if permission == 'R' or permission == 'R':
        if not os.access(file_or_directory_to_check, os.R_OK):
            error_flag = True
            print "Error: There is no read permissions for", file_or_directory_to_check
    if permission == 'WR' or permission == 'wr' or permission == 'Wr' or permission == 'wR' or permission == 'RW' or permission == 'rw' or permission == 'Rw' or permission == 'rW':
        if not os.access(file_or_directory_to_check, os.R_OK) or not os.access(file_or_directory_to_check, os.W_OK):
            error_flag = True
            print "Error: There is no read/write permissions for", file_or_directory_to_check
    if error_flag:
        sys.exit(errno.EACCES)
    return True

##
# @brief This function is for checking the existence of a file or a directory.
# This function checks the existence of a file. If message parameters is not False, a message appears.
# @param file_or_directory_to_check It indicates the file or the directory to check.
# @param message_yes This message appears if the file (or directory) exists. It can be set to False for displaying nothing.
# @param message_no This message appears if the file (or directory) does not exists. It can be set to False for displaying nothing.
# @return The function returns True if the file or directory exists or False otherwise.


def check_exists(file_or_directory_to_check, message_yes, message_not):
    if os.access(file_or_directory_to_check, os.F_OK) and message_yes != False:
        print message_yes
        return True
    if os.access(file_or_directory_to_check, os.F_OK) and message_yes == False:
        return True
    if not message_not == False:
        print message_not
    return False


##
# @brief This function is for creating a directory.
# It checks if there are write permissions on the creation path and then it creates the directory.
# If the message parameters are set to False, messages are not displayed.
# @param creation_path It indicates the path in which create the directory.
# @param directory_name It indicates the name of the directory to create.
# @param message_yes This message appears if the directory was successfully created.
# @param already_exists_message This message appears if the directory already exists.
# @return It returns True if all is gone OK or the directory aldready exists.
# In the other cases, it stops the execution of the script.


def check_and_create_directory(creation_path, directory_name, message_yes, already_exists_message):
    if check_exists(creation_path+directory_name, already_exists_message, False):
        return True
    else:
        if check_permissions(creation_path,"W"):
            os.mkdir(creation_path+directory_name)
        if not check_exists(creation_path+directory_name, message_yes, already_exists_message):
            print "Write error on", creation_path+directory_name
        print message_yes
    return True


##
# @brief This function is for copying all files in a directory using a pattern to another directory.
# It copies all files in a directory that are compliant with the specified pattern to another directory.
# @param source_dir It indicates the source directory.
# @param destination_dir It indicates the destination directory.
# @param pattern_file It indicates the pattern of the files to be copied.
# @return It returns True if all is gone OK. In the other case, it stops the execution of the script.


def check_and_copy_pattern_file(source_dir, destination_dir, pattern_file):
    check_permissions(source_dir, "R")
    check_permissions(destination_dir, "W")
    result = os.listdir(source_dir)
    for x in xrange(0,len(result)):
        if pattern_file in result[x]:
            source_file = source_dir+"/"+result[x]
            destination_file = destination_dir+"/"+result[x]
            check_permissions(source_file, "R")
            print "Copying file"+source_file
            shutil.copyfile(source_file, destination_file)
            if not check_exists(destination_file, False, False):
                sys.exit(errno.EIO)
    print "All files has been copied."
    return True

##
# @brief This function is for checking if the IPv6 service is disabled.
# It checks if the IPv6 is disabled.
# @return It returns True if the IPv6 service is disabled. Otherwise it returns False.


def check_ipv6_disabled():
    result = subprocess.check_output(["lsmod"])
    if "ipv6" in result == False:
        return True
    return False


##
# @brief This function is for writing a text in a file.
# This function allow to write a text in a file. If the append parameter is set, the text is written in the end of file.
# @param file_to_write It indicates the file to write.
# @param text_to_write It indicates the test to write in the file.
# @param append If it is set to True, the text is written in the end of file if the file exists. If it is set to False,
# the file will be overwritten.
# @return It returns True if everything is gone Ok. Otherwise it stops the execution of the script.


def check_and_write_text_to_file(file_to_write, text_to_write, append):
    if check_exists(file_to_write, "The file"+file_to_write+ "already exists.  It will be overwritten", False):
        check_permissions(file_to_write, "W")
    if append:
        file_pointer = open(file_to_write,"a")
    else:
        file_pointer = open(file_to_write,"w")
    file_pointer.write(text_to_write)
    file_pointer.close()
    if not check_exists(file_to_write,False,"Write error in"+file_to_write):
        sys.exit(errno.EIO)
    return True


##
# @brief This function is for reading a text file.
# This function allow to read a text file and stores the file content on a text string: it first checks if the file
# exists and then, stores its content in a text string.
# @param file_to_read It indicates the file to read.
# @return It returns the text string read if everything is gone OK. Otherwise it stops the exection of the script.


def check_and_read_file(file_to_read):
    if not check_exists(file_to_read, False, "The file does not exists."):
        return False
    check_permissions(file_to_read, "R")
    file_pointer = open(file_to_read,"r")
    result = file_pointer.read()
    file_pointer.close()
    return result

##
# @brief This function is for replace an option in a text file.
# This function checks the existence and the permission of a file. Then It finds the original text and replace
# it with the new text.
# @param file_to_write It indicates the text file with the content that will be replaced.
# @param original_option It indicates the original text to replace.
# @param replaced_option It indicates the text that will replace the original text.
# @return It returns True is all is gone OK. Otherwise it stops the execution of the script.


def check_and_replace_option_to_file(file_to_write, original_option, replaced_option):
    if not check_exists(file_to_write, False, "The file"+file_to_write+"does not exists."):
        check_and_write_text_to_file(file_to_write, replaced_option, False)
        return True
    check_permissions(file_to_write, "WR")
    result = check_and_read_file(file_to_write)
    result.replace(original_option,replaced_option)
    file_pointer = open(file_to_write,"w")
    file_pointer.write(result)
    file_pointer.close()
    return True


##
# @brief This function allows to comment lines in a text file compliant with a pattern.
# This functions first checks the existence and the permission of the text file then, it comments the lines compliant
# with the specified pattern.
# @param file_to_write It indicates the file to change.
# @param pattern It indicates the used pattern.
# @param comment It indicates the characters for comment the line.
# @returns It returns True if all is gone OK. Otherwise it stops the execution of the script.


def check_and_comment_rows_to_file(file_to_write, pattern, comment):
    if not check_exists(file_to_write, False, "The file"+file_to_write+"does not exists."):
        return True
    check_permissions(file_to_write,"WR")
    file_rows = list()
    with open(file_to_write,"r") as file_pointer:
        for line in file_pointer:
            if pattern in line:
                line = comment+line
            file_rows.append(line)
    file_pointer.close()
    file_pointer = open(file_to_write,"w")
    for row in file_rows:
        file_pointer.write("%s\n" % row)
    file_pointer.close()
    if not check_exists(file_to_write, False, False):
        sys.exit(errno.EIO)
    return True


##
# @brief This function is for the backup of the network configuration.
# This function copies configuration files into the backup directory. It checks if all directories are available,
# if all files are readable and then it copies all desired files. Finally it checks the correctness
# of the destination files.
# @warning destination files will be overwritten.
# @return It returns True if all is gone OK, False otherwise.


def backup_network_configuration():
    # DEFAULT PARAMETERS DEFINITION
    # put here the directory with network configuration files
    network_config_directory = "/etc/sysconfig/network-scripts"
    # put here the directory for the configuration backup
    backup_config_directory =  "/config_save_netcfg"
    # put here the pattern for which file to save
    backup_network_files_pattern = "ifcfg"
    check_and_create_directory(network_config_directory, backup_config_directory, "Directory" + backup_config_directory + "was successfully created.", "Directory" + backup_config_directory + "already exists.")
    print "Copying configuration files on backup directory"
    check_and_copy_pattern_file(network_config_directory,network_config_directory+backup_config_directory,backup_network_files_pattern)
    return True


##
# @brief This function is for disable the NetworkManager.
# This function stops and disables the Network Manager service.
# @return It returns True if all is gone OK. False otherwise.


def disable_network_manager():
    # DEFAULT PARAMETERS DEFINITION
    # put here the shell command for stop the Network Manager service
    stop_network_manager_service_command = ["service", "NetworkManager", "stop"]
    # put here the shell command for disable the Network Manager service
    disable_network_manager_service_command = ["chkconfig", "NetworkManager", "off"]
    result = subprocess.call(stop_network_manager_service_command)
    if result != 0:
        print "There was an error stopping the Network Manger service."
        return False
    else:
        print "Network Manager service successfully stopped."
    result = subprocess.call(disable_network_manager_service_command)
    if result != 0:
        print "There was an error disabling the Network Manager service."
        return False
    else:
        print "Network Manager service successfully disabled."
        return True


##
# @brief This function is for disable the IPv6 protocol service.
# This function stops and disables the IPv6 protocol and service.
# @warning IPv6 Configuration files will be overwritten.
# @warning To disable the support a system reboot is required.
# @return It returns True if all is gone OK. False otherwise.


def disable_ipv6_service():
    # DEFAULT PARAMETERS DEFINITION
    # put here the file of the IPv6 kernel module
    disable_ipv6_kernel_module_file = "/etc/modprobe.d/ipv6.conf"
    # put here the IPv6 kernel module disable option here
    disable_ipv6_kernel_module_option = "options ipv6 disable=1"
    # put here the shell command for disable IPv6 tables
    disable_ipv6_tables_command = ["chkconfig", "ip6tables", "off"]
    # put here the network configuration file
    disable_ipv6_network_configuration_file = "/etc/sysconfig/network"
    # put here the IPv6 network configuration file disable option
    disable_ipv6_network_configuration_option = "NETWORKING_IPV6=no"
    # put here the system configuration file
    disable_ipv6_system_configuration_file = "/etc/sysctl.conf"
    # put here the system configuration parameters to change from 0 to 1
    disable_ipv6_system_configuration_parameters = ["net.ipv6.conf.all.disable_ipv6",
                                                    "net.ipv6.conf.default.disable_ipv6"]
    # put here the host configuration file
    disable_ipv6_hosts_configuration_file = "/etc/hosts"
    # put here the backup configuration file of the host file
    disable_ipv6_hosts_configuration_backup_file = "/etc/hosts.disableipv6"
    # put here the default grub configuration file
    disable_ipv6_default_grub_file = "/etc/default/grub"
    # put here the option to append to the grub file
    disable_ipv6_grub_option = 'GRUB_CMDLINE_LINUX=".rd.lvm.lv=rhel/swap crashkernel=auto rd.lvm.lv=rhel/root ipv6.disable=1"'
    # put here the command to regenerate the grub file in legacy BIOS
    disable_ipv6_grub_regeneration_command_legacy_BIOS =["grub2-mkconfig", "-o", "/boot/grub2/grub.cfg"]
    # put here the command to regenerate the grub file in UEFI
    disable_ipv6_grub_regeneration_command_UEFI = ["grub2-mkconfig", "-o", "/boot/efi/EFI/redhat/grub.cfg"]
    result = subprocess.check_output(["lsmod"])
    if check_ipv6_disabled():
        print "IPv6 was already disabled."
        return True
    else:
        check_and_write_text_to_file(disable_ipv6_kernel_module_file,disable_ipv6_kernel_module_option, False)
        print "The file", disable_ipv6_kernel_module_file, "successfully created."
        subprocess.call(disable_ipv6_tables_command)
        print "ip6table service has been disabled."
        check_and_write_text_to_file(disable_ipv6_network_configuration_file, disable_ipv6_network_configuration_option, True)
        print "The file", disable_ipv6_network_configuration_file, "has been successfully updated."
        for x in xrange(0, len(disable_ipv6_system_configuration_parameters)):
            check_and_replace_option_to_file(disable_ipv6_system_configuration_file, disable_ipv6_system_configuration_parameters[x] + " = 0", disable_ipv6_system_configuration_parameters[x] + " = 1")
        print "The file", disable_ipv6_system_configuration_file, "has been updated."
        check_and_comment_rows_to_file(disable_ipv6_hosts_configuration_file, ":", "#")
        #print "The file", disable_ipv6_hosts_configuration_file, "has been updated."
        #check_and_write_text_to_file(, text_to_write, true)
    return True


##
# @brief This function is for disable both SElinux and iptables.
# This function checks if services are already disabled. If not, disables both SElinux and iptables and then it restarts the network service.
# @warning The network service will be restarted.
# @return It returns True if all is gone OK. The execution is interrupted otherwise.


def disable_selinux_and_iptables():
    # DEFAULT PARAMETERS DEFINITION
    # put here the configuration file of selinux
    disable_selinux_configuration_file = "/etc/selinux/config"
    # put here the command for stopping the iptables service
    stop_iptables_service_command = ["service", "iptables", "stop"]
    # put here the command for disabling the iptables service
    disable_iptables_service_command = ["chkconfig", "iptables", "off"]
    # put here the command for restarting the network service
    restart_network_command = ["service", "network", "restart"]
    subprocess.call(stop_iptables_service_command)
    subprocess.call(disable_iptables_service_command)
    subprocess.call(restart_network_command)

