import React, { Component } from 'react';
import ChatRoom from './ChatRoom';
import { Row, Col, Button } from 'react-bootstrap';
import '../Style/Lobby.css';
import Sideboard from './Sideboard'
class Lobby extends Component {

  constructor(props){
    super(props)
    this.state = {
      room: props.room,
      messages: this.props.messages
    }
    this.numPeople = this.state.room.players.length;
  }

  handleClick = () => {
    this.props.endSession()
    let tmp = this.state.room.players;
    tmp.pop(0);
    this.props.toRating(tmp)
  }



  render() {
    return (
      
      <div className='full Lobby'>
        <Button className="end-session" variant="danger" onClick={this.handleClick}>End session</Button>
        <Row className='full'>
          <Col xs={3} className='' style={{ paddingRight: 0 }}>
            <Sideboard users={this.state.room.players} user={this.props.user}></Sideboard>
          </Col>
          <Col xs={9} className='full ' style={{ paddingLeft: 0 }}>
            <ChatRoom messages={this.state.messages} className='' user={this.props.user} sendMessage={this.props.sendMessage}></ChatRoom>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Lobby;