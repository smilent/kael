KAEL_FILE=kael

# set python path to KAEL_FILE
PYTHON_PATH=$( which python )
line=$( head -n 1 $KAEL_FILE)
if ! [[ $line =~ ^#!/ ]]; then
    # python path not set
    echo "#!$PYTHON_PATH" | cat - $KAEL_FILE > tmp && mv tmp $KAEL_FILE
    chmod +x $KAEL_FILE
fi

# add to path
export KAEL_HOME=$( pwd )
export PATH=$PATH:$KAEL_HOME
