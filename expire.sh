#!/bin/bash

s3cmd ls s3://$1 | while read -r line;
  do
	type=`echo $line|awk {'print $1'}`
	if [[ $type == "DIR" ]]
		then
			continue
	fi

	createDate=`echo $line|awk {'print $1" "$2'}`
	createDate=`date -d"$createDate" +%s`
	olderThan=`date -d"-$2" +%s`
	if [[ $createDate -lt $olderThan ]]
		then
			fileName=`echo $line|awk {'print $4'}`
			if [[ $fileName != "" ]]
				then
					#echo "$fileName"
            				s3cmd del "$fileName"
        		fi
    		fi
  done;
