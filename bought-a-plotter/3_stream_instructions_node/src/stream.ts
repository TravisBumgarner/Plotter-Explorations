/**
 * Instructed ChatGPT to rewrite stream.py in Node.
 */

import { SerialPort } from 'serialport';
import { ReadlineParser } from '@serialport/parser-readline';
import fs from 'fs';

// Open grbl serial port
const port = new SerialPort({ path: '/dev/cu.usbserial-10', baudRate: 115200 });
const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }))
port.pipe(parser);

// Open g-code file
const gcodeFilePath = 'grbl.gcode';
const gcodeFileContent = fs.readFileSync(gcodeFilePath, 'utf-8');
const gcodeLines = gcodeFileContent.split('\n');

// Wake up grbl
port.write('\r\n\r\n');
setTimeout(() => {
  port.flush();
  console.log('Grbl initialized');
  streamGcode();
}, 2000);

// Stream g-code to grbl
function streamGcode() {
  for (const line of gcodeLines) {
    const l = line.trim(); // Strip all EOL characters for consistency
    console.log(`Sending: ${l}`);
    port.write(`${l}\n`);
  }
}

// Handle grbl response
parser.on('data', (line) => {
  const grbl_out = line.trim();
  console.log(`Received: ${grbl_out}`);
});

// Wait until grbl is finished to close serial port and file
console.log('Press <Enter> to exit and disable grbl.');
process.stdin.once('data', () => {
  port.close();
});

export {}