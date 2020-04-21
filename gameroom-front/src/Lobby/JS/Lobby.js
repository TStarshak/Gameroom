import React, { Component } from 'react';
import ChatRoom from './ChatRoom';
import { Row, Col, Button } from 'react-bootstrap';
import '../Style/Lobby.css';
import Sideboard from './Sideboard'
class Lobby extends Component {

  constructor(props){
    super(props)
    this.state = {
      room: {players:[{username: 'scarria'},{username: 'Faker'},{username: 'Levi'},{username: 'Caps'}]}
    }
    this.numPeople = props.numPeople;
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
            <Sideboard users={this.state.room.players}></Sideboard>
          </Col>
          <Col xs={9} className='full ' style={{ paddingLeft: 0 }}>
            <ChatRoom className=''></ChatRoom>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Lobby;