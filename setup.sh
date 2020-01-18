#!/bin/bash
#
# Program:
#   ssl-checker setup script
#
# Exit Code:
#   1 - Calling syntax error
#   3 - Destination directory does not exist
#
#   11 - Copy file failed
#   13 - Change file permission failed


# ============================
# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
# ============================
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

# ===========================
# Usage: Installation DESTDIR 
# ===========================
function Installation() {
    DESTDIR=${1}

    # Setup process
    cp README.md ${DESTDIR}
    checkCode 11 "Copy README.md failed." &> /dev/null    
    cp requirements.txt ${DESTDIR}
    checkCode 11 "Copy requirements.txt failed." &> /dev/null    

    if [[ ! -f ${DESTDIR}/sites.json ]]; then
        cp sites.json ${DESTDIR}
        checkCode 11 "Copy sites.json failed." &> /dev/null    
    fi

    if [[ ! -f ${DESTDIR}/conf.json ]]; then
        cp conf.json ${DESTDIR}
        checkCode 11 "Copy conf.json failed." &> /dev/null    
    fi

    cp -r checker_pkg ${DESTDIR}
    checkCode 11 "Copy checker_pkg directory failed." &> /dev/null    
    cp -r module_pkg ${DESTDIR}
    checkCode 11 "Copy module_pkg directory failed." &> /dev/null    
    cp checker.py ${DESTDIR}
    checkCode 11 "Copy checker.py failed." &> /dev/null    
    chmod 755 ${DESTDIR}/checker.py
    checkCode 13 "Change checker.py file permission failed." &> /dev/null    
}


# Calling setup format check
USAGE="setup.sh DESTINATION"

if [[ "${#}" -ne 1 ]];  then
    echo -e "USAGE:\n    ${USAGE}"
    exit 1
fi

if [[ ! -d ${1} ]]; then
    echo "ERROR: Destination directory does not exist"
    exit 3
fi


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    echo ""
    Installation ${1}
    ;;
  *)
    echo "System not supported."
    exit 1
esac


echo "ssl-checker setup success."
exit 0