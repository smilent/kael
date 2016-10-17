KAEL_FILE=kael

# set python path to KAEL_FILE
PYTHON_PATH=$( which python )
SCRIPT_PATH=$( realpath "${BASH_SOURCE[0]}" )
KAEL_HOME=$( dirname $SCRIPT_PATH )
KAEL_FILE_PATH=$KAEL_HOME/$KAEL_FILE
line=$( head -n 1 $KAEL_FILE_PATH)
if ! [[ $line =~ ^#!/ ]]; then
    # python path not set
    echo "#!$PYTHON_PATH" | cat - $KAEL_FILE_PATH > tmp && mv tmp $KAEL_FILE_PATH
    chmod +x $KAEL_FILE_PATH
fi

# add to path
export KAEL_HOME=$KAEL_HOME
export PATH=$PATH:$KAEL_HOME
