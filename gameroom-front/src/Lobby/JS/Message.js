import React, { Component } from 'react';
import '../Style/Lobby.css';
function Message(props) {
    let message = props.message;
    return (
        <li key={message.id}>
            <div className='message'>
            <div className='message-username'>
                {message.username}
            </div>
            <div className='bounding'>
                <div className='message-text'>
                    {message.message}
                </div>
            </div>
            
        </div>
            
        </li>
    )
}

export default Message;