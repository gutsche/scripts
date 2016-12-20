#
# Oli's Mac OS X bashrc
#
# echo ""
# echo "	Oli's Mac OS X bash"
# echo ""

# load aliases
test -f ~/.alias && . ~/.alias

# prompt
export PS1="GutSierraMiniBook:\W> "

# less
export LESS="-i -M"

# display for x
#export DISPLAY=127.0.0.1:0.0

# local bin
export PATH=$PATH:/usr/X11/bin:.

# proxy-ssh
export PATH=$PATH:/Users/gutsche/Documents/scripts/Kerberos/

# root
export ROOTSYS=/Users/gutsche/Software/root_v6.06.02
export PATH=$ROOTSYS/bin:$PATH
export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH 
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH

# CVS ROOT
export CVS_RSH=ssh
export CVSROOT=gutsche@cmscvs.cern.ch:/local/reps/CMSSW

# fnal cert
export PATH=$PATH:/usr/local/get-cert

md() {
  mkdir -p "$@" && cd "$@"
}
