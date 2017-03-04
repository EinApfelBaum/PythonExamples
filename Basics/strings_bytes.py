temp = "test".encode()
print(temp)


temp = "test".encode('utf-8')
print(temp)

temp2 = temp.decode('utf-8')
print(temp2)

temp = "b'[OTRHelper:] Die Datei, die Sie dekodieren m\xf6chten, wurde nicht auf auf www.onlinetvrecorder.com gefunden. Bitte \xfcberpr\xfcfen Sie den Dateinamen und vergewissern Sie sich, das Sie ihn nicht ge\xe4ndert haben. Den korrekten Dateinamen finden Sie im Download-Fenster zu dieser Sendung auf www.onlinetvrecorder.com .\r\n'".encode()
temp2 = temp.decode('utf-8')
print(temp2)


line = 'Progress\nTest'
char = ':'

if line is 'Progress':
    print('Stimmt')

if char is ':':
    print('stimmt auch')

i = line.find('\n')
print(i)

