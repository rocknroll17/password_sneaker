import subprocess
import re
import os
from collections import Counter

class InformationNotFound(Exception):
    def __init__(self, message="Password Information not found"):
        self.message = message
        super().__init__(self.message)

class windows:
    keywords = ["CCMP", "GCMP", "WEP", "TKIP", "WPA"]
    def main(self):
        profiles = self.Windows_get_wifi_profiles()
        for profile in profiles:
            password = self.Windows_get_wifi_password(profile)
            if password is None:
                continue
            print(f"Profile: {profile}\nPassword: {password}\n")

    def Windows_get_wifi_profiles(self):
        profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, encoding='utf-8')
        profiles = re.findall(r".*:\s*(.+)", profiles_output)
        del profiles[0]
        return profiles

    def Windows_get_wifi_password(self, profile):
        try:
            profile_output = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True, encoding='utf-8', env=dict(os.environ, LANG='en_US.UTF-8'))
            matches = re.findall(r'[^\n]+\n-{5,}[^\n]*\n(?:[^\n]+\n)*\n', profile_output)
            count = Counter()
            max_index = None
            for i, match in enumerate(matches):
                count[i] = sum(match.count(keyword) for keyword in windows.keywords if keyword in match)
            if count and all(value == 0 for value in count.values()):
                return None
            else:
                max_index = max(count, key=count.get)
                password_paragraph = matches[max_index]
            password = re.findall(r'[^\n]+\n', password_paragraph)[-1].split(":")[-1].strip()
            return password
        except subprocess.CalledProcessError:
            return "[Access Denied]"