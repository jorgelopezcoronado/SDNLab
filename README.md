Getting your own Software Defined Networking infrastructure up and running
==========================================================================

In general, in order to experiment with Software Defined
Networking (SDN) you need: (i) an SDN controller; (ii) a data-plane
(hosts, forwarding devices) with SDN-enabled forwarding devices (e.g.,
switches); and, finally some SDN *applications* managing the traffic. As
an SDN controller we will be using an [Onos](https://onosproject.org)
controller; the data-plane will be simulated with a
[Mininet](http://mininet.org) (in fact a
[Containernet](https://containernet.github.io), a Mininet fork that uses
Docker images for the hosts); and, the SDN applications are those
included within the Onos controller, and a web (REST) interface for you
to interact with the whole SDN architecture.

Getting the docker images
-------------------------

There are 6 docker images you need for this laboratory. Those are:

1.  The official [Onos docker
    image](https://hub.docker.com/r/onosproject/onos/), to get it,
    execute:

    ```bash
                docker pull onosproject/onos
            
     ```

2.  The official [Containernet docker
    image](https://github.com/containernet/containernet), to get it,
    execute:

    ```bash
                docker pull containernet/containernet
            
    ```



    For the remainng images, it is easier if you copy the contents of
    the
    [docker-images](https://github.com/jorgelopezcoronado/SDNLab/tree/master/docker-images)
    found in this repository. You can download via http or git. Change
    to that directory (`cd docker-images`).

3.  A modified wordpress image (referred as h2), to get it, execute:

    ``` {.bash language="bash"}
                 docker build -t mywordpress ./mywordpress
            
    ```

    For more information on building docker images see [the containers
    lab](https://github.com/letitbeat/containers-lab).

4.  A modified mysql image (referred as h1) , to get it, execute:

    ``` {.bash language="bash"}
                docker build -t mymysql ./mymysql
            
    ```

5.  A modified lab-api image (referred as h3, from the previous lab), to
    get it, execute:

    ``` {.bash language="bash"}
                docker build -t lab-api ./backend
            
    ```

6.  A modified lab-web image (referred as h4, from the previous lab), to
    get it, execute:

    ``` {.bash language="bash"}
                docker build -t lab-web ./frontend
            
    ```

For your knowledge, containernet needs docker images with certain
[requirements](https://github.com/containernet/containernet/wiki/Container-Requirements-and-Compatibility).

Executing the emulated infrastructure
-------------------------------------

Once the images are pulled, and build you can launch your emulated
data-plane and onos controller. To do so, the best way is to create a
`docker-compose` file. Create a file called `docker-compose.yml` with
the following contents (or download it from the repository)

    version: '3.3'

    services:
      onos:
        image: onosproject/onos:latest
        restart: always
        ports:
          - "8181:8181"
          - "6633:6633"
          - "6653:6653"
        container_name: onos

      containernet: 
        depends_on: 
          - onos
        image: containernet/containernet:v1
        volumes:
          - "/var/run/docker.sock:/var/run/docker.sock"      
        privileged: true
        pid: host
        tty: true
        container_name: containernet
        
Install [docker-compose](https://docs.docker.com/compose/install/).

After that, execute the docker *composition* with:

        docker-compose up
        

You may choose to execute it in detached mode (by adding `-d` flag to the
command) or better, open a new terminal.

After a while both of your images will be running, log in into the
containernet image by executing:

            docker exec -it containernet bash
        

Inside the container, to run the intended topology, execute the
following commands:

            mn -c;
            curl https://raw.githubusercontent.com/jorgelopezcoronado/SDNLab/master/custom_ctnnet_topology.py > cmnt.py;
            python cmnt.py
        

Your topology should be up and running, this is the intended topology:

![image](/images/topology.png)

Inside the containernet console you can try to check the connectivity
between hosts, for instance from h1 to h2, execute:

            containernet> h1 ping -c 5 h2
        

Normally, as there are no data-paths configured in your SDN controller
(and therefore switches) you shouldn't be successful. Likewise, if you
point to your wordpress installation at <http://localhost:8080> you
should see a database connection error. For more information on Mininet
basic commands, check the basic [Mininet
walkthrough](http://mininet.org/walkthrough/).

Manipulating SDN components
===========================

There are many ways to configure data-paths with an Onos controller,
however, an easy way is to do it though the Graphical User
Interface (GUI). Newer versions of Onos do not have the GUI enabled by
default, therefore we will use a console to enable it first. Open a new terminal and log in to
your Onos controller via:

            docker exec -it onos bash;
        

Once logged in, execute the Onos Command Line Interface (CLI) or client
console by executing:

            ./apache-karaf-4.2.8/bin/client
        

Inside the Onos console you can check many things, however, for the
moment as there are no connected devices there are few interesting
things to to here. For now, we will enable the GUI by executing:

            app activate org.onosproject.gui
        

You can check the enabled applications with the command:

            apps -s -a
        

Make sure the output contains the Onos GUI. Now, you can go to your Onos
GUI using your browser and going to the address
[localhost:8181/onos/ui/](localhost:8181/onos/ui/). The default username
/ password is *onos/rocks*. Check the GUI and explore the main menu
(bars at the left upper corner).

Go to the main menu `->` Applications. Enable the following applications
(select and hit the play button near the upper right corner):

-   OpenFlow Base Provider (org.onosproject.openflow-base)

-   Proxy ARP/NDP (org.onosproject.proxyarp), just to avoid taking care
    of ARP ourselves :)

-   LLDP Link Provider (org.onosproject.lldpprovider)

-   Host Location Provider (org.onosproject.hostprovider)

Indeed, you could have enabled all these applications via the Onos
console. Go to your containernet console and execute the command:

            containernet> pingall
        

You should still see no connectivity, but, do not worry, we did that
just to make sure our controller recognizes fully our data-plane. Go to
the main menu `->` Topology, you should be able to see the correct
topology (if you do not see the hosts toggle the host visibility by
typing `h` on the GUI or enabling on the display options panel at the left
lower corner).

Configuring SDN data-paths
--------------------------

### Using SDN routing applications

As previously discussed, there are many ways to configure data-paths.
Let us start by the easiest manner. To avoid thinking of such paths and
*avoiding responsibility* is to install an application that decides on
how to connect hosts though the data-plane forwarding devices. Go to the
applications menu and enable
`Reactive Forwarding (org.onosproject.fwd)`. Go to your containernet
console and execute the command:

            containernet> pingall
        

The results should be completely different, you should have near to 0%
packet loss. You may believe that this is a great tool, however, there
is no control over which hosts communicate with each other; simply all
hosts are able to communicate using any protocol. This is at least
insecure, and most probably not functionally desirable, e.g., assume we
need to communicate only `h1` with `h2` and `h3` with `h4` (which is the case
for our lab, why to communicate the mysql database with the lab-api?).
Additionally, our recent study shows that applications may flood the
network or install undesired data-paths; in fact, the reactive
forwarding application floods the network, sending the intended network
packet to all possible output ports until it reaches a host. Therefore,
the network packet actually arrives not only to the intended host but,
to all of them!

Go to the main menu `->` Applications, and disable the reactive
forwarding application (or `app deactivate org.onosproject.fwd` from the
Onos console). Verify that the `pingall` command is not longer working,
and that the wordpress (<http://localhost:8080/>) cannot reach the
database.

### Using Intents

Instead of supplying rules one by one (for the moment) Onos provides the
opportunity to create so called *Intents*, which is to state a data-path
starting at a given host (or switch port) and that finishes at another
host (or switch port). The easiest way to use intents is to do it from
the GUI. To do so, go to the main menu `->` Topology, click h1
(10.0.0.251), while holding shift click h2 (10.0.0.252), and then click
the `Create Host-To-Host Flow` as shown in the picture below.

![image](/images/GUIIntent.png)

Check that there is both ping connectivity between `h1` and `h2` and that
the wordpress works correctly (i.e., the mysql at h1 can be reached by
wordpress at `h2`). Go to the main menu `->` Topology, click on `s1` (the
switch with label `of:0000000000000001`, to see the labels hit the `L` key
on your keyboard), and then click `Show Flow View for This Device` below
the summary panel at the right side. You should understand that the
intent is translated to flow rules. In fact, the intent is translated to
two flow rules, those are:

-   The flow rule with selector
    `IN_PORT:1, ETH_DST:9A:D8:73:D8:90:6B, ETH_SRC:9A:D8:73:D8:90:6A`
    and output to port 2

-   The flow rule with selector
    `IN_PORT:2, ETH_DST:9A:D8:73:D8:90:6A, ETH_SRC:9A:D8:73:D8:90:6B`
    and output to port 1

The meaning of the rules is pretty straightforward. The first rule says
that any packet comming from port 1 (which is connected to `h1`), coming
from the MAC address of `h1`, going to the MAC address of `h2` should be
output to port 2 (which is connected to `s2`). In order to deliver packets
from `h1` to `h2`, what is the rule that complements the previous one on `s2`?
Verify that.

Configuring such intents can be insecure, all type of traffic is
permitted between hosts. Go to the main menu `->` Intents and check that
there are installed intents. Remove both intents and check that no
connectivity is possible between `h1` and `h2` (you can also check that the
flow rules are deleted).

### Using the REST API

Onos provides a REST API to query the controller information and also to
configure it. An easy way to interact with the API is through the Onos
documentation, accessible via
[localhost:8181/onos/v1/docs/](localhost:8181/onos/v1/docs/).

Go to the API URL and check the list of devices. The data exchange
format is JSON, a human-readable format. As an example, consider the
following device description (of s1):

        {
          "id": "of:0000000000000003",
          "type": "SWITCH",
          "available": true,
          "role": "MASTER",
          "mfr": "Nicira, Inc.",
          "hw": "Open vSwitch",
          "sw": "2.5.5",
          "serial": "None",
          "driver": "ovs",
          "chassisId": "3",
          "lastUpdate": "1554293500780",
          "humanReadableLastUpdate": "connected 3h25m ago",
          "annotations": {
            "channelId": "192.168.0.3:37096",
            "managementAddress": "192.168.0.3",
            "protocol": "OF_13"
          }
        }
        

As it can be seen, the switch is an Open vSwitch (as provided by
containernet), check the other properties and check the list of devices
by going to the REST API, `/devices` and clicking on "Try it out!".

Go for the intents are in the REST API
([<http://localhost:8181/onos/v1/docs/#/intents>](http://localhost:8181/onos/v1/docs/#/intents)).
Search for the `POST /intents` section. Introduce the following text
into the *stream* field:

    {
      "type": "PointToPointIntent",
      "appId": "org.onosproject.restconf",
      "priority": 55,
      "ingressPoint":
      {
        "device": "of:0000000000000002",
        "port": "1"
      },
      "egressPoint":
      {
        "device": "of:0000000000000001",
        "port": "1"
      },
      "selector": {
        "criteria": [
        {    
          "type": "ETH_TYPE",
          "ethType": "0x800"
        },
        {
          "type": "IPV4_SRC",
          "ip": "10.0.0.252/32"
        },
        {
          "type": "IPV4_DST",
          "ip": "10.0.0.251/32"
        }, 
        {   
          "type": "IP_PROTO",
          "protocol": 6
        },    
        { 
          "type": "TCP_DST",
          "tcpPort": 3306
        }      
        ]
      }  
    }

Click on the "Try it out!" button. You should receive a successful
response (with code 201). This is how simple is to add an intent though
the REST API. Understand that the selector; the selector *restricts* the
matching traffic, being able to specify in a granular manner to which
type of traffic the intent corresponds. Observe that in the intent the
origin is the port 1 at `s2`, which corresponds to the host `h2`; the
destination port is `3306` due to the fact that wordpress communicates
with a mysql database (that uses port `TCP 3306` at the destiny). If you
try the wordpress at this moment no database communication should
succeed. The reason is that h1 (mysql) cannot reply to the
communication. To do so, add the following intent:

    {
      "type": "PointToPointIntent",
      "appId": "org.onosproject.restconf",
      "priority": 55,
      "ingressPoint":
      {
        "device": "of:0000000000000001",
        "port": "1"
      },
      "egressPoint":
      {
        "device": "of:0000000000000002",
        "port": "1"
      },
      "selector": {
        "criteria": [
        {    
          "type": "ETH_TYPE",
          "ethType": "0x800"
        },
        {
          "type": "IPV4_SRC",
          "ip": "10.0.0.251/32"
        },
        {
          "type": "IPV4_DST",
          "ip": "10.0.0.252/32"
        }, 
        {   
          "type": "IP_PROTO",
          "protocol": 6
        },    
        { 
          "type": "TCP_SRC",
          "tcpPort": 3306
        }      
        ]
      }  
    }

Pay attention that this time the selector has source port `3306`! Try ping
communication and the wordpress database connection. As you can see, the
ping is unsuccessful while the wordpress communication is. This gives a
great level of granularity. Further, there are other advantages of using
intents, for example, assume that the link between `s1` and `s2` gets
interrupted. Intents automatically monitor changes in the topology and
adjust the flow rules to an alternative path (if possible). Observe the
flow rules (either by inspecting the GUI or by CLI executing the command
`flows -s`). Try to simulate a link interruption by going to your
containernet console and executing the following command:

        link s1 s2 down

Observe the flow rules again and check the alternative route they
produced. Bring the link back up (`link s1 s2 up`) and check the flow
rules again. As you can see, the paths do not revert to the original
one. Further, the choice of path is not possible!

### Installing Flow Rules

In case you are doing your own SDN application or if you want to have a
very granular control over the data-paths installed on the data-plane
then installing flow rules is solution. Consider that a flow rule
defines partial paths at a given switch, which packets match at which
port and what is the disposition (output to another port, most
commonly).

To exemplify how to configure a data-path using flow rules let us
configure the data-path(s) h4`<->`s4`<->`s3`<->`h3 for the traffic matching
(i.e., with selector):

        ETH_TYPE=0x800 and IPV4_SRC=10.0.0.254/32 and IPV4_DST=10.0.0.253/32 and IP_PROTO=6 and TCP_DST=5000

Go to the REST API to post flows
(<http://localhost:8181/onos/v1/docs/#!/flows/post_flows>), post the
following flow rule (choose any app ID of your choosing, remember it):

    {
      "flows": 
      [
        {
          "priority": 40000, 
          "timeout": 0,
          "isPermanent": true,
          "deviceId": "of:0000000000000004",
          "treatment": 
          {
            "instructions": 
            [
              {
                "type": "OUTPUT", 
                "port": "3"
              }
            ]
          },
          "selector": 
          {
              "criteria": 
              [
                {    
                  "type": "IN_PORT",
                  "port": "1"
                },
                {    
                  "type": "ETH_TYPE",
                  "ethType": "0x800"
                },
                {
                  "type": "IPV4_SRC",
                  "ip": "10.0.0.254/32"
                },
                {
                  "type": "IPV4_DST",
                  "ip": "10.0.0.253/32"
                }, 
                {   
                  "type": "IP_PROTO",
                  "protocol": 6
                },    
                { 
                  "type": "TCP_DST",
                  "tcpPort": 5000
                }
            ]
          }
        }
      ]
    }
        

Add the corresponding rules so that `h4` can connect to port `5000` at `h3`.
> Hint, there are 3 more rules. 

After adding the rules log in to `h4` using:

            docker exec -it mn.h4 bash
        

Execute the following command:

            curl 10.0.0.253:5000/; echo;
        

If you see a JSON message you have successfully added the rules. If you
see the following message then your rules are wrong:

            curl: (7) Failed to connect to 10.0.0.253 port 5000: Connection refused
        

If you did not configure the rules properly, an easy way to delete flow
rules is to do it via the REST API with an application ID
(<http://localhost:8181/onos/v1/docs/#!/flows/delete_flows_application_appId>).

Should you have any doubts, you can send an email to us: jorge.lopez@telecom-sudparis.eu, jose.reyes@telecom-sudparis.eu
