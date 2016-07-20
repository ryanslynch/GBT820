import os, subprocess

# Name of institution where pipeline is being run
institution = "McGill"
# Name of HPC machine where pipeline is being run
machine     = "guillimin"
# Timezone of processing site
timezone    = "Canada/Eastern"
# User name on 'machine'
user        = "rlynch"
# Email address where job notifications will be sent (if enabled)
email       = "rlynch+gbt820_jobs@physics.mcgill.ca"
# Walltime limit (hh:mm:ss)
walltimelim = "120:00:00"
# Maximum size of the 'pending' job queue
queuelim    = 30
# Time to wait between submitting a new job when there are no new files or the
# 'pending' queue is full
sleeptime   = 5*60
# Disk quota size of datadir (in bytes)
datadir_lim = 1024**4 - 12*1024**3 # 1 TB - 12 GB of overhead
# Top level analysis directory
topdir      = "/gs/project/bgf-180-ad/GBT820"
# Base working directory for data reduction (should have at least 13 GB free)
baseworkdir = "/localscratch"
# Base temporary directory for data reduction (should have at least 2 GB free)
basetmpdir  = "/localscratch"
# Directory where pipeline scripts are stored
pipelinedir = os.path.join(topdir, "pipeline")
# Directory where raw data files are stored before being processed
datadir     = "/gs/scratch/rlynch/GBT820"
# Directory where job submission files are stored
jobsdir     = os.path.join(topdir, "jobs")
# Directory wehre log files are stored
logsdir     = os.path.join(topdir, "logs")
# Directory where output files are permanently stored
baseoutdir  = os.path.join(topdir, "results")
# Location of FFT zaplist
zaplist     = os.path.join(pipelinedir, "lib", "GBT820.zaplist")
# Pipeline version (as the git hash)
version     = subprocess.Popen("cd %s ; git rev-parse HEAD 2> /dev/null"%pipelinedir,shell=True,stdout=subprocess.PIPE).stdout.readline().strip()
# Databases dictionary
DATABASES = {
    "observations" : {
    "dbnm"   : "CONTACT rlynch@nrao.edu FOR DATABASE NAME",
    "hostnm" : "CONTACT rlynch@nrao.edu FOR DATABASE HOST",
    "usernm" : "CONTACT rlynch@nrao.edu FOR DATABASE USER NAME",
    "passwd" : "CONTACT rlynch@nrao.edu FOR DATABASE PASSWORD",
        },
    }


# Dictionary for holding job submission scripts
subscripts = {"guillimin": 
"""#!/bin/bash
#PBS -S /bin/bash
#PBS -V
#PBS -N {jobnm}
#PBS -M {email}
#PBS -m ae
#PBS -q sw
#PBS -l nodes={nodenm}:ppn=1
#PBS -l walltime={walltimelim}
#PBS -A bgf-180-ae

if [ {nodenm} == 1 ]
  then
    echo -e \"$HOSTNAME
{jobid}
0 0\" > {jobsdir}/{jobnm}.checkpoint
    mkdir -p {workdir}
    mv {filenm} {workdir}
    cp {zaplist} {workdir}
  else
    set -- $({jobsdir}/{jobnm}.checkpoint)
    echo -e \"$HOSTNAME
{jobid}
$3 $4\" > {jobsdir}/{jobnm}.checkpoint
    mv {baseworkdir}/$2 {baseworkdir}/{jobid}
fi
cd {workdir}
search.py -w {workdir} -i {hashnm} {basenm}.fits 
#rm -rf {workdir}
"""
}

subscript = subscripts[machine]
