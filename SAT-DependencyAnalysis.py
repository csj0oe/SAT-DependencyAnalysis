# !wget https://www.labri.fr/perso/lsimon/option-ia/Search/Master-Class-SAT/pysat.zip
# !unzip -o pysat
# !mv lorensi-pysat-8625ab1d6cdf/src/* .

raw_package_data = '''
libdatrie-doc:
    DependsOn:
        - libjs-jquery
libjs-jquery:
    Breaks:
        - jquery
        - movabletype-opensource
libfstrcmp0-dbg:
    DependsOn:
        - libfstrcmp0
libfstrcmp0:
    DependsOn:
        - libc6
libc6:
    DependsOn:
        - libgcc1
    Breaks:
        - openrc
        - hurd
        - libtirpc1
        - locales
        - locales-all
        - nscd
libgcc1:
    DependsOn:
        - gcc-8-base
        - openrc
    Breaks:
        - gcc-4.3
        - gcc-4.4
        - gcc-4.5

libtirpc1:
    DependsOn:
        - libc6
        - libgssapi-krb5-2
    Breaks:
        - nfs-common
        - nfs-kernel-server

locales:
    DependsOn:
        - libc-bin
        - libc-bin:i386
        - debconf
        - debconf-2.0
        - cdebconf
        - debconf
    Breaks:
        - libc-bin

locales-all:
    Breaks:
        - locales
nscd:
    DependsOn:
        - lsb-base
        - libaudit1
        - libcap2
        - libselinux1

libgssapi-krb5-2:
    DependsOn:
        - libcom-err2
        - libk5crypto3
        - libkrb5-3
        - libkrb5support0
    Breaks:
        - moonshot-gss-eap

nfs-common:
    DependsOn:
        - libcap2
        - libcom-err2
        - libdevmapper1.02.1
        - libevent-2.1-6
        - libgssapi-krb5-2
        - libkeyutils1
        - libkrb5-3
        - libmount1
        - libnfsidmap2
        - libtirpc1
        - libwrap0
        - rpcbind
        - adduser
        - ucf
        - lsb-base
        - keyutils
        - keyutils:i386
    Breaks:
        - nfs-client
        - nfs-kernel-server
'''

import yaml
package_data = yaml.load(raw_package_data)

all_packages = set()
for package in package_data:
  all_packages.add(package)
  dependencies = package_data[package].get('DependsOn', None)
  conflicts = package_data[package].get('Breaks', None)
  if dependencies is not None:
    all_packages.update(set(dependencies))
  if conflicts is not None:
    all_packages.update(set(conflicts))

all_packages = list(all_packages)
print("[+] There are {} packages in the system".format(all_packages.__len__()))

#software_to_install = 'nfs-common'         # cannot install
software_to_install = 'libgssapi-krb5-2' # can install
print("[+] To install {}".format(software_to_install))
print("[..] Checking dependencies..")

CNF = []

from pysat import Solver
solver = Solver()

to_verify = set([software_to_install])
verifed   = []
while to_verify.__len__() > 0:
  software_to_verify = to_verify.pop()
  if software_to_verify in all_packages and software_to_verify not in verifed:
    dependencies = package_data.get(software_to_verify, {}).get('DependsOn', [])
    for dependency in dependencies:
      variable_1 = -all_packages.index(software_to_verify)
      variable_2 = all_packages.index(dependency)
      # print("adding dependencies: {}".format([variable_1, variable_2]))
      CNF.append([variable_1, variable_2])
    CNF.append([all_packages.index(software_to_verify)])
    to_verify.update(dependencies)
    to_verify.__len__()

    conflicts = package_data.get(software_to_verify, {}).get('Breaks', [])
    for conflict in conflicts:
      variable_1 = -all_packages.index(software_to_verify)
      variable_2 = -all_packages.index(conflict)
      # print("adding conflicts: {}".format([variable_1, variable_2]))
      CNF.append([variable_1, variable_2])
    
    verifed.append(software_to_verify)
  elif software_to_verify not in all_packages:
    print("[-] '{}' Not recognized".format(software_to_verify))
  
    

for cnf in CNF:
  solver.addClause(cnf)

print(CNF)
solver.buildDataStructure()
solver.solve()

solution = solver.finalModel
print("[*] Package can be installed? {}".format(solution.__len__() > 0))
