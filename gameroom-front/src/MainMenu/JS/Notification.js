import React, { Component } from 'react';
import '../Style/Notification.css';
import { Col, Row, Container, Button } from 'react-bootstrap'
function Notification(props) {
    let plength = props.players.length;
    let items = [];
    for (let i = 0; i < Math.ceil(plength / 2); i++){
        let rowItems = []
        for(let j = 0; j < Math.min(2, plength - i * 2); j++){
            rowItems.push(<Col><h2>{props.players[i * 2 + j].name}</h2></Col>)
        }
        items.push(<Row>{rowItems}</Row>)
    }
    // players is a dictionary with users info
    return (
        <div className='popup'>
            <div className='popup\_inner'>
                <h1>You have been matched</h1>
                <Container>
                    {items}
                    <Row>
                        <Col><Button onClick={()=>{
                            let tmp = props.players;
                            tmp.pop(0);
                            props.toRating(tmp);
                        }}>End Session</Button></Col>
                    </Row>
                </Container>
            </div>
        </div> 
    );
}

export default Notification;