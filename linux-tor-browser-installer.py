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


from bs4 import BeautifulSoup
import urllib
from os.path import join,basename,isdir,isfile
from os import uname,system,geteuid,chdir,getcwd,remove
from pwd import getpwuid
from shutil import rmtree
import tarfile
import gnupg


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
		
def dm(url,name,size,location,sym="#",symb="-",symx="[",symy="]"):
	old_dir = getcwd()
	chdir(location)
	url        = urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
	opurl      = urllib.request.urlopen(url)
	openfile   = open(name,"wb")
	block_size = 600
	psize = 0
	print (symx+symb*100+symy+" "+str(size)+"b"+" "+"0%",end="\r",flush=True)
	while True:
		count = int((psize*100)//size)
		n = sym * count
		bfr = opurl.read(block_size)
		openfile.write(bfr)
		psize += block_size
		print (symx+n+symb*(100-count)+symy+" "+str(size)+"b"+" "+str(round((psize*100)/size,2))+"%",end="\r",flush=True)
		if psize >= size:
			break
			
	openfile.close()
	print (" "*200,end="\r",flush=True)
	print (symx+sym*100+symy+" "+str(size)+"b"+" "+"100%")
	chdir(old_dir)
	
	
if __name__ == "__main__":
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
			print ("Q To Quit || F To Force Install Tor Browser || R To Remove Tor Browser.")
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

	url = urllib.request.Request("https://www.torproject.org/download/download-easy.html.en",headers={"User-Agent":"Mozilla/5.0"})
	opurl = urllib.request.urlopen(url)
	soup = BeautifulSoup(opurl,"html.parser")


	for a in soup.findAll("a",{"class":button_class}):
		url_tor = urllib.request.Request(join("https://www.torproject.org",a.get("href")[3:]),headers={"User-Agent":"Mozilla/5.0"})
		opurl_tor = urllib.request.urlopen(url_tor)
		tor = basename(url_tor.full_url)
		size  = opurl_tor.headers["Content-Length"]
		tor_download = join("https://www.torproject.org",a.get("href")[3:])

		
	for a in soup.findAll("a",{"class":sig}):
		url_tor_sig = urllib.request.Request(join("https://www.torproject.org",a.get("href")[3:]),headers={"User-Agent":"Mozilla/5.0"})
		opurl_tor_sig = urllib.request.urlopen(url_tor_sig)
		tor_sig = basename(url_tor_sig.full_url)
		size_sig = opurl_tor_sig.headers["Content-Length"]
		tor_download_sig = join("https://www.torproject.org",a.get("href")[3:])

				
		
		
	if not isfile(join(home,"Downloads",tor)):
		print("[#]get {} Size {}".format(tor_download,size))
		try:
			dm(tor_download,tor,int(size),location=join(home,"Downloads"))
			print("\n")
		except:
			exit("\nDownloading {} To {} Fail.".format(tor_download,join(home,"Downloads")))
	
	
	
	
	if not isfile(join(home,"Downloads",tor_sig)):
		print("[#]get {} Size {}".format(tor_download_sig,size_sig))
		try:
			dm(tor_download_sig,tor_sig,int(size_sig),location=join(home,"Downloads"))
			print("\n")
		except:
			exit("\nDownloading {} To {} Fail.".format(tor_download_sig,join(home,"Downloads")))
	
	
	
	
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




