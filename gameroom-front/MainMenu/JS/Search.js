import React, { Component } from 'react';
import '../Style/StarRating.css';
import { Container, Col, Row, Button, Form } from 'react-bootstrap';

class Search extends Component {
 

    render() {
        
        return (
            <Container>
                <Form>
                    <Form.Row>
                        <Form.Group as={Col} controlID="formGame">
                            <Form.Label>Game</Form.Label>
                            <Form.Control as={'select'}>
                                <option value='lol'>League of Legend</option>
                                <option value='cod'>Call of Duty</option>
                                <option value='ow'>Overwatch</option>
                                <option value='rl'>Rocket League</option>
                                <option value='d2'>Dota 2</option>
                            </Form.Control>
                        </Form.Group>
                        {/* This can be changed into region for specific games. Will implement later */}
                        <Form.Group as={Col} controlID="formRegion">
                            <Form.Label>Region</Form.Label>
                            <Form.Control as={'select'}>
                                <option value='na'>North America</option>
                                <option value='euw'>Europe West</option>
                                <option value='eue'>Europe East</option>
                                <option value='as'>Asia</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group as={Col} controlID="formTime">
                            <Form.Label>Play Time</Form.Label>
                            <Form.Control as={'select'}>
                                <option value='1'>1 Hour</option>
                                <option value='2'>2 Hours</option>
                                <option value='3'>3 Hours</option>
                                <option value='4'>4 Hours</option>
                                <option value='5'>5 Hours+</option>
                            </Form.Control>
                        </Form.Group>
                    </Form.Row>
                    <Row>
                        <Col>
                            <Button variant="dark" disabled>Create a lobby</Button>
                        </Col>
                        <Col>
                            <Button variant="dark" disabled>Lobby List</Button>
                        </Col>
                        <Col>
                            <Button  onClick={()=>{this.props.toNoti([{name: 'Scarria1'},{name: 'Scarria2'},{name: 'Scarria3'},{name: 'Scarria4'},{name: 'Scarria5'},{name: 'Scarria6'}])}}>Join a lobby</Button>
                        </Col>
                    </Row>

                </Form>
                
            </Container>
        );
    }
}



export default Search;