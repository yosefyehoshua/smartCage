import cPickle as pickle

# define tunnels and their characteristics:
# hardware available, GPIO of basic functions.
tunnelsDict = {'tunnel1': {
                    'PIN_WATER': 1, 
                    'PIN_LICK_DETECT': 2,
                    'USB_PORT': "/dev/ttyUSB0"}, 
               'tunnel2': {
                     'PIN_WATER': 3, 
                     'PIN_LICK_DETECT': 10,
                     'USB_PORT': "/dev/ttyUSB1"}}

# save dictionary in a pickle file
pickle.dump(tunnelsDict, open("tunnelsDict.p", "wb"))