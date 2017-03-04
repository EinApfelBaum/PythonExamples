
#
# split
#

string1 = "test:test2".encode()

# fails because ":" is string and temp is byte
#temp = temp.split(":")[1]

# okay
string1 = string1.split(":".encode())[1]
print(string1)


# string2 is string and ":" is string --> okay
string2 = "test:test2"
string2 = string2.split(":")[1]

print(string2)

#
# find
#

string3 = "ichBinEinPfadUndDateiÄName"
umlaute = ["ö", "Ö", "ä", "Ä", "ü", "Ü"]
umlaute2 = ["oe", "OE", "ae", "AE", "ue", "UE"]

for umlaut in umlaute:
    if umlaut in string3:
        temp = umlaute.index(umlaut)
        temp2 = umlaute2[umlaute.index(umlaut)]
        string3 = string3.replace(umlaut,umlaute2[umlaute.index(umlaut)])





