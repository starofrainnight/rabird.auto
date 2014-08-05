
##
# A script to install needed stuffs that required by this rabird_python libraries.
# 
# The hard part is that some libraries could not easily install by easy_install
# or pip, so we have to do it manually.
#
# @author Hong-she Liang <starofrainnight@gmail.com>
# 

import platform
import re
import os
import os.path
import sys
import shutil

def get_cpu_bits():
	return int(re.search(r"(\d+)bit", platform.architecture()[0]).group(1))

def pywin32_get_exe(version):
	if get_cpu_bits() == 32:
		cpu_bits_text = "win32"
	else:
		cpu_bits_text = "win-amd64"
		
	return r"pywin32-%s.%s-py%s.exe" % (version, cpu_bits_text, "%s.%s" % (sys.version_info[0], sys.version_info[1]))

def pywin32_get_url(version):
	return r"http://downloads.sourceforge.net/project/pywin32/pywin32/Build%%20%s/%s" % (
		version, pywin32_get_exe(version))
		
def numpy_get_url(version):
	return r"http://sourceforge.net/projects/numpy/files/NumPy/%s/numpy-%s-win32-superpack-python%s.exe" % (
		version, version, "%s.%s" % (sys.version_info[0], sys.version_info[1]))
		
def scipy_get_url(version):
	return r"http://sourceforge.net/projects/scipy/files/scipy/%s/scipy-%s-win32-superpack-python%s.exe" % (
		version, version, "%s.%s" % (sys.version_info[0], sys.version_info[1]))
		
def pil_get_url(version):
	return r"http://effbot.org/downloads/PIL-%s.win32-py%s.exe" % (version, "%s.%s" % (sys.version_info[0], sys.version_info[1]))

def main():
	wget_command = "%s --no-check-cert " % os.path.realpath(os.path.join(os.curdir, "wget", "wget.exe")) 
	
	os.environ["PATH"] = "%s;%s" % (os.environ["PATH"], os.path.join(sys.exec_prefix, "Scripts"))
	
	requirements = {
		"pywin32": pywin32_get_url("219"),
		"numpy": numpy_get_url("1.8.1"),
		"scipy": scipy_get_url("0.14.0"),
		"pil": pil_get_url("1.1.7"),
		}
		
	os.chdir("cache")
	
	# Install setuptools
	if not os.path.exists("ez_setup.py"):
		os.system("%s %s" % (wget_command, "https://bootstrap.pypa.io/ez_setup.py"))
	os.system("python ez_setup.py")
	
	# Install pip, wheel
	os.system("easy_install pip")
	os.system("easy_install wheel")
	
	# Install cv2 2.4.9, it"s a special package that need to install manually
	if get_cpu_bits() == 32:	
		cv2_cpu_bits_text = "x86"
	else:
		cv2_cpu_bits_text = "x64"
	site_packages_path = os.path.join(sys.exec_prefix, "Lib", "site-packages")
	
	try:
		os.remove(os.path.join(site_packages_path, "cv2.pyd"))
	except:
		pass
		
	# Install pywinio 
	if os.path.exists("pywinio-0.0.7-py2.7.egg"):
		os.system("easy_install pywinio-0.0.7-py2.7.egg")
		
	shutil.copy(os.path.join(os.curdir, "cv2", "2.7", cv2_cpu_bits_text, "cv2.pyd"), site_packages_path)
	
	# Install pycurl, so that we could replace the wget utility.
	os.system("easy_install pycurl")
	
	# Install all requirements
	
	# Filter all files in cache
	all_files = []
	for afile in os.listdir(os.curdir):
		if not os.path.isdir(afile):
			all_files.append(afile)
	
	for requirement, url in requirements.iteritems():
		# If file already downloaded, we just install it.
		is_found = False
		for afile in all_files:
			if not afile.lower().startswith("%s-" % requirement):
				continue
				
			is_found = True
			
			print("%s existed, directly invoke it ..." % afile)
			
			break
			
		if (not is_found) or (os.path.basename(url).lower() != afile.lower()):
			os.system("%s %s" % (wget_command, url))
			afile = os.path.basename(url)
			
		os.system(afile)
		
	# Install all modules.
	modules = ["core", "automation", "gts", "proxy"]
		
	for module in modules:
		module_dir = os.path.join(os.path.dirname(__file__), "..", "..", module)
		if os.path.exists(module_dir):
			os.chdir(module_dir)
			os.system("setup.py install")

if __name__ == "__main__":
    main()

