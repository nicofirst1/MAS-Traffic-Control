num_ps=$(ps -ax | grep dmas | grep python| wc -l)

if [ $num_ps -gt 0 ];then
    echo "There are currently $num_ps processes running under the dmas folder\n Killing..."
    pkill -f dmas
    sleep 1
    num_ps=$(ps -ax | grep dmas | grep python| wc -l)
    echo "Number of precess left is $num_ps "
else
    echo "No dmas processes are running in the background"
fi