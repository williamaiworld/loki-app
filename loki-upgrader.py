#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- coding: utf-8 -*-
#
# LOKI Upgrader
try:
 from urllib2 import urlopen
except ImportError:
 from urllib.request import urlopen #For python 3.5
import json
import zipfile
import shutil
try:
 from StringIO import StringIO
except ImportError:
 from io import StringIO
import os
import argparse
import traceback
from sys import platform as _platform

# Win32 Imports
if _platform == "win32":
    try:
        import wmi
        import win32api
        from win32com.shell import shell
    except Exception, e:
        platform = "linux"  # crazy guess


from lib.lokilogger import *

# Platform
platform = ""
if _platform == "linux" or _platform == "linux2":
    platform = "linux"
elif _platform == "darwin":
    platform = "osx"
elif _platform == "win32":
    platform = "windows"

class LOKIUpdater(object):
    
    UPDATE_URL_SIGS = ["https://github.com/Neo23x0/signature-base/archive/master.zip",
                       "https://github.com/SupportIntelligence/Icewater/archive/master.zip"]
    UPDATE_URL_LOKI = "https://api.github.com/repos/Neo23x0/Loki/releases/latest"
    
    def __init__(self, debug, logger, application_path):
        self.debug = debug
        self.logger = logger
        self.application_path = application_path

    def update_signatures(self):
        try:
            for sig_url in self.UPDATE_URL_SIGS:
                # Downloading current repository
                try:
                    self.logger.log("INFO", "Downloading %s ..." % sig_url)
                    response = urlopen(sig_url)
                except Exception as e:
                    if self.debug:
                        traceback.print_exc()
                    self.logger.log("ERROR", "Error downloading the signature database - check your Internet connection")
                    sys.exit(1)

                # Preparations
                try:
                    sigDir = os.path.join(self.application_path, './signature-base/')
                    for outDir in ['', 'iocs', 'yara', 'misc']:
                        fullOutDir = os.path.join(sigDir, outDir)
                        if not os.path.exists(fullOutDir):
                            os.makedirs(fullOutDir)
                except Exception as e:
                    if self.debug:
                        traceback.print_exc()
                    self.logger.log("ERROR", "Error while creating the signature-base directories")
                    sys.exit(1)

                # Read ZIP file
                try:
                    zipUpdate = zipfile.ZipFile(StringIO(response.read()))
                    for zipFilePath in zipUpdate.namelist():
                        sigName = os.path.basename(zipFilePath)
                        if zipFilePath.endswith("/"):
                            continue
                        self.logger.log("DEBUG", "Extracting %s ..." % zipFilePath)
                        if "/iocs/" in zipFilePath and zipFilePath.endswith(".txt"):
                            targetFile = os.path.join(sigDir, "iocs", sigName)
                        elif "/yara/" in zipFilePath and zipFilePath.endswith(".yar"):
                            targetFile = os.path.join(sigDir, "yara", sigName)
                        elif "/misc/" in zipFilePath and zipFilePath.endswith(".txt"):
                            targetFile = os.path.join(sigDir, "misc", sigName)
                        elif zipFilePath.endswith(".yara"):
                            targetFile = os.path.join(sigDir, "yara", sigName)
                        else:
                            continue

                        # New file
                        if not os.path.exists(targetFile):
                            self.logger.log("INFO", "New signature file: %s" % sigName)

                        # Extract file
                        source = zipUpdate.open(zipFilePath)
                        target = file(targetFile, "wb")
                        with source, target:
                            shutil.copyfileobj(source, target)

                except Exception as e:
                    if self.debug:
                        traceback.print_exc()
                    self.logger.log("ERROR", "Error while extracting the signature files from the download package")
                    sys.exit(1)

        except Exception as e:
            if self.debug:
                traceback.print_exc()
            return False
        return True


    def update_loki(self):
        try:

            # Downloading the info for latest release
            try:
                self.logger.log("INFO", "Checking location of latest release %s ..." % self.UPDATE_URL_LOKI)
                response_info = urlopen(self.UPDATE_URL_LOKI)
                data = json.load(response_info)
                # Get download URL
                zip_url = data['assets'][0]['browser_download_url']
                self.logger.log("INFO", "Downloading latest release %s ..." % zip_url)
                response_zip = urllib2.urlopen(zip_url)
            except Exception as e:
                if self.debug:
                    traceback.print_exc()
                self.logger.log("ERROR", "Error downloading the loki update - check your Internet connection")
                sys.exit(1)

            # Read ZIP file
            try:
                zipUpdate = zipfile.ZipFile(StringIO(response_zip.read()))
                for zipFilePath in zipUpdate.namelist():
                    if zipFilePath.endswith("/") or "/config/" in zipFilePath or "/loki-upgrader.exe" in zipFilePath:
                        continue

                    source = zipUpdate.open(zipFilePath)
                    targetFile = "/".join(zipFilePath.split("/")[1:])

                    self.logger.log("INFO", "Extracting %s ..." %targetFile)

                    try:
                        target = file(targetFile, "wb")
                        with source, target:
                                shutil.copyfileobj(source, target)
                    except Exception as e:
                        self.logger.log("ERROR", "Cannot extract %s" % targetFile)
                        if self.debug:
                            traceback.print_exc()

            except Exception as e:
                if self.debug:
                    traceback.print_exc()
                self.logger.log("ERROR", "Error while extracting the signature files from the download package")
                sys.exit(1)

        except Exception as e:
            if self.debug:
                traceback.print_exc()
            return False
        return True


def get_application_path():
    try:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(os.path.realpath(sys.executable))
        else:
            application_path = os.path.dirname(os.path.realpath(__file__))
        if "~" in application_path and platform == "windows":
            # print "Trying to translate"
            # print application_path
            application_path = win32api.GetLongPathName(application_path)
        #if args.debug:
        #    logger.log("DEBUG", "Application Path: %s" % application_path)
        return application_path
    except Exception as e:
        print("Error while evaluation of application path")
        traceback.print_exc()


if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser(description='Loki - Upgrader')
    parser.add_argument('-l', help='Log file', metavar='log-file', default='loki-upgrade.log')
    parser.add_argument('--sigsonly', action='store_true', help='Update the signatures only', default=False)
    parser.add_argument('--progonly', action='store_true', help='Update the program files only', default=False)
    parser.add_argument('--nolog', action='store_true', help='Don\'t write a local log file', default=False)
    parser.add_argument('--debug', action='store_true', default=False, help='Debug output')
    parser.add_argument('--detached', action='store_true', default=False, help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Computername
    if platform == "windows":
        t_hostname = os.environ['COMPUTERNAME']
    else:
        t_hostname = os.uname()[1]

    # Logger
    logger = LokiLogger(args.nolog, args.l, t_hostname, '', False, False, args.debug, platform=platform, caller='upgrader')

    # Update Loki
    updater = LOKIUpdater(args.debug, logger, get_application_path())

    # Updating LOKI
    if not args.sigsonly:
        logger.log("INFO", "Updating LOKI ...")
        updater.update_loki()
    if not args.progonly:
        logger.log("INFO", "Updating Signatures ...")
        updater.update_signatures()

    logger.log("INFO", "Update complete")

    if args.detached:
        logger.log("INFO", "Press any key to return ...")

    sys.exit(0)
