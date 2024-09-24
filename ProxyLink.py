import sys

import requests
import random
import time
import os
import re
import webbrowser
import threading
import customtkinter as ctk
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor

init()

# Установка темы
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

base_path = sys._MEIPASS # Убрать, если запускаете не бинарник.
ico = os.path.join(base_path, 'eggplant.ico') # Убрать, если запускаете не бинарник.

root = ctk.CTk()
root.title("ProxyLink")
root.geometry("250x260")
root.iconbitmap(ico)
root.resizable(False, False)


def load_proxies(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
    'Mozilla/5.0 (X11; U; Linux i686; hu-HU; rv:1.9.0.10) Gecko/2009042718 CentOS/3.0.10-1.el5.centos Firefox/3.0.10',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 GTB5 (.NET CLR 4.0.20506)',
    'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.1.4) Gecko/20070704 Firefox/2.0.0.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_2; en-US) AppleWebKit/533.44 (KHTML, like Gecko) Chrome/48.0.1285.356 Safari/601',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_5_9; like Mac OS X) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/49.0.3677.379 Mobile Safari/603.7',
    'Mozilla/5.0 (U; Linux i566 ; en-US) AppleWebKit/601.50 (KHTML, like Gecko) Chrome/51.0.3354.232 Safari/536',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.459.0 Safari/534.3',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/533.3',
    'Mozilla/5.0 (Windows NT 6.1; en-US) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.750.0 Safari/534.30',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
    'Mozilla/5.0 (Windows NT 10.5; Win64; x64; en-US) AppleWebKit/601.30 (KHTML, like Gecko) Chrome/49.0.1371.363 Safari/603.3 Edge/11.57863',
    'Mozilla/5.0 (Windows; Windows NT 10.3; WOW64) AppleWebKit/600.22 (KHTML, like Gecko) Chrome/52.0.2019.219 Safari/535',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.8 (KHTML, like Gecko) Chrome/52.0.3290.285 Safari/535',
    'Mozilla/5.0 (Linux; Android 5.1.1; MOTO X PURE XT1575 Build/LXB22) AppleWebKit/534.49 (KHTML, like Gecko)  Chrome/49.0.2204.224 Mobile Safari/603.6',
    'Mozilla/5.0 (Linux; Android 7.1.1; LG-H900 Build/NRD90C) AppleWebKit/533.21 (KHTML, like Gecko)  Chrome/54.0.2582.269 Mobile Safari/535.1',
    'Mozilla/5.0 (Android; Android 5.0.1; Lenovo A7000-a Build/LRX21M;) AppleWebKit/535.11 (KHTML, like Gecko)  Chrome/54.0.2020.137 Mobile Safari/537.0',
    'Mozilla/5.0 (Android; Android 5.0; SM-P810 Build/LRX22G) AppleWebKit/534.25 (KHTML, like Gecko)  Chrome/48.0.2640.227 Mobile Safari/601.4',
    'Mozilla/5.0 (Android; Android 5.0; SM-T805 Build/LRX22G) AppleWebKit/601.4 (KHTML, like Gecko)  Chrome/49.0.3230.203 Mobile Safari/533.5',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_7; like Mac OS X) AppleWebKit/603.18 (KHTML, like Gecko)  Chrome/54.0.3710.231 Mobile Safari/535.2',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_9_5; like Mac OS X) AppleWebKit/536.45 (KHTML, like Gecko)  Chrome/47.0.1433.129 Mobile Safari/536.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_6; like Mac OS X) AppleWebKit/601.47 (KHTML, like Gecko)  Chrome/51.0.2067.134 Mobile Safari/602.8',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_8; like Mac OS X) AppleWebKit/600.13 (KHTML, like Gecko)  Chrome/49.0.2309.211 Mobile Safari/601.9',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_5; like Mac OS X) AppleWebKit/602.31 (KHTML, like Gecko)  Chrome/51.0.3462.266 Mobile Safari/536.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3_7; like Mac OS X) AppleWebKit/534.5 (KHTML, like Gecko)  Chrome/52.0.1281.367 Mobile Safari/537.4',
    'Mozilla/5.0 (Linux; U; Linux i576 x86_64) Gecko/20100101 Firefox/58.1',
    'Mozilla/5.0 (iPod; CPU iPod OS 9_2_0; like Mac OS X) AppleWebKit/603.43 (KHTML, like Gecko)  Chrome/54.0.3389.110 Mobile Safari/534.3'
]


def send_request_with_proxy(url, proxy):
    global success_responses, bad_responses
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=(15, 22))
        if response.status_code == 200:
            print(Style.BRIGHT + Fore.GREEN + f'Successfully request with {proxy}')
            success_responses += 1
    except requests.exceptions.RequestException as e:
        print(Style.BRIGHT + Fore.RED + f'Error connecting to the proxy {proxy}: {e}')
        bad_responses += 1


def send_request_with_local_ip(url):
    global success_responses, bad_responses
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, timeout=(12, 20))
        if response:
            print(Style.BRIGHT + Fore.GREEN + f'Successfully request with local IP')
            success_responses += 1
    except requests.exceptions.RequestException as e:
        print(f'Error connecting to local IP: {e}')
        bad_responses += 1
    time.sleep(1)


def main(url, workerss):
    proxy_file = 'proxies.txt'
    if not os.path.isfile(proxy_file):
        open(proxy_file, "a").close()

    proxies = load_proxies(proxy_file)
    max_workers = workerss

    while running:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            global executor_stop
            executor_stop = executor

            futures = []
            for proxy in proxies:
                if not running:
                    return
                futures.append(executor.submit(send_request_with_proxy, url, proxy))
                if local_checkbox.get() == 1:
                    if not running:
                        return
                    futures.append(executor.submit(send_request_with_local_ip, url))
            for future in futures:
                try:
                    if not running:
                        break
                    future.result()
                except:
                    pass
        time.sleep(20)


def start_click():
    global running
    running = True
    url = URL.get()
    pattern = r'https?://[^\s]+'

    if re.search(pattern, url):
        workers_max = workers.get()
        workers_max = int(workers_max) if workers_max.isdigit() else 1

        # Блокировка элементов интерфейса
        URL.configure(state='disabled')
        workers.configure(state='disabled')
        local_checkbox.configure(state='disabled')
        start_button.configure(state='disabled')
        stop_button.configure(state='normal')

        thread = threading.Thread(target=main, args=(url, workers_max))
        thread.daemon = True
        thread.start()
    else:
        print("This is not URL")
        URL.configure(placeholder_text='This is not URL.')


def stop_click():
    global running, success_responses, bad_responses
    running = False
    executor_stop.shutdown(cancel_futures=True, wait=False)
    URL.configure(state='normal')
    workers.configure(state='normal')
    local_checkbox.configure(state='normal')
    start_button.configure(state='enabled')
    stop_button.configure(state='disabled')
    try:
        with open("./response_takes.txt", "w") as file:
            file.write(f'Successfully responses: {success_responses}\n Bad responses: {bad_responses}')
    except:
        print(Fore.RED + Style.BRIGHT + 'Received error in process creating file.')
        pass


def validate_int(text):
    return text.isdigit() or text == ""


validate_cmd = root.register(validate_int)

# Настройка интерфейса
label = ctk.CTkLabel(root, text="ProxyLink", font=('Calibri', 24, "bold"), anchor='e')
label.pack(pady=5)


URL = ctk.CTkEntry(root, placeholder_text='URL', fg_color='transparent', font=('Calibri', 12), justify='center')
URL.pack(pady=5)

workers = ctk.CTkEntry(root, placeholder_text='Number of threads', fg_color='transparent', font=('Calibri', 14),
                       justify='center')
workers.pack(pady=5)
workers.configure(validate="key", validatecommand=(validate_cmd, "%P"))

local_checkbox = ctk.CTkCheckBox(root, text='Use local IP address', width=10, font=('Calibri', 14))
local_checkbox.pack(pady=5)

start_button = ctk.CTkButton(root, text='Start', font=('Calibri', 18), command=start_click, hover=True,
                             hover_color='#6495ED')
start_button.pack(pady=5)

stop_button = ctk.CTkButton(root, text='Stop', font=('Calibri', 18), command=stop_click, hover=True,
                            hover_color='#6495ED', state='disabled')
stop_button.pack(pady=5)


def open_url(event):
    webbrowser.open('https://skew.rf.gd')


copyright_skew = ctk.CTkLabel(root, text="Developed by skew", font=('Calibri', 16, "bold"), anchor='e', text_color='#1f538d', cursor="hand2")
copyright_skew.pack(pady=5)

copyright_skew.bind('<Button-1>', open_url)



root.mainloop()
