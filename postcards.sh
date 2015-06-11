scp -i /home/byang/.ssh/id_rsa ./postcard.sh admin@openflow-0.cs.northwestern.edu:~/
ssh -i /home/byang/.ssh/id_rsa admin@openflow-0.cs.northwestern.edu -t "bash ./postcard.sh"

