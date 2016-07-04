
import sys
import cgi
import json
import argparse

import numpy as np

import main_model
import normalizer
from config import *

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

model = None
max_analysis_count = 50 - 1

def do_predict_multiple(data):
    output = {}

    count = 0

    for l in xrange(len(data) - 1, MIN_LENGTH, -1):
    # for l in xrange(MIN_LENGTH, len(data)):
        for i in xrange(len(data) - l + 1 - 1, -1, -1):
            if count > max_analysis_count:
                break

            current = normalizer.normalize(np.array(data)[i:i+l])
            result = model.predict(current)[0]
            result = LABEL_LIST[int(result)]

            if result not in output:
                output[result] = 1
            else:
                output[result] += 1

            if result != 'random' and result != 'horizontal' and result != 'vertical':
                count += 1

    return output

def do_predict_single(data):
    current = normalizer.normalize(np.array(data))
    result = model.predict(current)[0]
    result = LABEL_LIST[int(result)]
    return { result : 1 }

def do_predict(data):
    return do_predict_multiple(data)

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        def bad_request():
            self.send_response(400)
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write("Bad request!")


        def random_request():
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            # Send the html message
            self.wfile.write(json.dumps({'result' : {'random' : 1}}))

        data = self.rfile.read(int(self.headers['Content-Length']))
        if 'data' not in data:
            bad_request()
            return

        loaded_data = json.loads(data)
        data = loaded_data['data']
        if len(data) < MIN_LENGTH:
            random_request()
            return

        result = do_predict(data)

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        # Send the html message
        self.wfile.write(json.dumps({'result' : result}))

    #Handler for the GET requests
    def do_GET(self):
        self.send_response(405)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("405 Method not allowed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Server for mouse gesture recognition')
    parser.add_argument('-p', '--port', dest = 'port', default = 8000, help = 'Specify a port for server', type = int)

    args = parser.parse_args()
    args.load = True

    model = main_model.get_model(args)


    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('localhost', args.port), myHandler)
        print 'Started httpserver on port ' , args.port

        #Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        print 'Interrupted! Shutting down the web server'
        server.socket.close()
