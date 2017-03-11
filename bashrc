# $SCRIPTHOME/bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# alias
if [ -f $SCRIPTHOME/alias ]; then
    . $SCRIPTHOME/alias
fi

# scripts
export PATH=~/scripts:~/scripts/cvs_scripts:$PATH
export PATH=$SCRIPTHOME/DAS:$PATH

# pythonpath
export PYTHONPATH=$SCRIPTHOME/DAS:$PYTHONPATH

# sbt
export PATH=$EXTERNAL_SOFT/sbt-launcher-packaging-0.13.13/bin:$PATH

# ssh access for cvs
export CVS_RSH=ssh 
export CVSROOT=':gserver:cmssw.cvs.cern.ch:/local/reps/CMSSW'

# set if interactive
if [ -n "$PS1" ]; then

   # fix vi backspace
   stty erase '^?'

   # prompt
   export PS1="\h:\W> "

   # resize the shell at last 
   # resize

   # add additional mapping to beginning of line for inside a screen session
   bind '"\C-p": beginning-of-line'

fi

md() {
  mkdir -p "$@" && cd "$@"
}
