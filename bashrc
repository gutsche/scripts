# .bashrc

# git scripts
export SCRIPTHOME=/uscms/home/gutsche/git-scripts

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# alias
if [ -f $SCRIPTHOME/alias ]; then
    . $SCRIPTHOME/alias
fi

# GutSoft environment
export GUTCODEDIR=/uscms/home/gutsche/work/software/
export GUTHOME=/uscms/home/gutsche
export GUTDATA=/uscms_data/d1/gutsche
export GUTSCRATCH=/uscms_scratch/lpctrk/gutsche/
export GUTBLUE=/uscmst1b_scratch/lpc1/lpctrk/gutsche
export GUTAFS=/afs/fnal/files/home/room3/gutsche
export GUTRESILIENT=/pnfs/cms/WAX/resilient/gutsche

# GutSoft Path
export PATH=~/scripts:~/scripts/cvs_scripts:$PATH

# git scripts
export PATH=$SCRIPTHOME/DAS:$PATH
export PYTHONPATH=$SCRIPTHOME/DAS:$PYTHONPATH

# external software
export EXTERNAL_SOFT=/uscms/home/gutsche/software/external

# rpl
export RPL_DIR=rpl
export RPL_VERSION=1.4.0
export PATH=$EXTERNAL_SOFT/$RPL_DIR/$RPL_VERSION/bin:$PATH
export MANPATH=$EXTERNAL_SOFT/$RPL_DIR/$RPL_VERSION/man:$PATH

# ssh access for cvs
#export CVS_RSH=ssh 
#export CVSROOT=gutsche@cmscvs.cern.ch:/cvs_server/repositories/CMSSW
export CVSROOT=':gserver:cmscvs.cern.ch:/cvs_server/repositories/CMSSW'

export CMS2_NTUPLE_LOCATION=/storage/local/data2/cms1/cms2/
export CMS2_LOCATION=/uscms/home/gutsche/work/software/TAS/CMSSW_3_6_1_patch4/src/CMS2

# set if interactive
if [ -n "$PS1" ]; then

   # fix vi backspace
   # stty erase '^?'

   # prompt
   export PS1="\h:\W> "

   # resize the shell at last 
   resize

fi

md() {
  mkdir -p "$@" && cd "$@"
}
