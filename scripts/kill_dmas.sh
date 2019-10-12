num_ps=$(ps -ax | grep dmas | grep python| wc -l)
num_ps=$(($num_ps+$(ps -ax | grep sumo| grep -v grep| wc -l)))

if [ $num_ps -gt 0 ];then
    echo "There are currently $num_ps processes running under the dmas folder. Killing..."
    pkill -f dmas
    pkill -f sumo
    sleep 1
    num_ps=$(ps -ax | grep dmas | grep python| wc -l)
    echo "Number of precess left is $num_ps "
else
    echo "No dmas processes are running in the background"
fi