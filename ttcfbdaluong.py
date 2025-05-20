CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'
import threading
import time, re
import os, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import traceback
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from colorama import Fore, Style
from rich.console import Console
from selenium.webdriver.chrome.options import Options
import logging



os.system("")
console = Console()
frames = ['|', '/', '-', '\\']  
camxuc = {
        "CARE": "Thương thương",
        "LOVE": "Yêu thích",
        "HAHA": "Haha",
        "WOW": "Wow",
        "SAD": "Buồn",
        "ANGRY": "Phẫn nộ"
    }

# Hàm delay chung với tham số cho hành động và thời gian
def delay_action(second, action_text, is_error=False):
    for i in range(int(second * 10), 0, -1):
        icon = frames[i % len(frames)]  # Chọn icon theo bước
        color = RED if is_error else CYAN if i % 2 == 0 else BLUE
        bracket_color = YELLOW if i % 2 == 0 else MAGENTA
        print(f"{color}{icon} {action_text} {bracket_color}[{i//10}.{i%10}s] {RESET}", end="\r")
        time.sleep(0.1)
    print(" " * 60, end="\r")   
def delay(second):
    delay_action(second, "Đang chạy job")
def delay_laplai(second):
    delay_action(second, "Đang lấy job")
def delay_die(second):
    delay_action(second, "Job die => Đang bỏ qua", is_error=True)
def delay_anti(second):
    delay_action(second, "Đang chạy antiband")
def delay_xoa(second):
    delay_action(second, "Đang Chuẩn Bị Tài Nguyên Vào Tool") 
def delay_kt(second):
    delay_action(second, "Tự kiểm tra và đổi acc cho đúng admin xin cảm ơn....") 
# Tạo profile
def login_ttc(driver, username, password):
    driver.get("https://tuongtaccheo.com/home.php")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "submit").click()
    time.sleep(3)

def tao_profile_moi():
    index = 1
    while True:
        new_profile_path = os.path.join(base_path, f"chrome_profile_{index}")
        if not os.path.exists(new_profile_path):
            break
        index += 1

    print(f"{CYAN}➡️ Đang tạo profile chrome_profile_{index}, vui lòng đăng nhập GoLike{RESET}")
    driver = kt_driver(new_profile_path)
    driver.set_window_size(500, 700)
    delay_kt(2)
    driver.get("https://tuongtaccheo.com/home.php")
    user_name = input("Nhập User 👉: ")
    pass_name = input("Nhập Pass 👉: ")
    user_element = driver.find_element(By.NAME, 'username')
    user_element.send_keys(user_name)
    user = user_element.get_attribute("value") # Lấy dữ liệu user
    delay_kt(0.5)
    pass_element = driver.find_element(By.NAME, 'password')
    pass_element.send_keys(pass_name)
    passs = pass_element.get_attribute("value") # Lấy dữ liệu pass
    print(f"user {user} pass {passs}")
    delay_kt(0.5)
    driver.find_element(By.NAME, 'submit').click()
    print("Đang lưu tk mk vào file account.txt", end= "\r")
    save_path = "account_info.txt" # 
    if not os.path.exists(save_path): # Tạo file
        print(f"Tạo mới file: {save_path}")
    with open(save_path, 'a') as f: # Lưu file 
        f.write(f"Username: {user}| Password: {passs}\n")
    print(""*20, end="\r")
    delay_kt(2)
    driver.execute_script("window.open('https://m.facebook.com/login');")
    user_fb = input("👉 Nhập User FB: ")
    pass_fb = input("👉 Nhập Pass FB: ")
    all_tab = driver.window_handles
    driver.switch_to.window(all_tab[1])
    delay_kt(2)
    driver.find_element(By.NAME, 'email').send_keys(user_fb)
    delay_kt(2)
    driver.find_element(By.NAME, 'pass').send_keys(pass_fb)
    delay_kt(2)
    driver.find_element(By.NAME, 'login').click()
    while True:
        driver.get("https://www.facebook.com/friends/")
        delay_kt(2)
        if driver.current_url.startswith("https://www.facebook.com/friends/"):
            print(f"{Fore.GREEN}[✅] Đã đăng nhập Facebook{Style.RESET_ALL}")
            break
        else:
            input("Vui lòng đăng nhập Facebook tay, sau đó bấm Enter...")
            continue
    driver.quit()
    print(f"{GREEN}✅ Đã tạo và lưu chrome_profile_{index}{RESET}")
    return new_profile_path 
base_path = os.path.dirname(os.path.abspath(__file__))
profiles = []        
def load_profiles_from_file():
    profiles = []
    if os.path.exists('profiles.txt'):
        with open('profiles.txt', 'r') as file:     
            profiles = [line.strip().split("\\")[-1] for line in file.readlines()]
    return profiles
profiles = load_profiles_from_file()
def save_profiles_to_file(profiles):
    with open('profiles.txt', 'w') as file:
        for profile in profiles:
            file.write(f"{profile}\n")

def kiem_tra_profile(profiles):
    os.system("cls")
    print("")
    console.print("[bold magenta]              ╔═══╝ Danh sách cá[/bold magenta][bold yellow]c tài khoản ╚═══╗")
    console.print("[bold magenta]             ╙║                               [/bold magenta][bold yellow]  ║╜ ")
    for idx, profile in enumerate(profiles, start=1):
        console.print(f"            [bold magenta] ╙║  [/bold magenta]    [bold yellow][{idx}][/bold yellow] [bold magenta]{profile}[/bold magenta]       [bold yellow]║╜")
    console.print("[bold magenta]             ╙║                               [/bold magenta][bold yellow]  ║╜ ")
    console.print("[bold magenta]              ╚═════════════════[/bold magenta][bold yellow]════════════════╝       ")
    print("")
    lua_chon = console.input("  [[bold yellow]PAP[/bold yellow]|[bold magenta]Nhập số tk muốn chạy[/bold magenta]][bold green]:   ").strip()
    if lua_chon.lower() == 'x':
        return
    
    try:
        lua_chon = int(lua_chon)
        if 1 <= lua_chon <= len(profiles):
            profile_path = profiles[lua_chon - 1]
            print(f"{CYAN}➡️ Đang kiểm tra tài khoản: {profile_path}{RESET}", end="\r")
            
            driver = kt_driver(profile_path)
            driver.set_window_size(500,700)
            # Kiểm tra GoLike
            driver.get("https://tuongtaccheo.com/home.php")
            delay_kt(1)
            driver.execute_script("window.open('https://m.facebook.com/login');")
            # Kiểm tra Facebook
            all_windows = driver.window_handles
            driver.switch_to.window(all_windows[1])
            while True:
                driver.get("https://www.facebook.com/friends/")
                delay_kt(2)
                if driver.current_url.startswith("https://www.facebook.com/friends/"):
                    print(f"{Fore.GREEN}[✅] Đã đăng nhập Facebook: {profile_path}{Style.RESET_ALL}")
                    break
                else:
                    input("Vui lòng đăng nhập Facebook, sau đó bấm Enter...")
                    continue
            input("Không thay đổi gì nữa thì bấm enter rồi bấm 3 !")
            driver.quit()
        else:
            print(f"{RED}⚠️ Số tài khoản không hợp lệ!{RESET}")
    except ValueError:
        print(f"{RED}⚠️ Vui lòng nhập số hợp lệ!{RESET}")
# Lấy dữ liệu
def lay_du_lieu_ttc(file_path="account_info.txt"):
    accounts = []

    try:
        # Mở file và đọc các dòng
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()  # Loại bỏ khoảng trắng đầu và cuối dòng
            if line:  # Kiểm tra dòng không trống
                try:
                    # Tách theo dấu "|"
                    parts = line.split("|")

                    # Kiểm tra nếu dòng có đủ 2 phần: Username và Password
                    if len(parts) == 2:
                        username_part = parts[0].split(":")  # Phần chứa Username
                        password_part = parts[1].split(":")  # Phần chứa Password

                        # Kiểm tra và lấy username và password
                        if len(username_part) > 1 and len(password_part) > 1:
                            username = username_part[1].strip()  # Lấy phần sau dấu ":"
                            password = password_part[1].strip()  # Lấy phần sau dấu ":"

                            # Thêm vào danh sách nếu username và password hợp lệ
                            accounts.append((username, password))

                except Exception as e:
                    print(f"[❌] Lỗi khi xử lý dòng: '{line}': {e}")
                    continue  # Bỏ qua dòng lỗi và tiếp tục với dòng tiếp theo
    except Exception as e:
        print(f"[❌] Lỗi khi đọc file: {e}")

    return accounts


# Làm job like vip
tongxu = 0
biendem = 0
def lam_job_like_vip(driver,index):
    global tongxu, biendem
    try:
        driver.get("https://tuongtaccheo.com/kiemtien/likepostvipcheo/")
        driver.execute_script("document.body.style.zoom = '0.25';")
        driver.execute_script("document.body.style.zoom = '0.25';")
        delay_laplai(5)
        try:
            #tai = driver.find_element(By.ID, 'tailai')
            driver.find_element(By.XPATH ,'/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div').click()
        except:
            try:
                driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
            except:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[2]/div/div/button').click()
                except:
                    return 

        delay(15)
        all_tab = driver.window_handles
        driver.switch_to.window(all_tab[1])
        driver.execute_script("window.scrollBy(0, 500);")
        driver.execute_script("window.scrollBy(0, -500);")
        driver.execute_script("window.scrollBy(0, 500);")
        driver.execute_script("window.scrollBy(0, -500);")
        driver.execute_script("window.scrollBy(0, 500);")  
        driver.execute_script("window.scrollBy(0, -500);")
        found = False 
        try:
            try:
                # like
                modal = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Đóng"]').find_element(By.XPATH, "./ancestor::div[@role='dialog']")
                like = WebDriverWait(modal, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@aria-label="Thích"]')))
            except:
                like = driver.find_element(By.XPATH, '//div[@aria-label="Thích"]')
            try:
                found = True
                ActionChains(driver).move_to_element(like).perform()
                delay(2)
                ActionChains(driver).move_to_element(like).click().perform()
                delay(1)
            except:
                time.sleep(0.1)
            if found:
                handles = driver.window_handles
                driver.switch_to.window(handles[0])
                sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                # Kiểm tra số xu
                oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                soducu = int(oldsodu.text.replace(",", ""))
                driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                delay(10)
                sodumoi = int(oldsodu.text.replace(",", ""))
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                text_to_find = 'Giờ bạn chưa dùng được tính năng này'
                try:
                    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text_to_find}')]")))
                    return False
                except Exception as e:
                    time.sleep(0.5)
                try:
                    ActionChains(driver).move_to_element(like).click().perform()
                except:
                    
                    try:
                        modal = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Đóng"]').find_element(By.XPATH, "./ancestor::div[@role='dialog']")
                        like = WebDriverWait(modal, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@aria-label="Thích"]')))
                    except:
                        like = driver.find_element(By.XPATH, '//div[@aria-label="Thích"]')
                    ActionChains(driver).move_to_element(like).click().perform()
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                driver.close()
                driver.switch_to.window(handles[0])
                if sodumoi > soducu :
                    biendem +=1
                    tongxu +=1100
                    
                    print(f" [Luồng thứ {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Live Vip   {RESET} |{GREEN} +1100 xu{RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                else:
                    print("Job lỗi", end ="\r")
            else:
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                driver.close()
                driver.switch_to.window(handles[0])
                delay(1)
                sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                # Kiểm tra số xu
                oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                soducu = int(oldsodu.text.replace(",", ""))
                driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                delay(10)
                sodumoi = int(oldsodu.text.replace(",", ""))
                if sodumoi > soducu :
                    biendem +=1
                    tongxu += 1100
                    print(f" [Luồng thứ {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Live Vip   {RESET} |{GREEN} +1100 xu{RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")

                else:
                    print("Job lỗi", end ="\r")
        except:
            handles = driver.window_handles
            try:
                driver.switch_to.window(handles[1])
                driver.close()
            except:
                time.sleep(0.2)
            driver.switch_to.window(handles[0])
            time.sleep(0.2)
    except Exception as e:
        handles = driver.window_handles
        try:
            driver.switch_to.window(handles[1])
            driver.close()
        except:
            time.sleep(0.2)
        driver.switch_to.window(handles[0])
def lam_job_like_thuong(driver,index):
    global tongxu, biendem
    try:
        driver.get("https://tuongtaccheo.com/kiemtien/likepostvipre/")
        driver.execute_script("document.body.style.zoom = '0.25';")
        driver.execute_script("document.body.style.zoom = '0.25';")
        delay_laplai(5)
        try:
            #tai = driver.find_element(By.ID, 'tailai')
            driver.find_element(By.XPATH ,'/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div').click()
        except:
            try:
                driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
            except:
                try:
                    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[2]/div/div/button').click()
                except:
                    return 

        delay(15)
        all_tab = driver.window_handles
        driver.switch_to.window(all_tab[1])
        driver.execute_script("window.scrollBy(0, 500);")
        driver.execute_script("window.scrollBy(0, -500);")
        driver.execute_script("window.scrollBy(0, 500);")
        driver.execute_script("window.scrollBy(0, -500);")
        driver.execute_script("window.scrollBy(0, 500);")  
        driver.execute_script("window.scrollBy(0, -500);")
        found = False 
        try:
            try:
                # like
                modal = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Đóng"]').find_element(By.XPATH, "./ancestor::div[@role='dialog']")
                like = WebDriverWait(modal, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@aria-label="Thích"]')))
            except:
                like = driver.find_element(By.XPATH, '//div[@aria-label="Thích"]')
            try:
                found = True
                ActionChains(driver).move_to_element(like).perform()
                delay(2)
                ActionChains(driver).move_to_element(like).click().perform()
                delay(1)
            except:
                time.sleep(0.1)
            if found:
                handles = driver.window_handles
                driver.switch_to.window(handles[0])
                sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                # Kiểm tra số xu
                oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                soducu = int(oldsodu.text.replace(",", ""))
                driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                delay(10)
                sodumoi = int(oldsodu.text.replace(",", ""))
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                delay(1)
                text_to_find = 'Giờ bạn chưa dùng được tính năng này'
                try:
                    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text_to_find}')]")))
                    return False
                except Exception as e:
                    time.sleep(0.5)
                try:
                    ActionChains(driver).move_to_element(like).click().perform()
                except:
                    
                    try:
                        modal = driver.find_element(By.XPATH, '//div[@role="dialog"]//div[@aria-label="Đóng"]').find_element(By.XPATH, "./ancestor::div[@role='dialog']")
                        like = WebDriverWait(modal, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@aria-label="Thích"]')))
                    except:
                        like = driver.find_element(By.XPATH, '//div[@aria-label="Thích"]')
                    ActionChains(driver).move_to_element(like).click().perform()
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                driver.close()
                driver.switch_to.window(handles[0])
                if sodumoi > soducu :
                    biendem +=1
                    tongxu += 600

                    print(f" [Luồng thứ {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Like Rẻ    {RESET} |{GREEN} +600  xu{RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                else:
                    print("Job lỗi", end ="\r")
            else:
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                driver.close()
                driver.switch_to.window(handles[0])
                delay(1)
                sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                # Kiểm tra số xu
                oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                soducu = int(oldsodu.text.replace(",", ""))
                driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                delay(10)
                sodumoi = int(oldsodu.text.replace(",", ""))
                if sodumoi > soducu :
                    biendem +=1
                    tongxu += 1100
                    print(f" [Luồng thứ {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Like Rẻ    {RESET} |{GREEN} +600  xu{RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                else:
                    print("Job lỗi", end ="\r")
        except:
            handles = driver.window_handles
            try:
                driver.switch_to.window(handles[1])
                driver.close()
            except:
                time.sleep(0.2)
            driver.switch_to.window(handles[0])
            time.sleep(0.2)
    except Exception as e:
        handles = driver.window_handles
        try:
            driver.switch_to.window(handles[1])
            driver.close()
        except:
            time.sleep(0.2)
        driver.switch_to.window(handles[0])

def lam_job_camxuc_vip(driver,index):
    global tongxu, biendem
    try:
        driver.get("https://tuongtaccheo.com/kiemtien/camxucvipcheo/")
        driver.execute_script("document.body.style.zoom = '0.25';")
        driver.execute_script("document.body.style.zoom = '0.25';")
        delay_laplai(5)
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[starts-with(@onclick, 'like')]"))
            )
            onclick_value = btn.get_attribute("onclick")
            matches = re.findall(r"'(.*?)'", onclick_value)
            if matches:
                last_argument = matches[-1]
                kt_job = camxuc.get(last_argument)
                if kt_job is None:
                    print(f"Không tìm thấy '{last_argument}' trong camxuc", end="\r")
            else:
                print(f"onclick không hợp lệ: {onclick_value}", end="\r")
        except Exception as e:
            print("Lỗi khi tìm nút like: {e}", end="\r" )
        btn.click()
        
        if kt_job:
            delay(15)
            all_tab = driver.window_handles
            driver.switch_to.window(all_tab[1])
            driver.execute_script("window.scrollBy(0, 500);")
            driver.execute_script("window.scrollBy(0, -500);")
            driver.execute_script("window.scrollBy(0, 500);")
            driver.execute_script("window.scrollBy(0, -500);")
            driver.execute_script("window.scrollBy(0, 500);")  
            driver.execute_script("window.scrollBy(0, -500);")
            found = False 
            try:

                like_xpaths = [
        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/span/i",  # Xpath bình thường
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/span",  # Xpath video
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/div/div/span/div[1]/div/div/span",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/span/i",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[3]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/div/div/span/div[1]/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[3]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[3]/div/div/div/div/div[1]/div/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[2]/div/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]"
    ]
                found = False
                for xpath in like_xpaths:
                    try:
                        element = driver.find_element(By.XPATH, xpath)
                        found = True
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()
                        delay(3)
                        
                        if kt_job:
                            try:
                                reaction_button = driver.find_element(By.XPATH, f'//div[@aria-label="{kt_job}"]')
                                reaction_button.click()
                            except:
                                time.sleep(0.1)
                    except:
                        time.sleep(0.7)
                    
                        
                if found:
                    
                    handles = driver.window_handles
                    driver.switch_to.window(handles[0])
                    sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                    # Kiểm tra số xu
                    oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                    soducu = int(oldsodu.text.replace(",", ""))
                    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                    delay(10)
                    sodumoi = int(oldsodu.text.replace(",", ""))
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    text_to_find = 'Giờ bạn chưa dùng được tính năng này'
                    try:
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text_to_find}')]")))
                        return False
                    except Exception as e:
                        time.sleep(0.2)
                        for xpath in like_xpaths:
                            try:
                                element = driver.find_element(By.XPATH, xpath)
                                found = True
                                actions = ActionChains(driver)
                                actions.move_to_element(element).perform()
                                delay(1)
                                actions.move_to_element(element).click().perform()
                            except:
                                time.sleep(0.7)
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    driver.close()
                    driver.switch_to.window(handles[0])
                    if sodumoi > soducu :
                        biendem +=1
                        tongxu += 1100
                        print(f" [Luồng {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Cảm Xúc Vip{RESET} |{GREEN} +1100 xu{RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                    else:
                        print("Job lỗi", end ="\r")
                else:
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    driver.close()
                    driver.switch_to.window(handles[0])
                    delay(1)
                    sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                # Kiểm tra số xu
                    oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                    soducu = int(oldsodu.text.replace(",", ""))
                    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                    delay(10)
                    sodumoi = int(oldsodu.text.replace(",", ""))
                    if sodumoi > soducu :
                        biendem +=1
                        tongxu += 1100
                        print(f" [Luồng thứ {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Cảm Xúc Vip{RESET} |{GREEN} +1100 xu{RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                    else:
                        print("Job lỗi", end ="\r")
            except:
                handles = driver.window_handles
                try:
                    driver.switch_to.window(handles[1])
                    driver.close()
                except:
                    time.sleep(0.2)
                driver.switch_to.window(handles[0])
                time.sleep(0.2)
        else:
            handles = driver.window_handles
            try:
                driver.switch_to.window(handles[1])
                driver.close()
            except:
                time.sleep(0.2)
            driver.switch_to.window(handles[0])
            time.sleep(0.2)
    except Exception as e:
        handles = driver.window_handles
        try:
            driver.switch_to.window(handles[1])
            driver.close()
        except:
            time.sleep(0.2)
        driver.switch_to.window(handles[0])
def lam_job_camxuc_re(driver,index):
    global tongxu, biendem
    try:
        driver.get("https://tuongtaccheo.com/kiemtien/camxucvipre/")
        driver.execute_script("document.body.style.zoom = '0.25';")
        driver.execute_script("document.body.style.zoom = '0.25';")
        delay_laplai(3)
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[starts-with(@onclick, 'like')]"))
            )
            onclick_value = btn.get_attribute("onclick")
            matches = re.findall(r"'(.*?)'", onclick_value)
            if matches:
                last_argument = matches[-1]
                kt_job = camxuc.get(last_argument)
                if kt_job is None:
                    print(f"Không tìm thấy '{last_argument}' trong camxuc", end="\r")
            else:
                print(f"onclick không hợp lệ: {onclick_value}", end="\r")
        except Exception as e:
            print("Lỗi khi tìm nút like: {e}", end="\r" )
        btn.click()
        
        if kt_job:
            delay(15)
            all_tab = driver.window_handles
            driver.switch_to.window(all_tab[1])
            driver.execute_script("window.scrollBy(0, 500);")
            driver.execute_script("window.scrollBy(0, -500);")
            driver.execute_script("window.scrollBy(0, 500);")
            driver.execute_script("window.scrollBy(0, -500);")
            driver.execute_script("window.scrollBy(0, 500);")  
            driver.execute_script("window.scrollBy(0, -500);")
            found = False 
            try:

                like_xpaths = [
        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/span/i",  # Xpath bình thường
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/span",  # Xpath video
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/div/div/span/div[1]/div/div/span",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/span/i",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[3]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/div/div/span/div[1]/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[3]/div/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[3]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[3]/div/div/div/div/div[1]/div/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[2]/div/div",
        "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]"
    ]
                found = False
                for xpath in like_xpaths:
                    try:
                        element = driver.find_element(By.XPATH, xpath)
                        found = True
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()
                        delay(3)
                        
                        if kt_job:
                            try:
                                reaction_button = driver.find_element(By.XPATH, f'//div[@aria-label="{kt_job}"]')
                                reaction_button.click()
                            except:
                                time.sleep(0.1)
                    except:
                        time.sleep(0.7)
                    
                        
                if found:
                    
                    handles = driver.window_handles
                    driver.switch_to.window(handles[0])
                    sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                    # Kiểm tra số xu
                    oldsodu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                    soducu = int(oldsodu.text.replace(",", ""))
                    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                    delay(10)
                    sodumoi = int(oldsodu.text.replace(",", ""))
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    text_to_find = 'Giờ bạn chưa dùng được tính năng này'
                    try:
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text_to_find}')]")))
                        return False
                    except Exception as e:
                        time.sleep(0.2)
                        for xpath in like_xpaths:
                            try:
                                element = driver.find_element(By.XPATH, xpath)
                                found = True
                                actions = ActionChains(driver)
                                actions.move_to_element(element).perform()
                                delay(1)
                                actions.move_to_element(element).click().perform()
                            except:
                                time.sleep(0.7)
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    driver.close()
                    driver.switch_to.window(handles[0])
                    if sodumoi > soducu :
                        biendem +=1
                        tongxu += 600
                        print(f" [Luồng thứ {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Cảm Xúc Rẻ {RESET} |{GREEN} +600  xu {RESET}| {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                    else:
                        print("Job lỗi", end ="\r")
                else:
                    handles = driver.window_handles
                    driver.switch_to.window(handles[1])
                    driver.close()
                    driver.switch_to.window(handles[0])
                    delay(2)
                    sodu_xpath = "/html/body/div[1]/div/nav/div/div[2]/ul[2]/li[2]/a/strong"
                # Kiểm tra số xu
                    oldsodu  = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sodu_xpath)))
                    soducu = int(oldsodu.text.replace(",", ""))
                    driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div/div[1]/div/div/button').click()
                    delay(10)
                    sodumoi = int(oldsodu.text.replace(",", ""))
                    if sodumoi > soducu :
                        biendem +=1
                        tongxu += 1100
                        print(f" [Luồng {index}] {CYAN}| {biendem} |  FACEBOOK  | {RED} Cảm Xúc Rẻ {RESET} |{GREEN} +600 xu {RESET} | {YELLOW}Tổng: {tongxu}{RESET} | {MAGENTA}Xu: {sodumoi}{RESET} | {BLUE}Time: {datetime.now().strftime('%H:%M:%S')}{RESET} | ")
                    else:
                        print("Job lỗi", end ="\r")
            except:
                handles = driver.window_handles
                try:
                    driver.switch_to.window(handles[1])
                    driver.close()
                except:
                    time.sleep(0.2)
                driver.switch_to.window(handles[0])
                time.sleep(0.2)
        else:
            handles = driver.window_handles
            try:
                driver.switch_to.window(handles[1])
                driver.close()
            except:
                time.sleep(0.2)
            driver.switch_to.window(handles[0])
            time.sleep(0.2)
    except Exception as e:
        handles = driver.window_handles
        try:
            driver.switch_to.window(handles[1])
            driver.close()
        except:
            time.sleep(0.2)
        driver.switch_to.window(handles[0])
         
# Hàm tạo driver với profile
def kt_driver(profile_path, headless=False):
    options = webdriver.ChromeOptions() 
    options.add_argument("--log-level=3")
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    driver = webdriver.Chrome(options=options)
    return driver
def create_driver(profile_path, headless=False):
    os.environ["PYTHONWARNINGS"] = "ignore"  # tắt cảnh báo python
    logging.basicConfig(level=logging.WARNING)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--force-device-scale-factor=0.1")
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    #mobile_ua = "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"
    #options.add_argument(f"--user-agent={mobile_ua}")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")  # 0=INFO, 1=WARNING, 2=LOG_ERROR, 3=LOG_FATAL
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--enable-unsafe-webgpu") 
    options.add_argument("--disable-features=VoiceTranscriptionCapability")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {
    "profile.default_content_setting_values": {
        "images": 1,      # Load ảnh bình thường
        "javascript": 1,  # Chạy JavaScript đầy đủ
        "cookies": 1,      # Không chặn cookie
        "popups": 1,       # Không chặn popup
        "plugins": 1       # Load tất cả plugin
    }
} 
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--memory-pressure-off")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-features=MediaEngagementBypassAutoplayPolicies")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--disable-background-video-track")
    options.add_argument("--disable-background-media-suspend")
    options.add_argument("--disable-webrtc-hw-decoding")
    options.add_argument("--disable-webrtc-hw-encoding")
    for arg in [  
    "--no-sandbox", "--disable-gpu", "--disable-software-rasterizer",  
    "--disable-dev-shm-usage", "--disable-crash-reporter", "--disable-extensions",  
    "--disable-in-process-stack-traces", "--disable-logging", "--disable-background-video-track",  
    "--disable-features=MediaEngagementBypassAutoplayPolicies,PreloadMediaEngagementData,WebRTC,WebAudio,AutoplayIgnoreWebAudio",  
    "--blink-settings=imagesEnabled=false", "--disable-sync", "--disable-background-timer-throttling",  
    "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",  
    
    ]: options.add_argument(arg) 
    for arg in ["--disable-features=MediaEngagementBypassAutoplayPolicies,PreloadMediaEngagementData,WebRTC,WebAudio,AutoplayIgnoreWebAudio",
            "--disable-background-video-track", "--disable-accelerated-video-decode", "--disable-software-rasterizer"]: options.add_argument(arg)  
    options.add_argument("--disable-gesture-requirement-for-media-playback")  # Ngăn video chạy tự động
    options.add_argument("--disable-animations")
    options.add_argument("--disable-sync")  # Tắt đồng bộ Chrome
    options.add_argument("--metrics-recording-only")  # Chỉ ghi nhận dữ liệu cần thiết
    options.add_argument("--mute-audio")  # Tắt âm thanh (giảm xử lý đa phương tiện
    options.add_argument("--disable-popup-blocking")  # Tắt chặn pop-up (tránh lỗi)
    options.add_argument("--disable-infobars")  # Ẩn thông báo "Chrome đang được điều khiển..."
    options.add_argument("--disable-notifications")  # Chặn thông báo từ web
    options.add_argument("--disable-save-password-bubble")  # Tắt gợi ý lưu mật khẩu
    options.add_argument("--disable-translate")  # Tắt tính năng dịch của Chrome
    options.add_argument("--disk-cache-size=1000000000")  # 1GB cache
    options.add_argument("--disable-features=ScriptStreaming")  # Giảm tải xử lý JS
    options.add_argument("--mute-audio")
    options.add_argument("--process-per-site")  # Giảm số process của Chrome
    options.add_argument("--disable-backgrounding-occluded-windows")  
    options.add_argument("--disable-renderer-backgrounding")  
    options.add_argument("--disable-features=ScriptStreaming") 
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--no-ssl-cert-check") 
    options.add_argument("--disable-software-rasterizer")  
    prefs = {"profile.managed_default_content_settings.images": 2, 
    "profile.managed_default_content_settings.stylesheets": 2, 
    "profile.managed_default_content_settings.fonts": 2}  
    options.add_experimental_option("prefs", prefs) 
    options.add_argument("--disable-gpu") 
    if headless:
        options.headless = True
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    return driver
# Hàm làm nhiệm vụ Facebook Like cho mỗi profile
def lam_job(profile_path, username, password, index=0):
    driver = create_driver(profile_path, headless=False)
    driver.set_window_size(800, 500)
    driver.set_window_position(x=1500 * index, y=0 )
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        login_ttc(driver, username, password)
    except:
        time.sleep(0.2)
    while True:
        delay_laplai(1)
        lam_job_camxuc_vip(driver, index)
        lam_job_like_vip(driver, index)
        lam_job_like_thuong(driver, index)
        lam_job_camxuc_re(driver,index)
# Hàm chạy đa luồng với delay giữa các luồng
def chay_da_luong(profile_paths, delay=20):
    accounts = lay_du_lieu_ttc(file_path="account_info.txt")  # Lấy danh sách tài khoản
    print(f"Đã đọc {len(accounts)} tài khoản từ file.")
    print(f"Đã nhận được {len(profile_paths)} profile paths.")
    
    # Kiểm tra dữ liệu tài khoản
    for i, (username, password) in enumerate(accounts):
        print(f"Tài khoản {i}: {username} | {password}")

    threads = []

    # Kiểm tra nếu số lượng tài khoản không đủ
    if len(accounts) < len(profile_paths):
        print(f"[WARNING] Có {len(profile_paths) - len(accounts)} profile paths nhưng chỉ có {len(accounts)} tài khoản.")
        # Nếu không đủ tài khoản, có thể sẽ bị thiếu tài khoản cho các profile paths sau
        # Bạn có thể lặp lại tài khoản nếu muốn hoặc xử lý theo cách khác.

    # Lặp qua profile_paths và tạo các luồng
    for index, profile_path in enumerate(profile_paths):
        # Kiểm tra nếu còn tài khoản để sử dụng
        if index < len(accounts):
            username, password = accounts[index]  # Lấy username, password từ tài khoản
        else:
            print(f"[ERROR] Không đủ tài khoản cho profile path {profile_path}. Dừng lại.")
            break

        time.sleep(delay)
        t = threading.Thread(target=lam_job, args=(profile_path, username, password, index))
        t.daemon = True  # Đảm bảo luồng tự động kết thúc khi chương trình kết thúc
        print(f"Đang mở: {profile_path} [Luồng {index}] ")
        t.start()
        threads.append(t)

    # Đợi tất cả các luồng hoàn thành
    for t in threads:
        t.join()

def tat_chrome_hieu_ung():
    os.system('taskkill /f /im chrome.exe >nul 2>&1')
def giaodien():
    console.print("[bold magenta]                    Chào mừng bn[/bold magenta][bold yellow] đến với[/bold yellow] tool TTCFB ĐA LUỒNG VIP")
    console.print("[bold magenta]                 ╚═╦════════════[/bold magenta][bold yellow]══════════╦═╝")
    console.print("[bold magenta]═════════════════════[ TTC Faceb[/bold magenta][bold yellow]ook ]═══════════════════════[/bold yellow]")
 #Menu UI
def ui():
    while True:
        #tat_chrome_hieu_ung()
        #delay_xoa(5)
        os.system('cls')
        giaodien()
        print("")
        console.print("[bold magenta][[bold yellow]1[/bold yellow]]  Thêm tài khoản tuongtaccheo[/bold magenta]")
        console.print("[bold magenta][[bold yellow]2[/bold yellow]]  Kiểm tra đăng nhập tuongtaccheo[/bold magenta]")
        console.print("[bold magenta][[bold yellow]3[/bold yellow]]  Làm nhiệm vụ cùng lúc đa luồng (đồng thời)[/bold magenta]")
        console.print("[bold magenta][[bold yellow]X[/bold yellow]]  Thoát[/bold magenta]")
        print("")
        lua_chon = console.input("  [[bold yellow]PAP[/bold yellow]|[bold magenta]Nhập sô[/bold magenta]][bold green]:     ")
        profiles = load_profiles_from_file()  # Đọc lại danh sách profile từ file

        if lua_chon == "1":
            profile_path = tao_profile_moi()
            if profile_path not in profiles:
                profiles.append(profile_path)
                save_profiles_to_file(profiles)  # Lưu lại danh sách profile vào file
        elif lua_chon == "2":
            kiem_tra_profile(profiles)

        elif lua_chon == "3":
            
            try:
        
                chay_da_luong(profiles)
            except Exception as e:
                print(e)
                break
        elif lua_chon.lower() == "x":
            break
# Thực thi chương trình với 3 profile
if __name__ == "__main__":
    ui()






    
