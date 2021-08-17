## __This project was created to aggregate the custom scripts I wrote during my trials through OSCP, HTB, and VHL.__ ##

### *Either Installation approach below will work.* ###

#### PYTHONPATH Install and Uninstall ####
    Add the project location your python path for the appropriate shell.
    ~./bashrc, ~./zshrc etc, session export, etc.
    
    Example:
        To InstallA
            code ~./bashrc
            -- Navigate to bottom and add below --
            export PYTHONPATH=${PYTHONPATH}:/path/to/project/offsec-python

            Then, ensure you install the needed dependencies:
                python -m pip install requests
                python -m pip install beautifulsoup4
        
        To remove:
            Delete directory offsec-python and remove added export line from files above.
        
            Then run:
                    python -m pip uninstall requests
                    python -m pip uninstall beautifulsoup4

#### PIP Install and Uninstall ####
    Navigate to project directory and excute the pip install command.

    Example:
        To Install
            python -m pip install -e offsec-python
        
        To Remove:
            python -m pip uninstall offsec-python 
        
            Then run:
                    python -m pip uninstall requests
                    python -m pip uninstall beautifulsoup4

#### Execute from anywhere ####
    Add bin to PATH variable

    Example:
        code ~./bashrc
        -- Navigate to bottom and add below --
        export PATH=$PATH:/path/to/project/offsec-python/bin

#### Additional Info ####
    For installation options above, if running multiple python versions, simply specify version in shell command
        python -m pip pipCommand package
        python2.7 -m pip pipCommand package
        python3 -m pip pipCommand package