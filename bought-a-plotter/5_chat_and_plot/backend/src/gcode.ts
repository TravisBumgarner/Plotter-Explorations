import { SerialPort } from 'serialport';
import { ReadlineParser } from '@serialport/parser-readline';
import * as fs from 'fs';

async function sendInstructionAndWaitForReply(instruction: string, port: SerialPort): Promise<string> {
  return new Promise<string>((resolve) => {
    const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }));
    parser.once('data', (line) => {
      const grbl_out = line.trim();
      resolve(grbl_out);``
    });
    port.write(instruction + '\n');
  });
}
const PATH = '/dev/cu.usbserial-10'
const BAUD_RATE = 115200
const port = new SerialPort({ path: PATH, baudRate: BAUD_RATE });

export async function streamGcode(instructions: string[]) {
  console.log(instructions)
  // Flush startup text in serial input
  await new Promise<void>((resolve) => {
    port.flush();
    resolve();
  });

  let replies = ''
  for await (const instruction of instructions) {
    const reply = await sendInstructionAndWaitForReply(instruction, port);
    replies += reply
}
  return replies;
}
