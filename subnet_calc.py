
# A Python program to calculate subnet values like network address, broadcast address and valid hosts within that subnet

# Importing regular expression to verify the input
import re

# Function to validate the entered IP Address
def validate_ip(ip):
    # A regular expression to match the format of an IP Address
    if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip) == None:
        return False
    else:
        return True

# Function to validate the entered Subnet Mask
def validate_mask(mask):

    # A list of all valid values that a subnet mask can contain
    valid_masks = [0, 128, 192, 224, 240, 248, 252, 254, 255]

    # Splitting the subnet mask into 4 octets with '.' as delimiter
    mask_octets = mask.split(".")

    # A regular expression to match the format of subnet mask
    # And further conditions to check if the entered values are a part of valid values
    if (re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", mask) == None) or \
    (int(mask_octets[0]) not in valid_masks) or \
    (int(mask_octets[1]) not in valid_masks) or \
    (int(mask_octets[2]) not in valid_masks) or \
    (int(mask_octets[3]) not in valid_masks):
        return False

    # Further conditions to check if the entered mask is continuous or not
    elif (int(mask_octets[0]) < 255 and (int(mask_octets[1]) > 0 or int(mask_octets[2]) > 0 or int(mask_octets[3]) > 0)) or \
        (int(mask_octets[0]) == 255 and int(mask_octets[1]) < 255 and (int(mask_octets[2]) > 0 or int(mask_octets[3]) > 0)) or \
        (int(mask_octets[0]) == 255 and int(mask_octets[1]) == 255 and int(mask_octets[2]) < 255 and int(mask_octets[3]) > 0):
        print("\nSubnet mask is discontinous.")
        return False

    # If input is valid return True
    else:
        return True


def subnet_calc(ip, mask):

    # Declaring empty list for storing binary values of IP & Mask
    ip_bin_octets = []
    mask_bin_octets = []

    # Splitting the IP & Mask values to get list of octet values
    ip_octets = ip.split(".")
    mask_octets = mask.split(".")

    # A for loop to iterate through octet values to convert them to binary
    for octet in ip_octets:

        # Following line converts each octet into binary and pads leading 0s to get an 8 digit binary string
        ip_bin_octet = "%08d" % int("{0:b}".format(int(octet)))

        # Storing the binary octets into a list
        ip_bin_octets.append(ip_bin_octet)

    # Repitition of above for loop to store binary mask values
    for octet in mask_octets:
        mask_bin_octet = "%08d" % int("{0:b}".format(int(octet)))
        mask_bin_octets.append(mask_bin_octet)

    # Joining the list elements to form a binary string
    binary_ip = "".join(ip_bin_octets)
    binary_mask = "".join(mask_bin_octets)

    # Counting the number of 1s and 0s in the mask to compute subnet further
    mask_ones = binary_mask.count("1")
    mask_zeroes = 32 - mask_ones

    # Calculating total number of possible hosts
    total_hosts = 2**mask_zeroes - 2

    # Calculating the binary value for Network Address
    net_add_bin = binary_ip[:mask_ones] + "0" * mask_zeroes

    # Calculating the binary value for Broadcast Address
    bst_add_bin = binary_ip[:mask_ones] + "1" * mask_zeroes

    # Declaring empty lists to store octet values for Network & Broadcast Addresses
    net_octets = []
    bst_octets = []

    # A for loop iterating through the binary string splitting it in chunks of 8 bits and appending them to the above list
    for octet in range(0,32,8):

        # Storing 8 bit values to a temp variable
        net_octet_bin = net_add_bin[octet:octet+8]

        # Converting the 8 bit values to decimal & appending them to the above declared list
        net_octets.append(int(net_octet_bin,2))

    # Another for loop repeating the above steps for broadcast address
    for octet in range(0,32,8):
        bst_octet_bin = bst_add_bin[octet:octet+8]
        bst_octets.append(int(bst_octet_bin,2))

    # Assigning the integer list values to variables for calculating first and last IP Addresses
    first_ip = net_octets
    last_ip = bst_octets

    # Converting the list of octets from integer to string
    net_octets = list(map(str, net_octets))

    # Joining the list of Strings to a single String to get the final Network Address
    network_address = ".".join(net_octets)

    # Repeating the above two steps for Broadcast Address
    bst_octets = list(map(str, bst_octets))
    broadcast_address = ".".join(bst_octets)

    # Handling an exceptional case for /31 Subnet Mask
    if int(mask_octets[3]) == 254:

        print("\nEntered subnet is a /"+str(mask_ones)+" mask with only two possible hosts.\n")

        # In this case there will be only two addresses same as network & broadcast addresses
        first_host = network_address
        last_host = broadcast_address

        print("First Valid Host:    " + str(first_host))
        print("Second Valid Host:   " + str(last_host) + "\n")

    # Handling another exceptional case for /32 Subnet Mask
    elif int(mask_octets[3]) == 255:

        print("\nEntered subnet is a /"+str(mask_ones)+" mask with only one possible host.\n")

        # In this case the variable total_hosts will have a negative value hence avoiding it
        print("Valid Host:     " + str(network_address) + "\n")

    # Else block to handle every other case
    else:

        # Calculating first & last IP from the above stored lists
        first_ip[3] += 1
        last_ip[3] -= 1

        # Converting the list of octets from integer to string & joining them
        first_ip = list(map(str, first_ip))
        first_host = ".".join(first_ip)

        # Repeating the above two steps for last IP
        last_ip = list(map(str, last_ip))
        last_host = ".".join(last_ip)

        # Printing the calculated values in a legible format
        print("\nEntered subnet is a /"+str(mask_ones)+" mask with "+str(total_hosts)+" possible hosts.\n")
        print("Network Address:     " + str(network_address))
        print("Broadcast Address:   " + str(broadcast_address))
        print("First Valid Host:    " + str(first_host))
        print("Last Valid Host:     " + str(last_host) + "\n")


# This is the first line to get executed asking for user input
ip = input("\nEnter an IP Address: ")
mask = input("\nEnter a Subnet Mask: ")

# Checking if entered values are valid or not
if (validate_ip(ip) and validate_mask(mask)):

    # Calculate only if the values are valid
    subnet_calc(ip, mask)

# Else print appropriate message & exit
else:
    print("\nPlease check the input & try again.\n")
