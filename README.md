# linux-tor-browser-installer 0.3
Python Script To Install Tor Browser

www.arfedora.blogspot.com


# Requires
 *  ```python3 ```
 * ``` python3-gnupg ```
 * ``` python3-beautifulsoup4 ```
 * ``` python3-requests ```
 * ``` tor ```
 * ``` python3-dbus ```

# Install Requires (Fedora)
 * ``` sudo dnf install git tor python3-dbus python3-requests python3-beautifulsoup4 python3-gnupg ```

# Copr Repository (For Fedora)
 * ``` sudo  dnf copr enable youssefmsourani/linux-tor-browser-installer -y  ```
 * ``` sudo dnf install linux-tor-browser-installer -y ```
 * ``` linux-tor-browser-installer ``
  
# To Use
 * ``` cd && git clone https://github.com/yucefsourani/linux-tor-browser-installer ```

 * ``` chmod 755 ~/linux-tor-browser-installer/linux-tor-browser-installer.py ```

 * ``` ~/linux-tor-browser-installer/linux-tor-browser-installer.py```
 
 
# Options
 * ``` --without-check-sig || -s       ==> Install without Check File Signature  ```
 * ``` --without-tor       || -t       ==> Download Tor Browser without Tor Network ```

