def _validate_peg(peg, name):
    if type(peg) is not int:
        raise TypeError(name + " must be an integer")

    if peg < 1 or peg > 3:
        raise ValueError(name + " must be 1, 2, or 3")


def _make_indentation(recursion_level):
    indentation = ""
    current_level = 0

    while current_level < recursion_level:
        indentation = indentation + "    "
        current_level += 1

    return indentation


def move_disk(source, destination, disk, recursion_level):
    if type(disk) is not int:
        raise TypeError("disk must be an integer")

    if disk < 1:
        raise ValueError("disk must be positive")

    _validate_peg(source, "source")
    _validate_peg(destination, "destination")

    if source == destination:
        raise ValueError("source and destination must differ")

    if type(recursion_level) is not int:
        raise TypeError("recursion_level must be an integer")

    if recursion_level < 1:
        raise ValueError("recursion_level must be positive")

    indentation = _make_indentation(recursion_level)
    print(indentation + "Recursion Level=", recursion_level)
    print(indentation + "Moving Disk", disk, "from Source", source,
          "to Destination", destination)
    print(indentation + "n=", disk, ", src=", source, ", dest=",
          destination, sep="")


def towers(number_of_disks, source, destination, recursion_level=1):
    if type(number_of_disks) is not int:
        raise TypeError("number_of_disks must be an integer")

    if number_of_disks < 1:
        raise ValueError("number_of_disks must be positive")

    _validate_peg(source, "source")
    _validate_peg(destination, "destination")

    if source == destination:
        raise ValueError("source and destination must differ")

    if type(recursion_level) is not int:
        raise TypeError("recursion_level must be an integer")

    if recursion_level < 1:
        raise ValueError("recursion_level must be positive")

    if number_of_disks == 1:
        move_disk(source, destination, number_of_disks, recursion_level)
    else:
        temporary = 6 - source - destination
        towers(number_of_disks - 1, source, temporary,
               recursion_level + 1)
        move_disk(source, destination, number_of_disks, recursion_level)
        towers(number_of_disks - 1, temporary, destination,
               recursion_level + 1)
