# Script to start NordVPN
# $1 should be the VPN server to connect to. Default: vn1
# $2 should be the protocol "tcp" or "udp". Default: tcp

username="qFYVMUvVDn8EEuPHrZTAzQSK"
password="seHq4emXQHkxioi8UpceP1x1"
openvpn_dir="/etc/openvpn/ovpn_udp/"
server=${1:-"nl918"}
proto=${2:-"udp"}

# if [ "$proto" == "tcp" ]; then
#     proto+="443";
# elif [ $proto == "udp" ]; then
#     proto+="1194";
# fi

echo "" >nordvpn-auth.txt
chmod 200 ./nordvpn-auth.txt
printf "$username\n$password" >nordvpn-auth.txt

sudo openvpn --config $openvpn_dir$server".nordvpn.com."$proto".ovpn" --auth-user-pass ./nordvpn-auth.txt
