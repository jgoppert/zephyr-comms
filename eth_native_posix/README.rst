Native Posix Ethernet
#####################

Overview
********

On host terminal 1:
.. code-block:: console
    sudo ./net-setup.sh &

On device sim:
.. code-block:: console
    cd ~/workdir/cerebri
    west build -b native_posix eth_native_posix
    west build -t run

On host terminal 1:
.. code-block:: console
    ping 192.0.2.1

On host terminal 2, connect to shell, find uart device (ex. /dev/pts/3):
.. code-block:: console
    screen /dev/pts3
    net stats

There are many other net commands, you can also ping.
On host terminal 2:
.. code-block:: console
    net ping 192.0.2.2