#This file is part of ClusterRateWatch.
#This file is part of ClusterRateWatch.
#Copyright 2017 William Putnam

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from flask import Flask, render_template, Response, send_file
import time

from shelljob import proc

app = Flask(__name__)

#load directly from localhost without subdirs
@app.route('/')
def get_page():
    return send_file('page.html')
    
#function called by the HTML page
@app.route( '/stream' )
def stream():
    g = proc.Group()
    p = g.run( [ "bash", "-c", "sudo python analyzer.py" ] )
    print "Script launched"

    def read_process():
        while g.is_pending():   
            lines = g.readlines()
            for proc, line in lines:
                yield "data:" + line + "\n\n"

    return Response( read_process(), mimetype= 'text/event-stream' )

#this setting will run the server on localhost
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug = True