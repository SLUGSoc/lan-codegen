"""Generates codes and SQL insert statement for Heimdall authpuppy.

v1.0
Rob Ede
June 2017
"""

from random import choice
from datetime import datetime


def randomChar():
    """Random character."""
    return choice(chars)


def code():
    """Code string."""
    return ''.join([randomChar() for i in range(8)])


def fileOutput(codes, filename):
    """Output codes to filename."""
    file = open(filename + '.csv', 'w')

    for code in codes:
        file.write(code + '\n')

    file.close()


# character set: 0-9 + A-Z
chars = [chr(x) for x in range(48, 58)] + [chr(x) for x in range(65, 91)]

# number of codes per ticket type
nTickets = 100

# unique code storage
codes = set()

# format: ticketTypeId: (ticketName, listOffset)
ticketTypes = [
    (1, 'weekend', nTickets * 0, nTickets * 1),
    (2, 'friday', nTickets * 1, nTickets * 2),
    (3, 'saturday', nTickets * 2, nTickets * 3),
    (4, 'sunday', nTickets * 3, nTickets * 4)
]

# generate nTickets unique codes for each ticket type
while len(codes) < nTickets * 4:
    codes.add(code())

# convert codes set to list
codes = list(codes)

sqlFile = open('codes.sql', 'w')

# truncate tables
sqlFile.write('TRUNCATE TABLE `authpuppy`.`ap_user`;\n')
sqlFile.write('TRUNCATE TABLE `authpuppy`.`connections`;\n')
sqlFile.write('TRUNCATE TABLE `authpuppy`.`ap_applicable_policies`;\n')
sqlFile.write('\n')

sql = ''

# output ticket codes
for tId, tName, tOffsetStart, tOffsetEnd in ticketTypes:
    fileOutput(codes[tOffsetStart:tOffsetEnd], tName)

    for i, code in enumerate(codes[tOffsetStart:tOffsetEnd]):
        sql += 'INSERT INTO `authpuppy`.`ap_user`'
        sql += ' (`id`, `username`, `password`, `email`, `registered_on`,'
        sql += ' `validation_token`, `status`, `username_lower`,'
        sql += ' `physical_user_id`, `payment`, `ticket_notes`,'
        sql += ' `local_user_profile_id`, `simple_network_id`)'
        sql += ' VALUES ('

        sql += '\'' + str(tOffsetStart + i) + '\','
        sql += ' \'' + code + '\','
        sql += ' \'8/qxgC9lDfrjuqjdf71NrQ==\','
        sql += ' \'' + code + '@SLUGSLAN.com\','
        sql += ' \'' + (datetime.now()).strftime('%Y-%m-%d %H:%M:%S') + '\','
        sql += ' NULL,'
        sql += ' \'1\','
        sql += ' \'' + code.lower() + '\','
        sql += ' \'' + str(tId) + '\','
        sql += ' \'FREE\','
        sql += ' \'\','
        sql += ' \'' + str(tId) + '\','
        sql += ' \'2\''

        sql += ');\n'

sqlFile.write(sql)
