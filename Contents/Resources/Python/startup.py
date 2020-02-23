#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import kjams

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/play' or self.path == '/pause':
            kjams.pause()
        
        if self.path == '/next':
            kjams.next()

        if self.path == '/stop':
            kjams.stop()

        if self.path == '/previous':
            kjams.previous()

        if self.path == '/volume-up':
            kjams.volumeUp()

        if self.path == '/volume-down':
            kjams.volumeDown()
        

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8978), Handler)

server.serve_forever()