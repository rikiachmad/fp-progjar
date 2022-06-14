import logging
import json
import shlex
from logic import ServerInterface

class ServerProtocol:
    def __init__(self):
        self.file = ServerInterface()

    def proses_string(self,string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        c = shlex.split(string_datamasuk.lower())
        try:
            c_request = c[0].strip()
            logging.warning(f"memproses request: {c_request}")
            params = [x for x in c[1:]]
            cl = getattr(self.file,c_request)(params)
            return json.dumps(cl)
        except Exception:
            return json.dumps(dict(status='ERROR',data='request tidak dikenali'))


if __name__=='__main__':
    #contoh pemakaian
    fp = ServerProtocol()
    # print(fp.proses_string("set_location player 1 100 200"))
    # print(fp.proses_string("get_location food 1"))