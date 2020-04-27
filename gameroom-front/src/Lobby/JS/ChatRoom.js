import React, { Component } from 'react';
import '../Style/Lobby.css';
import Message from './Message';
import { Button } from 'react-bootstrap';
import Notification from '../../MainMenu/JS/Notification';
class ChatRoom extends Component {

    constructor(props) {
        super(props);
        this.state = {
            messages: this.props.messages,
            user: this.props.user,
            message: ''
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        setInterval(() => {console.log('update')
             this.setState({ messages: this.props.messages }) },3000)
    }

    handleSubmit = () => {
        this.props.sendMessage(this.state.message)
        this.setState({ message: '' })
    }

    onChange = (e) => {
        this.setState({ 'message': e.target.value });
    }




    render() {
        console.log(this.state.messages)
        return (
            <div className='full chatRoom'>
                <ul className='message-list'>
                    {this.state.messages.map(message => {
                        return (
                            <Message message={message}></Message>
                        )
                    })}
                </ul>
                <form className='send-message-form' >
                    <input
                        onChange={this.onChange}
                        value={this.state.message}
                        placeholder='Type your message'
                        type="text"
                    />
                    <Button onClick={this.handleSubmit}>Send</Button>
                </form>
            </div>

        );
    }
}

export default ChatRoom;