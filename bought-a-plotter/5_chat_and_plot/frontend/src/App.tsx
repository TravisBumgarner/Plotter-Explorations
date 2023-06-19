import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import styled from 'styled-components';
import { Message } from '../../shared/types';

export const WEBSOCKET_URL = 'ws://127.0.0.1:5001';
const FEED_RATE = 10000

const client = new W3CWebSocket(WEBSOCKET_URL);

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
  const [messages, setMessages] = React.useState<{ sender: string; message: string, timestamp: string }[]>([]);
  const [chatInput, setChatInput] = React.useState('');
  const [fileContents, setFileContents] = React.useState<string[]>([]);
  const chatInputRef = React.useRef<HTMLInputElement>(null);
  const chatContainerRef = React.useRef<HTMLDivElement>(null);

  const checkConnectionStatus = () => {
    if (client.readyState === WebSocket.CLOSED) {
      addMessage({ sender: 'ReactApp', message: 'It would appear the backend has died.' })
    }
  };

  const addMessage = ({sender, message}: {sender: string, message: string}) => {
    setMessages([...messages, { sender, message, timestamp: new Date().toLocaleTimeString() }]);
    scrollToBottom();
  }

  React.useEffect(() => {
    const interval = setInterval(checkConnectionStatus, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const contents = event.target.result;
        const parsedContents = contents
          .split('\n')
          .map((line) => line.trim())
          .filter((line) => line !== '');
        setFileContents(parsedContents);
      };
      reader.readAsText(file);
    }
  };

  const sendMessage = (body: string[]) => {
    const message: Message = { body };
    const encodedMessage = JSON.stringify(message);
    client.send(encodedMessage);
    addMessage({ sender: 'User', message: body.join(',') })
  };

  const invertXAndY = () => {
    sendMessage(['$2=3']);
  };
  const unvertXAndY = () => {
    sendMessage(['$2=0']);
  };
  const penUp = () => {
    sendMessage(['M3 S0']);
  };
  const penDown = () => {
    sendMessage(['M3 S1000']);
  };
  const moveLeft = () => {
    sendMessage(['G91', `G1 X-10 F${FEED_RATE}`, 'G90']);
  };
  const moveRight = () => {
    sendMessage(['G91', `G1 X10 F${FEED_RATE}`, 'G90', '']);
  };
  const moveUp = () => {
    sendMessage(['G91', `G1 Y10 F${FEED_RATE}`, 'G90']);
  };
  const moveDown = () => {
    sendMessage(['G91', `G1 Y-10 F${FEED_RATE}`, 'G90']);
  };
  const moveHome = () => {
    sendMessage(['G28']);
  };
  const setHome = () => {
    sendMessage(['G10 P0 L20 X0 Y0 Z0']);
  };

  const handleArrowKeyPress = (event) => {
    if (chatInputRef.current === document.activeElement) {
      // Don't fire when chat box has focus
      return;
    }

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
    }
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  React.useEffect(() => {
    document.addEventListener('keydown', handleArrowKeyPress, true);

    return () => {
      document.removeEventListener('keypress', handleArrowKeyPress);
    };
  }, []);

  client.onmessage = (message) => {
    addMessage({ sender: 'PlotterGPT', message: message.data })
  };

  if (!hasConnected) {
    client.onopen = (message) => {
      setHasConnected(true);
      addMessage({ sender: 'ReactApp', message: 'Connected to backend' })
    };
    return <p>Loading</p>;
  }

  console.log(messages);
  const chatMessages = messages.map(({ message, sender, timestamp }, index) => {
    return (
      <ChatMessage key={index}>
        ({timestamp}) <strong style={{ fontWeight: 900 }}>{sender}</strong>: {message}
      </ChatMessage>
    );
  });

  const submit = () => {
    setChatInput('');

    if(chatInput === 'CLEAR') {
      setMessages([]);
      return
    } 
    sendMessage([chatInput]);
  };

  const handleChatKeyPress = (event) => {
    switch (event.key) {
      case 'Enter':
        submit();
    }
  };

  return (
    <AppWrapper>
      <ChatClientWrapper>
        <ChatMessagesWrapper ref={chatContainerRef}>{chatMessages}</ChatMessagesWrapper>
        <ChatInputWrapper>
          <ChatInput
            ref={chatInputRef}
            onKeyPress={handleChatKeyPress}
            value={chatInput}
            onChange={(event) => setChatInput(event.target.value.toUpperCase())}
          />
        </ChatInputWrapper>
      </ChatClientWrapper>
      <ButtonsButtonsWrapper>
        <ButtonsWrapper>
          <button onClick={penUp}>Pen Up</button>
          <button onClick={penDown}>Pen Down</button>
        </ButtonsWrapper>
        <ButtonsWrapper>
          <button onClick={moveHome}>Go Home</button>
          <button onClick={setHome}>Set Home</button>
          <button onClick={invertXAndY}>Invert X and Y</button>
          <button onClick={unvertXAndY}>Unvert X and Y</button>
        </ButtonsWrapper>
        <ButtonsWrapper>
          <button onClick={moveLeft}>Move Left</button>
          <button onClick={moveRight}>Move Right</button>
          <button onClick={moveUp}>Move Up</button>
          <button onClick={moveDown}>Move Down</button>
        </ButtonsWrapper>
        <ButtonsWrapper>
          <input type="file" accept=".gcode" onChange={handleFileChange} />
          <button
            disabled={fileContents === null}
            onClick={() => {
              sendMessage(fileContents);
              setFileContents(null);
            }}
          >
            Ship it.
          </button>
        </ButtonsWrapper>
      </ButtonsButtonsWrapper>
      <ul>
        <li>Feed Rate F{FEED_RATE}</li>
      </ul>
    </AppWrapper>
  );
};

const ButtonsButtonsWrapper = styled.div``;

const ButtonsWrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
`;

export default App;
export { client };

ReactDOM.render(<App />, document.getElementById('root'));
