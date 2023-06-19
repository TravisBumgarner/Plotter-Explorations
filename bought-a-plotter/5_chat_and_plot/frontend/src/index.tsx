import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import styled from 'styled-components';

const client = new W3CWebSocket('ws://127.0.0.1:5001');

const AppWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  flex-direction: column;
`;

const ChatClientWrapper = styled.div`
    width: 70vw;
    height: 70vh;
    border: 2px solid black;
    padding 10px;
    display: flex;
    flex-direction: column;
`;

const ChatInputWrapper = styled.div`
  display: flex;
  min-height: 30px;
`;

const ChatInput = styled.input`
  // box-sizing: border-box;
  flex-grow: 1;
  flex: 1;
`;

const ChatMessage = styled.div``;

const ChatMessagesWrapper = styled.div`
  width: 100%;
  flex-grow: 1;
  background-color: rgba(0, 0, 0, 0.2);
  overflow: scroll;
`;

const App = () => {
  const [hasConnected, setHasConnected] = React.useState<boolean>(false);
  const [messages, setMessages] = React.useState<{ sender: string; message: string }[]>([]);
  const [content, setContent] = React.useState('');
  const [fileContents, setFileContents] = React.useState<string | null>(null)

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const contents = e.target.result;
        console.log(contents); // Display the loaded contents (G-code) in the console
        setFileContents(contents as string)
      };

      reader.readAsText(file);
    }
  };

  const sendMessage = (content: string) => {
    const encodedMessage = JSON.stringify({
      content,
      sender: 'User',
      type: 'TRANSMIT_MESSAGE',
    });
    client.send(encodedMessage);
    setMessages([{ sender: 'User', message: content }, ...messages]);
  };

  const moveLeft = () => {
    sendMessage('G91\r\nG0 X-10\r\nG90\r\n');
  };

  const moveRight = () => {
    sendMessage('G91\r\nG0 X10\r\nG90\r\n');
  };

  const moveUp = () => {
    sendMessage('G91\r\nG0 Y10\r\nG90\r\n');
  };

  const moveDown = () => {
    sendMessage('G91\r\nG0 Y-10\r\nG90\r\n');
  };

  const moveHome = () => {
    sendMessage('G28\r\n');
  }

  const setHome = () => {
    sendMessage('G10 P0 L20 X0 Y0 Z0\r\n');
  }

  const handleArrowKeyPress = (event) => {
    console.log('RUDA', event)
    switch (event.key) {
      case 'Enter':
        submit();
        break;
      case 'ArrowLeft':
        moveLeft();
        break;
      case 'ArrowRight':
        moveRight();
        break;
      case 'ArrowUp':
        moveUp();
        break;
      case 'ArrowDown':
        moveDown();
        break;
      default:
        break;
  };
}

  React.useEffect(() => {
    document.addEventListener('keydown', handleArrowKeyPress, true);

    return () => {
      document.removeEventListener('keypress', handleArrowKeyPress);
    };
  }, []);

  client.onmessage = (message) => {
    console.log(message.data);
    setMessages([{ sender: 'PlotterGPT', message: message.data }, ...messages]);
  };
  if (!hasConnected) {
    client.onopen = (message) => {
      setHasConnected(true);
    };
    return <p>Loading</p>;
  }

  const chatMessages = messages.map(({ message, sender }, index) => {
    return (
      <ChatMessage key={index}>
        <strong>{sender}</strong>: {message}
      </ChatMessage>
    );
  });

  const submit = () => {
    sendMessage(content);
    setContent('');
  };



  const handleChatKeyPress = (event) => {
    console.log('chat key', event.key)
    switch (event.key) {
      case 'Enter':
        submit();
    }
  };

  return (
    <AppWrapper>
      <ChatClientWrapper>
        <ChatMessagesWrapper>{chatMessages}</ChatMessagesWrapper>
        <ChatInputWrapper>
          <ChatInput
            onKeyPress={handleChatKeyPress}
            value={content}
            onChange={(event) => setContent(event.target.value.toUpperCase())}
          />
        </ChatInputWrapper>
      </ChatClientWrapper>
      <ButtonsWrapper>
        <button onClick={moveHome}>Go Home</button>
        <button onClick={() => sendMessage('M3 S0\r\n')}>Pen Up</button>
        <button onClick={() => sendMessage('M3 S1000\r\n')}>Pen Down</button>
        <button onClick={() => sendMessage('$2=3\r\n')}>Invert X and Y</button>
        <button onClick={setHome}>Set Home</button>
        <button onClick={moveLeft}>Move Left</button>
        <button onClick={moveRight}>Move Right</button>
        <button onClick={moveUp}>Move Up</button>
        <button onClick={moveDown}>Move Down</button>
      </ButtonsWrapper>
      <ButtonsWrapper>
        <input type="file" accept=".gcode" onChange={handleFileChange} />
        <button disabled={fileContents === null} onClick={() => {sendMessage(fileContents); setFileContents(null)}}>Ship it.</button>
      </ButtonsWrapper>
    </AppWrapper>
  );
};

const ButtonsWrapper = styled.div`
  display: flex;
  flex-direction: row;
`;

export default App;
export { client };

ReactDOM.render(<App />, document.getElementById('root'));
