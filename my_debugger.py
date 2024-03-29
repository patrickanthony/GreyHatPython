from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        pass

    def load(self,path_to_exe):

        # dwCreation flag determines how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if you want
        # to see the calculator GUI
        creation_flags = DEBUG_PROCESS

        # instantiate the structs
        startupinfo         = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        # The following two options allow the started process# to be shown as a seperate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the debuggee.
        startupinfo.dwFlags     = 0x1
        startupinfo.wShowWindow = 0x0

        # We then initialize the cb variable in the STARTUPINFO struct# which is just the size of the struct intself
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                    None,
                                    None,
                                    None,
                                    None,
                                    creation_flags,
                                    None,
                                    None,
                                    byref(startupinfo),
                                    byref(process_information)):
            
            print "[*] We have successfully launched the process!"
            print "[*] The Process ID I have is: %d" % \
                         process_information.dwProcessId
            self.pid = process_information.dwProcessId
            self.h_process = self.open_process(self,process_information.dwProcessId)
            self.debugger_active = True
        else:    
            print "[*] Error with error code %d." % kernel32.GetLastError()

    def open_process(self,pid):

        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS,pid,False)
        return h_process


    def attach(self,pid):

        self.h_process = self.open_process(pid)

        # We attempt to attach to the process
        # if this fails we exit the call
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid             = int(pid)
            self.run()
        else:
            print "[*] Unable to attach to process."

    def run(self):
        # Now we have to poll the debuggee for
        # debugging events

        while self.debugger_active == True:
            self.get_debug_event()

    def get_debug_event(self):

        debug_event        = DEBUG_EVENT()
        continue_status    = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event),INFINITE):

            # We arent going to build any event handlers
            # just yet. Let's just resume the process for now.
            raw_input("Press any key to continue...")
            self.debugger.active = False
            kernel32.ContinueDebugEvent( \
                debug_event.dwProcessId, \
                debug_event.dwThreadIdm \
                continue_status )
    def detatch(self):

        if kernel32.DebugActiveProcessStop(self,pid):
            print "[*] Finished debugging. Exiting..."
            return True
        else:
            print "There was an error."
            return False
