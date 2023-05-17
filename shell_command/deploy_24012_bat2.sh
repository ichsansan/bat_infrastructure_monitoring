clear
rsync -arPe "ssh -p 24012" ../../bat_infrastructure_monitoring/ root@10.7.1.116:~/SourceCode/bat_infrastructure_monitoring/
ssh root@10.7.1.116 -p 24012 'rsync -arP ~/SourceCode/bat_infrastructure_monitoring/* bat2:~/SourceCode/bat_infrastructure_monitoring/.'
sleep 1
echo "Tolong start `./start.sh` dari server BAT2"