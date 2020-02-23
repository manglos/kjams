# -*- coding: utf-8 -*- 
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

        self.end_headers()
        self.wfile.write(b'Hello, world!')
        

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8978), Handler)

server.serve_forever()