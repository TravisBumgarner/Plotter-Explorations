import { SerialPort } from 'serialport';
import { ReadlineParser } from '@serialport/parser-readline';
import * as fs from 'fs';

async function sendInstructionAndWaitForReply(instruction: string, port: SerialPort): Promise<string> {
  return new Promise<string>((resolve) => {
    const parser = port.pipe(new ReadlineParser({ delimiter: '\r\n' }));
    parser.once('data', (line) => {
      const grbl_out = line.trim();
      resolve(grbl_out);
    });
    port.write(instruction + '\n');
  });
}

export async function streamGcode(instruction: string, path: string, baudRate: number) {
  // Open grbl serial port
  const port = new SerialPort({ path, baudRate });

  // Open g-code file
  //   const gcodeFileContent = fs.readFileSync(gcodeFilePath, 'utf-8');
  //   const gcodeLines = gcodeFileContent.split('\n');

  // Wake up grbl
  await new Promise<void>((resolve) => {
    port.write('\r\n\r\n');
    resolve();
  });

  // Wait for grbl to initialize
  await new Promise<void>((resolve) => setTimeout(resolve, 2000));

  // Flush startup text in serial input
  await new Promise<void>((resolve) => {
    port.flush();
    resolve();
  });

  console.log('Grbl initialized');
  console.log('instruction', instruction)
  const reply = await sendInstructionAndWaitForReply(instruction.trim(), port);
  console.log(`Received: ${reply}`);

  // Close the serial port
  port.close();

  return 'All instructions sent and replies received.';
}
