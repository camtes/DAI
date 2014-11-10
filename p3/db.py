import anydbm

# Open database, creating it if necessary.
db = anydbm.open('db', 'r')

# Record some values

# Loop through contents.  Other dictionary methods
# such as .keys(), .values() also work.
value = {}
for k, v in db.iteritems():
    value[k] = v

# Storing a non-string key or value will raise an exception (most
# likely a TypeError).

# Close when done.
db.close()

print value['correo']
