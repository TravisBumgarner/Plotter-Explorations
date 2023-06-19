import * as express from 'express';
import * as http from 'http';
import * as WebSocket from 'ws';
import { streamGcode } from './gcode';

const app = express();

//initialize a simple http server
const server = http.createServer(app);

//initialize the WebSocket server instance
const wss = new WebSocket.Server({ server });

interface ExtWebSocket extends WebSocket {
  isAlive: boolean;
}

interface Message {
  content: string;
  sender: string;
  type: string;
}

wss.on('connection', (ws: WebSocket) => {
  const extWs = ws as ExtWebSocket;
  extWs.isAlive = true;
  ws.on('pong', () => {
    extWs.isAlive = true;
  });

  ws.on('message', async (msg: string) => {
    const parsed: Message = JSON.parse(msg);
    await streamGcode(parsed.content, '/dev/cu.usbserial-10', 115200)
      .then((reply) => {
        wss.clients.forEach((client) => client.send(reply));
      })
      .catch((error) => {
        console.log(error)
        wss.clients.forEach((client) => client.send(`An error occurred: ${JSON.stringify(error)}`));
      });
  });

  ws.on('error', (err) => {
    console.warn(`Client disconnected - reason: ${err}`);
  });
});

setInterval(() => {
  wss.clients.forEach((ws: WebSocket) => {
    const extWs = ws as ExtWebSocket;

    if (!extWs.isAlive) return ws.terminate();

    extWs.isAlive = false;
    ws.ping(null, undefined);
  });
}, 10000);

//start our server
server.listen(5001, () => {
  console.log(`Server started on port 5001`);
});
