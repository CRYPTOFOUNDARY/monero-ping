import requests
import json
import pprint
import pdb
import datetime
import simplejson
import socket
import struct
import logging
import coloredlogs


API_URL = "http://api.ipstack.com/"
API_KEY = "-PUT-YOUR-KEY-HERE-" # get it free at https://ipstack.com
LIMIT   = 2
LISTS   = ["gray_list", "white_list"]
OK      = "OK"
TRUNC   = False # Truncate peers list to LIMIT len
DAEMON  = "107.150.28.134:12561" # Monero RPC compatible public node


logging.basicConfig(level=logging.INFO)
coloredlogs.install(fmt="%(message)s")


def ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def geo(ip):
    return requests.get("http://api.ipstack.com/%s?access_key=%s" % (ip, API_KEY)).json()


def visit(peer):
    return {
        "ip": ip(peer["ip"]),
        "geo": geo(ip(peer["ip"]))
    }


dump = lambda name, data: simplejson.dump(
    data, open(name, "w"), default=str, indent=2)


def main():
    data = requests.post(
        f"{DAEMON}/get_peer_list",
        data=json.dumps({}),
        headers={"content-type": "application/json"}
    ).json()

    data["updated_at"] = datetime.datetime.utcnow()

    if data["status"] == OK:
        data["updated_at"] = datetime.datetime.utcnow()
        for color in LISTS:
            if TRUNC:
                logging.warning("Truncating down to %s elements", LIMIT)
                data[color] = data[color][0:LIMIT]
            logging.info(f"Entering {color} group, {len(data[color])} peers")
            group = 0
            for peer in data[color]:
                group += 1
                logging.info(f"{group} / {len(data[color])}")
                peer["info"] = visit(peer)
        logging.info("Saving data")
        dump("data.json", data)
    else:
        logging.error("Status is not OK")

main()
