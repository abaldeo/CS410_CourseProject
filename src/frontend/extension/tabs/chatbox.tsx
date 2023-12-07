import React, { useState, useEffect } from 'react'
import { Box, TextField, Typography, Button, CircularProgress } from '@mui/material';
import { styled } from '@mui/material/styles'
import * as style from "./styles.module.css"
import {fetchAnswer} from '../utils/chatbotanswer'


interface Message {
    text: string;
    sender: 'user' | 'bot';
  }
  
  interface MessageBubbleProps {
    sender: 'user' | 'bot';
  }
  
  async function getAnswer(question: string): Promise<string> {
    var ans = ""
    await fetchAnswer(question).then(res => {
      ans = res
    })
    return ans
  }
  
  const MessageBubble = styled(Box)<MessageBubbleProps>`
    background-color: ${({ theme, sender }) =>
      sender === 'user' ? theme.palette.primary.main : theme.palette.grey[300]};
    color: ${({ theme, sender }) => (sender === 'user' ? theme.palette.primary.contrastText : theme.palette.text.primary)};
    padding: 8px 12px;
    border-radius: ${({ sender }) =>
      sender === 'user' ? '16px 16px 0px 16px' : '16px 16px 16px 0px'};
    margin: 4px 0;
    max-width: 70%;
    word-wrap: break-word;
  `;
  
  function ChatBox({}) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isBotTyping, setIsBotTyping] = useState(false);
  
    useEffect(() => {
      const greetingMessage: Message = {
        text: 'Hello! How may I help you today?',
        sender: 'bot',
      };
      setMessages([greetingMessage]);
    }, []);
  
    const handleSend = () => {
      if (input.trim()) {
        setMessages([...messages, { text: input, sender: 'user' }]);
        setInput('');
        setIsBotTyping(true);
        setTimeout(async () => {
          const response = await getAnswer(input);
          console.log(response)
          const bot_response: Message = {
            text: response,
            sender: 'bot',
          };
          setMessages((prevMessages) => [...prevMessages, bot_response]);
          setIsBotTyping(false);
        }, 3000);
      }
    };
  
    const handleKeyPress = (e: React.KeyboardEvent) => {
      if (e.key === 'Enter') {
        handleSend();
      }
    };
  
  
    return (
    <Box display="flex" flexDirection="column" alignItems="center" p={2} bgcolor="#FDFCFA" borderColor="#A9A9A9" height="100vh">
        <Box display="flex" flexDirection="column" width="100%" mb={2} maxHeight="400px" overflow="auto" flexGrow={1}>
        {messages.map((message, index) => (
            <Box
            key={index}
            alignSelf={message.sender === 'user' ? 'flex-end' : 'flex-start'}
            >
            <MessageBubble sender={message.sender}>
                <Typography variant="body2">{message.text}</Typography>
            </MessageBubble>
            </Box>
        ))}
        {isBotTyping && (
            <Box alignSelf="flex-start" display="flex" alignItems="center" pl={1}>
            <CircularProgress size={16} />
            <Typography variant="body2" style={{ marginLeft: '8px' }}>
                Typing...
            </Typography>
            </Box>
        )}
        </Box>
        <Box display="flex" width="100%">
        <TextField
            fullWidth
            variant="outlined"
            size="small"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
        />
        <Button
            color="primary"
            variant="contained"
            onClick={handleSend}
            style={{ marginLeft: '8px' }}
        >
            Send
        </Button>
        </Box>
    </Box>
    );
  };

  export default ChatBox