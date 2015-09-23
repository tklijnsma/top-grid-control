echo "Hello T3 server"

# Go to the external machine, prepare a log-file
cd $MY_SCRATCH

echo "This is job $MY_JOBID" >> joblog.txt
echo "Running on config file:" >> joblog.txt
echo $FILE_NAMES >> joblog.txt
echo "Contents of config file:" >> joblog.txt
echo $(less $FILE_NAMES) >> joblog.txt

# Copy the config file from local to external
cp -pv $FILE_NAMES top++.cfg

# Set library path for top++
export LD_LIBRARY_PATH=/swshare/LHAPDF/lhapdf-6.1.5/lib/:$LD_LIBRARY_PATH

echo $DATASETPATH >> top++.log
echo "Attempting to run top++:"
/swshare/top++2.0/top++ | tee -a top++.log

echo "Directory contents on external machine:" >> joblog.txt
echo $(ls) >> joblog.txt
