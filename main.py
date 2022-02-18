import os
import sys

blue = "\033[1;34;48m"
green = "\033[1;32;48m"
red = "\033[1;31;48m"
white = "\033[0;37;48m"

banner = f"""{green}| {blue}Network, Broadcast, First and Last Usable IP Address Finder{green} ----------------------------\n"""

clear = lambda: os.system("cls")

try:
    while True:

        clear()
        print(banner)

        address = input(f"{blue}> {green}IP Address and Prefix Length : {red}")

        if address.find("/") == -1:
            raise TabError("You did not enter a Prefix Length.")

        address_list = address.replace("/", ".").split(".")
        address_list = [int(x) for x in address_list]
        subnet_mask = address_list.pop()

        if len(address_list) != 4:
            raise TabError(
                "The number of IP address Octets cannot be greater or less than 4."
            )

        for i in address_list:
            if i < 0 or i > 255:
                raise TabError(
                    "IP Address Octet cannot be less than 0 or greater than 255."
                )

        if subnet_mask < 0 or subnet_mask > 32:
            raise TabError("Subnet mask cannot be less than 0 or greater than 32.")
        subnet_mask_binary = int(subnet_mask) * "1" + (32 - int(subnet_mask)) * "0"

        def binary_to_decimal(octet: str):
            return int(octet, 2)

        def binary_to_decimal_list(binary_string):
            lst = []
            lst.append(binary_to_decimal(binary_string[:8]))
            lst.append(binary_to_decimal(binary_string[8:16]))
            lst.append(binary_to_decimal(binary_string[16:24]))
            lst.append(binary_to_decimal(binary_string[24:]))

            return lst

        subnet_mask_decimal_octet_list = binary_to_decimal_list(subnet_mask_binary)

        def broadcast_and_last_usable_address_process(network_address: str):
            def decimal_to_binary(octet):
                return bin(int(octet)).replace("0b", "")

            binary_address = ""

            network_address_list = network_address.split(".")
            for octet in network_address_list:
                binary = decimal_to_binary(octet)
                if len(binary) <= 8:
                    binary = (8 - len(binary)) * "0" + binary
                binary_address += binary

            binary_address = binary_address[:subnet_mask] + (32 - subnet_mask) * "1"
            broadcast_address_list = binary_to_decimal_list(binary_address)

            last_usable_address = broadcast_address_list.copy()
            last_usable_address[3] = last_usable_address[3] - 1

            return broadcast_address_list, last_usable_address

        network_address = ""
        first_usable_address_list = []

        for a, s, i in zip(address_list, subnet_mask_decimal_octet_list, range(4)):
            network_address += str(a & s) + "."
            if i == 3:
                first_usable_address_list.append(str((a & s) + 1))
                continue
            first_usable_address_list.append(str(a & s))

        network_address = network_address[:-1]
        first_usable_address = ".".join(first_usable_address_list)

        (
            broadcast_address_list,
            last_usable_address_list,
        ) = broadcast_and_last_usable_address_process(network_address)

        broadcast_address = ".".join([str(x) for x in broadcast_address_list])

        last_usable_address = ".".join([str(x) for x in last_usable_address_list])

        print(f"{blue}>{green} Network Address : {red}" + network_address)
        print(f"{blue}>{green} Broadcast Address : {red}" + broadcast_address)
        print(f"{blue}>{green} First Usable Address : {red}", first_usable_address)
        print(f"{blue}>{green} Last Usable Address : {red}", last_usable_address)

        print()

        question = input(f"{blue}> {green}New IP Address (y/n) : {red}")
        if question in "y" or question in "Y":
            clear()
            print(banner)
            continue
        else:
            print(f"{white}Bye :)")
            sys.exit()

except TabError as e:
    print(f"{white}{e}")
except Exception as e:
    print(f"{white}Incorrect format or an error has occurred. Exiting the program...")
    sys.exit()
