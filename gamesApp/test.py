from dronekit import connect

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('com14', wait_ready=True)
