import React, { Component } from 'react';
import ChatRoom from './ChatRoom';
import { Row, Col, Button } from 'react-bootstrap';
import '../Style/Lobby.css';
import Sideboard from './Sideboard'
class Lobby extends Component {

  constructor(props){
    super(props)
    this.state = {
      users: [
        {username: "Faker"},
        {username: "Faker"},
        {username: "Faker"},
        {username: "Faker"},
        {username: "Faker"},
      ]

    }
    this.numPeople = props.numPeople;
  }

  render() {
    return (
      
      <div className='full Lobby'>
        <Button className="end-session" variant="danger">End session</Button>
        <Row className='full'>
          <Col xs={3} className='' style={{ paddingRight: 0 }}>
            <Sideboard users={this.state.users}></Sideboard>
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