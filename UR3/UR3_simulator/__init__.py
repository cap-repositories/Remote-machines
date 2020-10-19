"""
"""
import multiprocessing as mp
import threading
from tcp_server_socket import *
import sys


def kill_all_servers_process(fileno):
    killevent_obj = mp.Event()
    
    def wait_user(killevent_obj):
        input()
        killevent_obj.set()
    
    p = threading.Thread(target=wait_user,args=(killevent_obj,))
    p.start()

    return (killevent_obj,p)

if __name__ == '__main__ ':
    mp.freeze_support()
    tcp_s = tcp_servers()

    ports = {
        "10Hz_primary_RxTx": 30001,
    	"10Hz_primary_Tx": 30011}
    """
        "10Hz_secondary_RxTx": 30002,
        "10Hz_secondary_Tx": 30012,
        "500Hz_RealTime_RxTx": 30003,
        "500Hz_RealTime_Tx":30013,
        "500Hz_RTD_RxTx":30004
    }
    """

    event_obj = mp.Event()
    fn = sys.stdin.fileno() #get original file descriptor
    sys.stdin.close()
    (killevent_obj,kill_p) = kill_all_servers_process(fn)
    tcp_s.start_server_processes(ports = ports.values(),event_obj=event_obj,
                                killevent_obj=killevent_obj)
    
    if kill_p.is_alive():
        kill_p.join()

if __name__ == '__main__':
    import getpass
    pswd = getpass.getpass('Password:')
    print(pswd)