![Logo](/lokiicon.jpg)
# Loki - Simple IOC Scanner

Scanner for Simple Indicators of Compromise

Detection is based on four detection methods:

    1. File Name IOC
       Regex match on full file path/name

    2. Yara Rule Check
       Yara signature match on file data and process memory

    3. Hash check
       Compares known malicious hashes (MD5, SHA1, SHA256) with scanned files
       
    4. C2 Back Connect Check
       Compares process connection endpoints with C2 IOCs (new since version v.10)
       
Additional Checks:

    1. Regin filesystem check (via --reginfs)
    2. Process anomaly check (based on [Sysforensics](http://goo.gl/P99QZQ)
    3. SWF decompressed scan (new since version v0.8)
    4. SAM dump check

The Windows binary is compiled with PyInstaller 2.1 and should run as x86 application on both x86 and x64 based systems.

## How-To Run LOKI and Analyse the Reports

### Run

  - Clone the LOKI repository (if you download LOKI as ZIP file, make sure to download the sub-repository [signature-base"](https://github.com/Neo23x0/signature-base) as well and place it in the respective subfolder)
  - Provide the folder to a target system that should be scanned: removable media, network share, folder on target system
  - Right-click on loki.exe and select "Run as Administrator" or open a command line "cmd.exe" as Administrator and run it from there (you can also run LOKI without administrative privileges but some checks will be disabled and relevant objects on disk will not be accessible)

### Reports

  - The resulting report will show a GREEN, YELLOW or RED result line.
  - Please analyse the findings yourself by:
    1. uploading non-confidential samples to Virustotal.com
    2. Search the web for the filename
    3. Search the web for keywords from the rule name (e.g. EQUATIONGroupMalware_1 > search for "Equation Group")
    4. Search the web for the MD5 hash of the sample
  - Please report back false positives via the "Issues" section, which is accessible via the right sidebar (mention the false positive indicator like a hash and/or filename and the rule name that triggered)

## Included IOCs

Loki currently includes the following IOCs:

  - Equation Group Malware (Hashes, Yara Rules [by Kaspersky](http://securelist.com/blog/research/68750/equation-the-death-star-of-malware-galaxy/) and [10 custom rules](http://pastebin.com/P0Fb9DPb) generated by us)
  - Carbanak APT - [Kaspersky Report](http://securelist.com/blog/research/68732/the-great-bank-robbery-the-carbanak-apt/) (Hashes, Filename IOCs - no service detection and Yara rules)
  - Arid Viper APT - [Trendmicro](http://blog.trendmicro.com/trendlabs-security-intelligence/arid-viper-gaza-vs-israel-cyber-conflict/) (Hashes)
  - Anthem APT Deep Panda Signatures (not officialy confirmed) (krebsonsecurity.com - see [Blog Post](http://krebsonsecurity.com/2015/02/china-to-blame-in-anthem-hack/))
  - Regin Malware (GCHQ / NSA / FiveEyes) (incl. Legspin and Hopscotch)
  - Five Eyes QUERTY Malware (Regin Keylogger Module - see: [Kaspesky Report](https://securelist.com/blog/research/68525/comparing-the-regin-module-50251-and-the-qwerty-keylogger/))
  - Skeleton Key Malware (other state-sponsored Malware) - Source: [Dell SecureWorks Counter Threat Unit(TM)](http://www.secureworks.com/cyber-threat-intelligence/threats/skeleton-key-malware-analysis/)
  - WoolenGoldfish - (SHA1 hashes, Yara rules) [Trendmicro Report](http://blog.trendmicro.com/trendlabs-security-intelligence/operation-woolen-goldfish-when-kittens-go-phishing/)
  - OpCleaver (Iranian APT campaign) - Source: [Cylance](http://www.cylance.com/operation-cleaver/)
  - More than 180 hack tool Yara rules - Source: [APT Scanner THOR](http://www.bsk-consulting.de/apt-scanner-thor/)
  - More than 600 web shell Yara rules - Source: [APT Scanner THOR](http://www.bsk-consulting.de/apt-scanner-thor/)
  - Numerous suspicious file name regex signatures - Source: [APT Scanner THOR](http://www.bsk-consulting.de/apt-scanner-thor/)
  - Much more ... (cannot update the list as fast as I include new signatures)

Loki is the new generic scanner that combines most of the features from my recently published scanners: [ReginScanner](https://github.com/Neo23x0/ReginScanner) and [SkeletonKeyScanner](https://github.com/Neo23x0/SkeletonKeyScanner).

## Requirements

No requirements if you use the compiled EXE.

If you want to build it yourself:

- [yara](http://goo.gl/PQjmsf) : It's recommended to use the most recent version of the compiled packages for Windows (x86) - Download it from here: http://goo.gl/PQjmsf
- [colorama](https://pypi.python.org/pypi/colorama) : to color it up
- [psutil](https://pypi.python.org/pypi/psutil) : process checks
- [pylzma] (https://pypi.python.org/pypi/pylzma/)
- [pywin32](http://sourceforge.net/projects/pywin32/) : path conversions (PyInstaller [issue](https://github.com/pyinstaller/pyinstaller/issues/1282); Windows only)
- Microsoft Visual C++ 2010 Redistributable Package (https://www.microsoft.com/en-US/download/details.aspx?id=5555)
- Microsoft Visual C++ Compiler for Python 2.7 (https://www.microsoft.com/en-us/download/details.aspx?id=44266): for pylzma

```
c:\Python27\python.exe -m pip install --upgrade pip
c:\Python27\Scripts\pip.exe install psutil
c:\Python27\Scripts\pip.exe install netaddr
c:\Python27\Scripts\pip.exe install wmi
c:\Python27\Scripts\pip.exe install path\to\colorama-0.3.6-py2.py3-none-any.whl
c:\Python27\Scripts\pip.exe install pylzma
```

Requirements for the Threat Intel receivers:

- [OTX Python SDK](https://github.com/AlienVault-Labs/OTX-Python-SDK)
- [pyMISP](https://github.com/CIRCL/PyMISP)

# Usage

    usage: loki.exe [-h] [-p path] [-s kilobyte] [-l log-file] [--printAll]
                    [--noprocscan] [--nofilescan] [--noindicator] [--reginfs]
                    [--dontwait] [--intense] [--csv] [--onlyrelevant] [--nolog]
                    [--update] [--debug]

    Loki - Simple IOC Scanner

    optional arguments:
      -h, --help      show this help message and exit
      -p path         Path to scan
      -s kilobyte     Maximum file size to check in KB (default 2048 KB)
      -l log-file     Log file
      --printAll      Print all files that are scanned
      --noprocscan    Skip the process scan
      --nofilescan    Skip the file scan
      --noindicator   Do not show a progress indicator
      --reginfs       Do check for Regin virtual file system
      --dontwait      Do not wait on exit
      --intense       Intense scan mode (also scan unknown file types and all
                      extensions)
      --csv           Write CSV log format to STDOUT (machine prcoessing)
      --onlyrelevant  Only print warnings or alerts
      --nolog         Don't write a local log file
      --update        Update the signatures from the "signature-base" sub
                      repository
      --debug         Debug output

## Signature and IOCs

Since version 0.15 the Yara signatures reside in the sub-repository [signature-base](https://github.com/Neo23x0/signature-base). You will not get the sub-repository by downloading the LOKI as ZIP file. It will be included when you clone the repository. 

The IOC files for hashes and filenames are stored in the './signature-base/iocs' folder. All '.yar' files placed in the './signature-base/yara' folder will be initialized together with the rule set that is already included. Use the 'score' value to define the level of the message upon a signature match. 

You can add hash, c2 and filename IOCs by adding files to the './signature-base/iocs' subfolder. All hash IOCs and filename IOC files must be in the format used by LOKI (see the default files). The files must have the strings "hash", "filename" or "c2" in their name to get pulled during initialization.  

For Hash IOCs (divided by newline; hash type is detected automatically)
```
Hash;Description [Reference]
```

For Filename IOCs (divided by newline)
```
Filename as Regex;Description [Reference]
```

# Threat Intel Receivers

Since version v0.10 LOKI includes various threat intel receivers using the public APIs of these services to retrieve and store the IOCs in a format that LOKI understands. It is no problem if these indicators overlap with the ones already included. Loki uses a filename regex or hash only once. (no preformance impact)

The threat intel receivers have also been moved to the [signature-base](https://github.com/Neo23x0/signature-base) sub repository with version 0.15 and can be found in "./signature-base/threatintel".   

Provide your API key via ```-k APIKEY``` or set it in the script header.  

## Open Threat Exchange (OTX) Receiver

It's a simple script that downloads your subscribed events/iocs from [Alienvault OTX](https://otx.alienvault.com) and stores them in the correct format in the './iocs' subfolder. The script is located in the "./threatintel" folder and is named "get-otx-iocs.py". (see requirements above)

```
usage: get-otx-iocs.py [-h] [-k APIKEY] [-o dir] [--verifycert] [--debug]

OTX IOC Receiver

optional arguments:
  -h, --help    show this help message and exit
  -k APIKEY     OTX API key
  -o dir        Output directory
  --verifycert  Verify the server certificate
  --debug       Debug output
```

## MISP Receiver

A simple script that downloads your subscribed events/iocs from a custom [MISP](https://github.com/MISP/MISP) instance and stores them in the correct format in the './iocs' subfolder. YARA rules stored in MISP will be written to the './iocs/yara' subfolder and automatically initialized during startup. The script is located in the "./threatintel" folder and is named "get-misp-iocs.py". (see requirements above)

```
usage: get-misp-iocs.py [-h] [-u URL] [-k APIKEY] [-l tframe] [-o dir]
                        [-y yara-dir] [--verifycert] [--debug]

MISP IOC Receiver

optional arguments:
  -h, --help    show this help message and exit
  -u URL        MISP URL
  -k APIKEY     MISP API key
  -l tframe     Time frame (e.g. 2d, 12h - default=30d)
  -o dir        Output directory
  -y yara-dir   YARA rule output directory
  --verifycert  Verify the server certificate
  --debug       Debug output
```

# Screenshots

Loki Scan

![Screen](/screens/lokiscan2.png)

Regin Matches

![Screen](/screens/lokiscan1.png)

Regin False Positives

![Screen](/screens/lokiscan3.png)

Hash based IOCs

![Screen](/screens/lokiconf1.png)

File Name based IOCs

![Screen](/screens/lokiconf2.png)

Generated log file

![Screen](/screens/lokilog1.png)

# Contact

LOKI scanner on our company homepage
[http://www.bsk-consulting.de/loki-free-ioc-scanner/](http://www.bsk-consulting.de/loki-free-ioc-scanner/)

Twitter
[@cyb3rOps](https://twitter.com/Cyb3rOps)
[@thor_scanner](https://twitter.com/thor_scanner)

If you are interested in a corporate solution for APT scanning, check out Loki's big brother [THOR](http://www.bsk-consulting.de/apt-scanner-thor/).

# Compile the Scanner

Download PyInstaller [v2.1](https://github.com/pyinstaller/pyinstaller/releases/tag/v2.1), switch to the pyinstaller program directory and execute:

    python ./pyinstaller.py -F C:\path\to\loki.py

This will create a `loki.exe` in the subfolder `./loki/dist`.

## Pro Tip (optional)

To include the msvcr100.dll to improve the target os compatibility change the line in the file `./loki/loki.spec` that contains `a.bianries,` to the following:

    a.binaries + [('msvcr100.dll', 'C:\Windows\System32\msvcr100.dll', 'BINARY')],
    
# Use LOKI on Mac OS X

- Download Yara sources from [here](https://github.com/plusvic/yara/releases/tag/v3.4.0)
- Change to folder ```yara-python``` 
- Run ```python setup.py install```
- Also install the requirement mentioned above by ```sudo pip install colorama```

# Antivirus - False Positives

The compiled scanner may be detected by antivirus engines. This is caused by the fact that the scanner is a compiled python script that implement some file system and process scanning features that are also used in compiled malware code.

If you don't trust the compiled executable, please compile it yourself.

# License

Loki - Simple IOC Scanner
Copyright (c) 2015 Florian Roth

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)
