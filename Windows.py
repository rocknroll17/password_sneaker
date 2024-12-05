import subprocess
import re
import os

class windows:
    def main(self):
        profiles = self.Windows_get_wifi_profiles()
        for profile in profiles:
            password, formatted_output = self.Windows_get_wifi_password(profile)
            print(f"Profile: {profile}\nPassword: {password}\n\n")
            break

    def Windows_get_wifi_profiles(self):
        profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, encoding='utf-8')
        print(profiles_output)
        profiles = re.findall(r".*:\s*(.+)", profiles_output)
        del profiles[0]
        return profiles

    def Windows_get_wifi_password(self, profile):
        try:
            profile_output = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True, encoding='utf-8', env=dict(os.environ, LANG='en_US.UTF-8'))
            matches = re.findall(r'[^\n]+\n-{5,}[^\n]*\n(?:[^\n]+\n)*\n', profile_output)
            print(profile_output)
            return matches
        except subprocess.CalledProcessError:
            return "[Access Denied]"