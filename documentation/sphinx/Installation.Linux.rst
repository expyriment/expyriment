.. _Linux:

Platform-specific instructions: Linux
=====================================

All Linux distributions
-----------------------

1. Use your distribution's package manager to install

  * Python3
  * setuptools
  * pip3
  * build-essential (or equivalent)
  * libffi-dev
  * python3-dev
  * PortAudio
  * ffmpeg (for enhanced video support, optional)

2. In a command line, run::

    sudo pip3 install -U pip wheel
    sudo pip3 install -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

For example, in Debian run::

    sudo apt-get install python3 python3-pip python3-setuptools build-essential libffi-dev python3-dev libportaudio2 ffmpeg
    sudo pip3 install -U pip wheel
    sudo pip3 install -U expyriment[all]
    

Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce
    3D desktop effects. To get accurate timing of the visual stimulus
    presentation it is important to switch off desktop effects in your window
    manager!

**Use Python 3.7.6 with pyenv**

    If ``pip install expyriment`` fails, this may be because there is no wheel for your specific version of Python. 
    In that case, a solution is to install Python 3.7.6 in a virtual environment using `pyenv <https://github.com/pyenv/pyenv>`__. In a nutshell::

    curl https://pyenv.run | bash

    cat >> .bashrc <<'EOF'
    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    EOF

    source .bashrc

    pyenv install 3.7.6
    pyenv virtualenv 3.7.6 expyriment

    pyenv activate expyriment
    pip install expyriment[all]


**Use Python 3.7 with anaconda**
 
   If you use the `anaconda distribution <https://www.anaconda/com>`__, you can create an environment for expyriment in the following way (works also for Windows & MacOS)::

   conda create -n expyriment python=3.7
   conda activate expyriment
   pip install expyriment[all]



.. _`release page`: http://github.com/expyriment/expyriment/releases/latest
