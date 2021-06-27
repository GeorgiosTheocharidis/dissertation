### Energy demand prediction algorithm using machine learning.  

# Installation instructions
After you clone this code from github you will need to follow this steps
to prepare a valid working environment:

### Install vagrant
[Here](#https://www.vagrantup.com/docs/installation) you can read the 
instructions to install vagrant for your platform.

  
### Change the directory to the top level of the project and start vagrant:


    cd dissertation
    vagrant up
    vagrant ssh
    cd /vagrant

### Run the following commands:


    sudo python3 setup.py develop
    chmod +x unzip-files.sh 
    ./unzip-files.sh
    cd notebooks
    chomod +x j.sh
    ./j.sh

### Start and access jupyter

At this point your screen output should look like the following:

    vagrant@vagrant:/vagrant/notebooks$ ./j.sh 
    [I 21:58:37.027 NotebookApp] Writing notebook server cookie secret to /home/vagrant/.local/share/jupyter/runtime/notebook_cookie_secret
    [W 21:58:37.558 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
    [I 21:58:37.564 NotebookApp] Serving notebooks from local directory: /vagrant/notebooks
    [I 21:58:37.565 NotebookApp] Jupyter Notebook 6.2.0 is running at:
    [I 21:58:37.565 NotebookApp] http://vagrant:8888/?token=b8f972865053aca58f28cd42fc13e2574fc8cdd4fb6f5b8e
    [I 21:58:37.565 NotebookApp]  or http://127.0.0.1:8888/?token=b8f972865053aca58f28cd42fc13e2574fc8cdd4fb6f5b8e
    [I 21:58:37.566 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    [W 21:58:37.570 NotebookApp] No web browser found: could not locate runnable browser.
    [C 21:58:37.571 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///home/vagrant/.local/share/jupyter/runtime/nbserver-35905-open.html
    Or copy and paste one of these URLs:
        http://vagrant:8888/?token=b8f972865053aca58f28cd42fc13e2574fc8cdd4fb6f5b8e
     or http://127.0.0.1:8888/?token=b8f972865053aca58f28cd42fc13e2574fc8cdd4fb6f5b8e

Use the last line of the output and replace the `127.0.0.1:8888` with `127.0.0.1:7888`
to access the notebook from a browser.

