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

export async function streamGcode(gcodeFilePath: string, path: string, baudRate: number): Promise<void> {
  // Open grbl serial port
  const port = new SerialPort({path, baudRate });

  // Open g-code file
  const gcodeFileContent = fs.readFileSync(gcodeFilePath, 'utf-8');
  const gcodeLines = gcodeFileContent.split('\n');

  // Wake up grbl
  await new Promise<void>((resolve) => {
    port.write('\r\n\r\n');
    resolve()
  });

  // Wait for grbl to initialize
  await new Promise<void>((resolve) => setTimeout(resolve, 2000));

  // Flush startup text in serial input
  await new Promise<void>((resolve) => {
    port.flush();
    resolve()
  });

  console.log('Grbl initialized');

  // Stream g-code to grbl
  for (const line of gcodeLines) {
    const instruction = line.trim(); // Strip all EOL characters for consistency
    console.log(`Sending: ${instruction}`);

    const reply = await sendInstructionAndWaitForReply(instruction, port);
    console.log(`Received: ${reply}`);
  }

  // Close the serial port
  port.close();

  console.log('All instructions sent and replies received.');
  process.exit(0)
}