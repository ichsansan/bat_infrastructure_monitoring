clear
rsync -aPvre "ssh -p 24035" ../../bat_infrastructure_monitoring/ ichsan@10.7.1.116:~/SourceCode/bat_infrastructure_monitoring/
ssh ichsan@10.7.1.116 -p 24035 'cd SourceCode/bat_infrastructure_monitoring/; ./get_process_id.sh'
read -p "Enter process id: " processid
ssh ichsan@10.7.1.116 -p 24035 "kill $processid"
echo "Successfully killed process $processid"
ssh ichsan@10.7.1.116 -p 24035 "cd SourceCode/bat_infrastructure_monitoring/; ./start.sh"