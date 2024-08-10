import os, time
columns, rows = os.get_terminal_size()
print (columns, rows)

print("\033[5;25HHello")

time.sleep(2)
