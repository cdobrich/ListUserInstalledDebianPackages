
"""
Description: List all packages manually installed (by users, by admin/root, or both), as determined by the Debian package system.
"""

def main():
	"""
	Parse any input arguments and process.
	"""
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--default', action='store_true', help="list intersecting packages from processing both apt history logs and apt-mark showmanual")
	parser.add_argument('--aptMark', action='store_true', help="list packages only from processing apt-mark showmanual")
	parser.add_argument('--aptHistory', action='store_true', help="list packages only from processing apt history logs")
	args = parser.parse_args()
	if args.default:
		CombineListsAllInstalledPackages()
	elif args.aptMark:
		dpkgAllPackageSet = DpkgAllPackageStatus()
		aptMarkSet = AptMarkShowManualPackageNames()

		finalSet = dpkgAllPackageSet.intersection(aptMarkSet)

		jointVerdict = list(finalSet)
		jointVerdict.sort()
		for item in jointVerdict:
			print(item)
	elif args.aptHistory:
		dpkgAllPackageSet = DpkgAllPackageStatus()
		aptHistorySet = AptLogHistoryPackageNames()

		finalSet = dpkgAllPackageSet.intersection(aptHistorySet)

		jointVerdict = list(finalSet)
		jointVerdict.sort()
		for item in jointVerdict:
			print(item)
	else:
		CombineListsAllInstalledPackages()

def CombineListsAllInstalledPackages():
	"""
	Combine and display the results of both querying the Debian package tool
	Apt-Mark and manually parsing the logs in /var/log/dpkg.log*. Then display
	the combined output.
	"""
	dpkgAllPackageSet = DpkgAllPackageStatus()
	aptHistorySet = AptLogHistoryPackageNames()
	aptMarkSet = AptMarkShowManualPackageNames()

	finalSet = aptMarkSet.union(aptHistorySet)
	finalSet = dpkgAllPackageSet.intersection(finalSet)

	jointVerdict = list(finalSet)
	jointVerdict.sort()
	for item in jointVerdict:
		print(item)

def DpkgAllPackageStatus():
	"""
	Get a Set of strings for ALL installed packages according to the Debian
	dpkg system, by reading /var/lib/dpkg/status.

	For brevity of development, no sophisticated testing for whether a file does
	not conform to the listed expected input. This can be added later if desired.

	@assumptions: The extected input file is /var/lib/dpkg/status. We do not
	account for any prior log files like status-old.

	@return Set-object of strings for all installed packages
	"""
	from pathlib import Path
	import re

	INDEX_DPKG_STATUS_PACKAGE_STRING = 1

	packageNamesFromLogs = set()

	# Get list of all existing DPKG logs in /var/log/dpkg.log*
	dpkgStatusPath = "/var/lib/dpkg/status"
	openedDpkgStatusPath = Path(dpkgStatusPath)

	fileOpened = open(openedDpkgStatusPath, 'r')
	contents = fileOpened.readlines()
	fileOpened.close()
	for line in contents:
		if re.search(r'^Package: ', line):
			splits = line.strip().split(' ')
			packageNamesFromLogs.add(splits[INDEX_DPKG_STATUS_PACKAGE_STRING])

	return packageNamesFromLogs


def AptMarkShowManualPackageNames():
	"""
	Get a Set of strings for all manually installed packages byaccording to the system tool Apt-Mark.

	NOTE: Chose to use subprocess.check_output for older Python compatiblity
	because this is simple.

	@return Set-object of strings for all installed packages
	"""
	import subprocess

	packageNamesAptMarkShowManual = set()

	output = subprocess.check_output(['apt-mark', 'showmanual'])
	contents = output.decode('utf-8')
	for line in contents.splitlines():
		packageNamesAptMarkShowManual.add(line)

	return packageNamesAptMarkShowManual


def AptLogHistoryPackageNames():
	"""
	Generate a Set of strings for all manually installed packages by parsing
	the Apt history log files for the express 'apt install ' and retrieving
	all items listed after that text.

	Note this does not account for if they have been removed.

	@return Set-object of strings for all installed packages
	"""
	from pathlib import Path
	import gzip
	import io
	import os
	import re

	INDEX_APT_HISTORY_LOG_PACKAGE_NAME = 3

	packageNamesFromLogs = set()

	# Get list of all existing DPKG logs in /var/log/apt/history.log*
	aptLogPath = "/var/log/apt"
	openedAptLogPath = Path(aptLogPath)

	for file in list(openedAptLogPath.glob('**/history.log*')):
		# Only read expected text-files and gzip-text files
		fileName,ext = os.path.splitext(file)
		if ext == '.log' or re.search( r'\d+', ext):
			# Process as plain text-file
			fileOpened = open(file, 'r')
			contents = fileOpened.readlines()
			fileOpened.close()
			for line in contents:
				if re.search(r'apt install ', line):
					splits = line.strip().split(' ')
					packageNamesFromLogs.add(splits[INDEX_APT_HISTORY_LOG_PACKAGE_NAME])
		elif ext == '.gz':
			# Process as Gzip file
			with gzip.open(file,'r') as gzipFile: # open the gzip file read-only
				with io.TextIOWrapper(gzipFile, encoding='utf-8') as decoder: # decode the gzip file contents
					contents = decoder.readlines() # Get contents line by line

					for line in contents:
						if re.search(r'apt install ', line):
							splits = line.strip().split(' ')
							# Get all items on the install command history line
							for item in splits[INDEX_APT_HISTORY_LOG_PACKAGE_NAME:]:
								packageNamesFromLogs.add(item)

	return packageNamesFromLogs


if __name__ == '__main__':
	"""
	Invoke the main dispatcher function.
	"""
	main()
