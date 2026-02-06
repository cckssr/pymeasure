import pyvisa

rm = pyvisa.ResourceManager()

for resource in rm.list_resources_info():
    print(resource.)
