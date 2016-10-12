## Install
1. remove the first line of kael:
> \#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

2. run command: `source deploy_kael.sh`

## Config
Please configure your own `config.conf` file:

1. splunk\_path: the direct parent dir that contains all your splunk instances. Splunk instances should be named as "splunk\*".
2. app\_path: the folder to store downloaded app
3. ta\_path: the folder to store downloaded ta
4. sa\_path: the folder to store downloaded sa
