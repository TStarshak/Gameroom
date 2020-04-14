import React, { Component } from 'react';
import '../Style/Lobby.css';
import Message from './Message';
import { Button } from 'react-bootstrap';
import Notification from '../../MainMenu/JS/Notification';
class ChatRoom extends Component {

    constructor(props) {
        super(props);
        this.state = {
            messages: [
                { id: '123', username: 'Faker', text: 'Yo dude                     fsdf' },
                { id: '123', username: 'Faker', text: 'Yo dude f d sa á' },
                { id: '123', username: 'Faker', text: 'Yo dudfdae' },
                { id: '123', username: 'Faker', text: 'Yo dude' },
                { id: '123', username: 'Faker', text: 'Yo dudefdasfds dfd dfd ' },
                { id: '123', username: 'Faker', text: 'Yo dude' },
                { id: '123', username: 'Faker', text: 'Yo dude fgsdfvf fgf gf fgf gsdfgsdf gdfg fgfg gfgdf  gfgf  gfg  dfdfasdfdsfdsfsdfsdf' },
                { id: '123', username: 'Levi', text: 'Chao may Caps' },
                { id: '123', username: 'Faker', text: 'Chao may' },
                // { id: '234', username: 'Perks', text: 'Chao may Faker' },
                // { id: '123', username: 'Levi', text: 'Chao may Caps' },
                // { id: '123', username: 'Faker', text: 'Chao may' },
                // { id: '234', username: 'Perks', text: 'Chao may Faker' },
                // { id: '123', username: 'Levi', text: 'Chao may Caps' }
            ],
            user: {
                username: 'Levi',
            }
        }
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit() {
        return null;
    }

    handleChange() {
        return null;
    }



    render() {
        return (
            <div className='full chatRoom'>
                <ul className='message-list'>
                    {this.state.messages.map(message => {
                        return (
                            <Message message={message}></Message>
                        )
                    })}
                </ul>
                <form className='send-message-form' onSubmit={this.handleSubmit}>
                    <input
                        onChange={this.handleChange}
                        value={this.state.message}
                        placeholder='Type your message'
                        type="text"
                    />
                    <Button type='submit'>Send</Button>
                </form>
            </div>

        );
    }
}

export default ChatRoom;