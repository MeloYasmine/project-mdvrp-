#!/bin/bash
###############################################################################
# This script is the command that is executed every run.
# Check the examples in examples/
#
# This script is run in the execution directory (execDir, --exec-dir).
#
# PARAMETERS:
# $1 is the candidate configuration number
# $2 is the instance ID
# $3 is the seed
# $4 is the instance name
# The rest ($* after `shift 4') are parameters to the run
#
# RETURN VALUE:
# This script should print one numerical value: the cost that must be minimized.
# Exit with 0 if no error, with 1 in case of error
###############################################################################

EXE=../main_test_with_irace.py
FIXED_PARAMS=""

CONFIG_ID=$1
INSTANCE_ID=$2
SEED=$3
INSTANCE=$4
shift 4 || exit 1
CONFIG_PARAMS=$*

LOGS=log/c${CONFIG_ID}-${INSTANCE_ID}.log
DAT_FILE=dat/c${CONFIG_ID}-${INSTANCE_ID}.dat
touch ${DAT_FILE}


# If the program just prints a number, we can use 'exec' to avoid
# creating another process, but there can be no other commands after exec.
#exec $EXE ${FIXED_PARAMS} -i $INSTANCE ${CONFIG_PARAMS}
# exit 1
# 
# Otherwise, save the output to a file, and parse the result from it.
# (If you wish to ignore segmentation faults you can use '{}' around
# the command.)
# $EXE ${FIXED_PARAMS} -i $INSTANCE --seed ${SEED} ${CONFIG_PARAMS} 1> ${STDOUT} 2> ${STDERR}
python3 $EXE -v --seed ${SEED} ${CONFIG_PARAMS} --datfile ${DAT_FILE} -i $INSTANCE> ${LOGS} 2>&1

error() {
    echo "`TZ=UTC date`: $0: error: $@"
    exit 1
}
# # This may be used to introduce a delay if there are filesystem
# # issues.
# SLEEPTIME=1
# while [ ! -s "${STDOUT}" ]; do
#     sleep $SLEEPTIME
#     let "SLEEPTIME += 1"
# done

# The output of the candidate $CONFIG_ID should be written in the file 
# c${CONFIG_ID}.stdout (see target runner for ACOTSP).
# Does this file exist?
if [ ! -s "${DAT_FILE}" ]; then
    # In this case, the file does not exist. Let's exit with a value 
    # different from 0. In this case irace will stop with an error.
    error "${DAT_FILE}: No such file or directory"
fi

# Ok, the file exist. It contains the whole output written by ACOTSP.
# This script should return a single numerical value, the best objective 
# value found by this run of ACOTSP. The following line is to extract
# this value from the file containing ACOTSP output.
COST=$(cat ${DAT_FILE} | grep -e '^[[:space:]]*[+-]\?[0-9]' | cut -f1)
if ! [[ "$COST" =~ ^[-+0-9.e]+$ ]] ; then
    error "${DAT_FILE}: Output is not a number"
fi

# Print it!
echo "$COST"

# We are done with our duty. Clean files and exit with 0 (no error).
rm -f "${DAT_FILE}" "${LOGS}"
rm -f best.* stat.* cmp.*
exit 0