#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  linux-tor-browser-installer.py
#  
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# python3-gnupg
# python3-beautifulsoup4
# python3-requests
# tor


from bs4 import BeautifulSoup
from os.path import join,basename,isdir,isfile
from os import uname,system,geteuid,chdir,getcwd,remove
from pwd import getpwuid
from shutil import rmtree
import tarfile
import gnupg
import requests
import sys
import dbus
import subprocess
import json

def import_key():
	gpg=gnupg.GPG(gnupghome=join(home,".gnupg"))
	gpg.encoding = "utf-8"
	i = gpg.recv_keys("pool.sks-keyservers.net", "0x4E2C6E8793298290")
	if "problem" in i.results[0].keys():
		return False
	return True
	
def check_valid_sg(stream,data_file):
	gpg=gnupg.GPG(gnupghome=join(home,".gnupg"))
	sf=open(stream,"rb")
	v=gpg.verify_file(sf,data_file)
	sf.close()
	return v.valid
	
def extract_tar_xz(location):
	with tarfile.open(location) as f:
		f.extractall(home)
		

def dm(opurl,name,size,location,sym="#",symb="-",symx="[",symy="]",chunk_size = 600):
	old_dir = getcwd()
	chdir(location)
	openfile   = open(name,"wb")
	psize = 0
	print (symx+symb*100+symy+" "+str(size)+"b"+" "+"0%",end="\r",flush=True)
	with open(name, 'wb') as op:
		for chunk in opurl.iter_content(chunk_size=chunk_size):
			count = int((psize*100)//size)
			n = sym * count
			op.write(chunk)
			psize += chunk_size
			print (symx+n+symb*(100-count)+symy+" "+str(size)+"b"+" "+str(round((psize*100)/size,2))+"%",end="\r",flush=True)
			
	print (" "*200,end="\r",flush=True)
	print (symx+sym*100+symy+" "+str(size)+"b"+" "+"100%")
	chdir(old_dir)
	
	
def check_tor_service():
	result = ""
	bus = dbus.SystemBus()
	proxy = bus.get_object("org.freedesktop.systemd1","/org/freedesktop/systemd1")
	interface = dbus.Interface(proxy,"org.freedesktop.systemd1.Manager")
	m = interface.get_dbus_method("ListUnitFiles")
	all_unit_files = m()
	for s in all_unit_files:
		if s[0].endswith("tor.service"):
			result = "ff"
			
	if result=="ff":
		if not service_is_started():
			check = subprocess.call("pkexec systemctl start tor.service",shell=True)
			if check !=0:
				return "f"

	else:
		return "n"
	
	return "s"
	

def service_is_started():
	result = ""
	bus = dbus.SystemBus()
	proxy = bus.get_object("org.freedesktop.systemd1","/org/freedesktop/systemd1")
	interface = dbus.Interface(proxy,"org.freedesktop.systemd1.Manager")
	m = interface.get_dbus_method("GetUnit")
	try:
		m("tor.service")
	except:
		return False
	return True
	
def get_real_ip(status=False):
	url = "http://httpbin.org/ip"
	if status:
		opurl = session.get(url).json()
	else:
		opurl = requests.get(url).json()
	return opurl["origin"]
	
if __name__ == "__main__":
	help_ = """Version : 0.2

linux-tor-browser-installer --without-check-sig || -s       ==> Install without Check File Signature

linux-tor-browser-installer --without-tor  || -t            ==> Download Tor Browser without Tor Network
"""
	if len(sys.argv)>1:
		if "--without-check-sig" in sys.argv or "-s" in sys.argv:
			check_sig = False
		else:
			check_sig = True
		if "--without-tor" in  sys.argv or "-t" in sys.argv:
			with_tor = False
		else:
			with_tor = True
		if "--help" in sys.argv or "-h" in sys.argv:
			exit(help_)
	else:
		check_sig = True
		with_tor  = True
	
	
	if with_tor:
		session = requests.session()
		session.proxies = {'http':  'socks5://127.0.0.1:9050',
                   'https': 'socks5://127.0.0.1:9050'}
	else:
		session = requests
	
	
	agent = {"User-Agent":"Mozilla/5.0"}
	system('setterm -cursor off')

	arch              = uname().machine

	home              = getpwuid(geteuid()).pw_dir

	tor_folder        = join(home,"tor-browser_en-US")

	tor_desktop_entry = join(home,".local/share/applications/start-tor-browser.desktop")

	desktop_entry = """[Desktop Entry]
Type=Application
Name=Tor Browser Setup
GenericName=Web Browser
Comment=Tor Browser is +1 for privacy and -1 for mass surveillance
Categories=Network;WebBrowser;Security;
Exec=sh -c '{}/Browser/start-tor-browser --detach || ([ ! -x {}/Browser/start-tor-browser ] && {}/start-tor-browser --detach)' dummy %k
X-TorBrowser-ExecShell={}/Browser/start-tor-browser --detach
Icon=web-browser
StartupWMClass=Tor Browser
""".format(tor_folder,tor_folder,tor_folder,tor_folder)

	if arch == "x86_64":
		button_class = "button lin-tbb64"
		sig = "lin-tbb64-sig"
	else:
		button_class = "button lin-tbb32"
		sig = "lin-tbb32-sig"



	if isdir(tor_folder) and isfile(tor_desktop_entry):
		while True:
			system("clear")
			print ("\nNothing To Do.")
			print ("Q To Quit || F To Force Reinstall Tor Browser || R To Remove Tor Browser.")
			answer = input("- ").strip()
			if answer == "q" or answer == "Q":
				exit("\nBye...")
			elif answer == "r" or answer == "R":
				try:
					rmtree(tor_folder)
				except:
					exit("Remove {} Fail.".format(tor_folder))
				try:
					remove(tor_desktop_entry)
				except:
					exit("Remove {} Fail.".format(tor_desktop_entry))
				exit("\nRemove Done.")
			elif answer == "f" or answer == "F":
				print ("\n")
				break
	
	
	if  with_tor:
		print ("Old Real IP ====> {}".format(get_real_ip()))
		print("[#]Check/Start Tor Service.")
		check = check_tor_service()
		if  check=="f":
			exit ("-Start Tor Service Fail.")
		elif check == "n":
			exit ("-Error Please Install Tor.")
		else:
			print ("New Real IP ====> {}".format(get_real_ip(True)))
			print ("-Sucess.\n")
			
	url = "https://www.torproject.org/download/download-easy.html.en"
	opurl = session.get(url,headers=agent)
	soup = BeautifulSoup(opurl.text,"html.parser")


	for a in soup.findAll("a",{"class":button_class}):
		tor_download = join("https://www.torproject.org",a.get("href")[3:])
		opurl_tor = session.get(tor_download,stream=True,headers=agent)
		tor = basename(opurl_tor.url)
		size  = opurl_tor.headers["Content-Length"]




		
	for a in soup.findAll("a",{"class":sig}):
		tor_download_sig = join("https://www.torproject.org",a.get("href")[3:])
		opurl_tor_sig = session.get(tor_download_sig,stream=True,headers=agent)
		tor_sig = basename(opurl_tor_sig.url)
		size_sig = opurl_tor_sig.headers["Content-Length"]


				
		
		
	if not isfile(join(home,"Downloads",tor)):
		print("[#]get {} Size {}".format(tor_download,size))
		try:
			dm(opurl_tor,tor,int(size),location=join(home,"Downloads"))
			print("\n")
		except:
			exit("\nDownloading {} To {} Fail.".format(tor_download,join(home,"Downloads")))
	
	
	
	
	if not isfile(join(home,"Downloads",tor_sig)):
		print("[#]get {} Size {}".format(tor_download_sig,size_sig))
		try:
			dm(opurl_tor_sig,tor_sig,int(size_sig),location=join(home,"Downloads"))
			print("\n")
		except:
			exit("\nDownloading {} To {} Fail.".format(tor_download_sig,join(home,"Downloads")))
	
	
	
	if check_sig:
		print ("[#]Start Import GPG Key.")
		if not import_key():
			exit("Import GPG Key Fail.")
		else:
			print ("-Import GPG Key Done.\n")
	
		print ("[#]Start Check Valid signatures.")
		if not check_valid_sg(join(home,"Downloads",tor_sig),join(home,"Downloads",tor)):
			exit("WARNING! Check Valid signatures Fail.")
		print ("-Check Valid signatures Done.\n")
	
	
	
	try:
		print ("[#]Start Extract {} To {}.".format(join(home,"Downloads",tor),home))
		extract_tar_xz(join(home,"Downloads",tor))
	except:
		exit("Extract {} To {} Fail.".format(join(home,"Downloads",tor),home))
	print ("-Extract {} To {} Done.\n".format(join(home,"Downloads",tor),home))
	
	
	
	
	try:
		print ("[#]Start Write {}.".format(tor_desktop_entry))
		with open(tor_desktop_entry,"w") as entry:
			entry.write(desktop_entry)
	except:
		exit("Write {} Fail.".format(tor_desktop_entry))
	print ("-Write {} Done.".format(tor_desktop_entry))
	
	
	
	print ("\nDone.")




